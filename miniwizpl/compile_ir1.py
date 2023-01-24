import sys
import numpy as np
from dataclasses import dataclass
from collections import defaultdict
import os
from .globals import *
from .expr import *
from .data_types import *
from .utils import *
import sys
import galois

sys.setrecursionlimit(10000)

output_file = None
current_wire = 0
witness_list = []
IR_MODE = 1
WRITE_TO_WIT = 1
WRITE_TO_REL = 1
all_pubvals = {}
var_env = {}
ram_type = None

@dataclass
class WireVal(AST):
    name: str
    type: type
    val: any

    def __eq__(self, other):
        return Prim('equals', [self, other], val_of(self) == val_of(other))
    def __req__(self, other):
        return Prim('equals', [other, self], val_of(other) == val_of(self))
    def __str__(self):
        return f'WireVal({self.name}, {self.val})'
    __repr__ = __str__


@dataclass
class WireArray:
    wires: any
    val: any
    scale: int

def warn(s):
    if params['produce_warnings']:
        print('Warning:', s)

def next_wire():
    global current_wire
    r = current_wire
    current_wire += 1
    return '$' + str(r)

def emit(s=''):
    global output_file
    if WRITE_TO_REL == 1:
        output_file.write(s)
        output_file.write('\n')
    
def add_array_to_witness(arr):
    s = params['scaling_factor']
    encoded = encode_array(arr, s)
    wires = np.vectorize(add_to_witness, otypes=[str])(encoded)
    return WireArray(wires, encoded, s)

def add_array_constant(arr):
    def add_elt(elt):
        w = next_wire()
        emit(f'  {w} <- < {elt} >; // array const')
        return w

    s = params['scaling_factor']
    encoded = encode_array(arr, s)
    wires = np.vectorize(add_elt, otypes=[str])(encoded)
    return WireArray(wires, encoded, s)

def add_to_witness(obj, comment=None):
    wit_fun = '@private()' if IR_MODE == 0 else '@short_witness'
    wire_name = str(next_wire())
    if WRITE_TO_WIT == 1:
        witness_list.append(obj)
    if comment:
        emit(f'  {wire_name} <- {wit_fun}; // {comment}')
    else:
        emit(f'  {wire_name} <- {wit_fun};')

    return wire_name

def _extended_gcd(a, b):
   """
   Division in integers modulus p means finding the inverse of the
   denominator modulo p and then multiplying the numerator by this
   inverse (Note: inverse of A is B such that A*B % p == 1) this can
   be computed via extended Euclidean algorithm
   """
   x = 0
   last_x = 1
   y = 1
   last_y = 0
   while b != 0:
       quot = a // b
       a, b = b, a % b
       x, last_x = last_x - quot * x, x
       y, last_y = last_y - quot * y, y
   return last_x, last_y

def modular_inverse(x, p):
   """Compute the inverse of x mod p, i.e. b s.t. x*b mod p = 1"""
   b, _ = _extended_gcd(x, p)
   return b % p

int_ops_ir1 = {
    'add': 'add',
    'mul': 'mul',
}

def subst(x, v, e):
    sys.setrecursionlimit(10000)

    assert isinstance(x, SymVar)
    if e is x:
        return v
    elif isinstance(e, (int, float, str, SymVar, SecretInt)):
        return e
    elif isinstance(e, Prim):
        return Prim(e.op, [subst(x, v, a) for a in e.args], e.val)
    else:
        raise RuntimeError('unknown expression type', e)


function_unrollings = defaultdict(int)
exp_cache = {}

def encode_array(arr, s):
    p = params['arithmetic_field']
    enc_arr = np.array((arr * s).astype(int), dtype=object) % p
    return enc_arr

def print_exp_ir1(e):
    if id(e) in exp_cache:
        r, e = exp_cache[id(e)]
        return r
    else:
        r = print_exp_ir1_(e)
        # IMPORTANT: the cache needs to save both r and e
        # otherwise Python will garbage-collect e and re-use its memory location
        # if this happens, id(e) will point to a new object and we'll get the wrong
        # value from the cache
        exp_cache[id(e)] = (r, e)
        return r

def print_exp_ir1_(e):
    global all_pubvals
    global params
    global current_wire
    global WRITE_TO_REL
    global WRITE_TO_WIT

    if isinstance(e, (SecretInt, SecretGF)):
        return add_to_witness(e)

    elif isinstance(e, SymVar):
        return var_env[e.name]

    elif isinstance(e, SecretTensor):
        return add_array_to_witness(val_of(e).detach().numpy())

    elif isinstance(e, SecretArray):
        return add_array_to_witness(val_of(e))

    elif isinstance(e, SecretStack):
        emit('  // begin init stack')
        wvs = [add_to_witness(v) for v in val_of(e)]
        r = next_wire()
        rn = r.replace('$', '')

        emit()
        emit(f'  @function(init_ram_{rn}, @out: {ram_type}:1, @in: 0:1)')
        emit(f'    @plugin(ram_arith_v0, init, {e.max_size+1});')
        emit()

        emit(f'  {r} <- @call(init_ram_{rn}, {print_exp_ir1(0)});')
        emit()
        emit(f'  @call(write_ram, {r}, {print_exp_ir1(0)}, {print_exp_ir1(len(wvs) + 1)}); // stack top')
        for i, w in enumerate(wvs):
            emit(f'  @call(write_ram, {r}, {print_exp_ir1(i+1)}, {w});')
        emit('  // end init stack')
        emit()
        return r

    elif isinstance(e, SecretIndexList):
        emit('  // begin init ram')
        wvs = [add_to_witness(v) for v in val_of(e)]
        r = next_wire()
        rn = r.replace('$', '')

        emit()
        emit(f'  @function(init_ram_{rn}, @out: {ram_type}:1, @in: 0:1)')
        emit(f'    @plugin(ram_arith_v0, init, {len(wvs)});')
        emit()

        emit(f'  {r} <- @call(init_ram_{rn}, {print_exp_ir1(0)});')
        emit()
        for i, w in enumerate(wvs):
            emit(f'  @call(write_ram, {r}, {print_exp_ir1(i)}, {w});')
        emit('  // end init ram')
        emit()
        return r

    elif isinstance(e, WireVal):
        # just return the wire name
        return e.name

    elif isinstance(e, np.int64):
        r = next_wire()
        emit(f'  {r} <- < {e} >;')
        return r

    elif isinstance(e, int):
        r = next_wire()
        emit(f'  {r} <- < {int(e)} >;')
        return r

    elif isinstance(e, galois.Array):
        global all_pubvals
        if int(e) in all_pubvals:
            return all_pubvals[int(e)]
        else:
            r = next_wire()
            emit(f'  {r} <- < {int(e)} >;')
            all_pubvals[int(e)] = r
            return r

    elif str(type(e)) == "<class 'torch.Tensor'>":
        return add_array_constant(e.detach().numpy())

    elif str(type(e)) == "<class 'numpy.ndarray'>":
        return add_array_constant(e)

    elif isinstance(e, Prim):
        if e.op in int_ops_ir1:
            e1, e2 = e.args
            x1 = print_exp_ir1(e1)
            x2 = print_exp_ir1(e2)
            op_sym = int_ops_ir1[e.op]
            r = next_wire()

            emit(f'  {r} <- @{op_sym}({x1}, {x2});')
            return r
        elif e.op == 'mod':
            field = params['arithmetic_field']
            a, p = e.args
            if p != field:
                warn(f'attempting mod {p} in field {field}')
            return print_exp_ir1(a)
        elif e.op == 'rec':
            name, bound, args, func = e.args
            if function_unrollings[name] > bound:
                r = next_wire()
                emit(f'  {r} <- < 0 >;')
                return r
            else:
                function_unrollings[name] += 1
                arg_wires = []
                for a in args:
                    w = print_exp_ir1(a)
                    wv = WireVal(w, int, val_of(a))
                    arg_wires.append(wv)

                body = func(*arg_wires)
                r = print_exp_ir1(body)
                return r
        elif e.op == 'fold':
            xs, f, init = e.args
            assert isinstance(xs, SecretList)

            if IR_MODE == 1:
                xs_wires = [print_exp_ir1(SecretInt(x)) for x in val_of(xs)]
                init_wire = next_wire()
                emit(f'  {init_wire} <- < {init} >;')

                r1 = xs_wires[0]
                rf = xs_wires[-1]
                wires = [next_wire() for _ in range(0, len(val_of(xs))+1)]
                x_wire_val = WireVal('$1', int, None)
                a_wire_val = WireVal('$2', int, None)

                # step 1: create the "abstracted" loop body with anonymous function's inputs
                # we want this step to output code to the .rel file
                # we want this step to NOT output anything to the .wit file
                WRITE_TO_REL = 1
                WRITE_TO_WIT = 0
                loop_body = f(a_wire_val, x_wire_val)

                emit(f' {wires[0]}...{wires[-1]} <- @for i @first {0} @last {len(val_of(xs))}')
                emit(f'   $(i+{len(val_of(xs)) + 1}) <- @anon_call($i, $(i + {len(val_of(xs))}), @instance: 0, @short_witness : 0)')
                ocw = current_wire
                current_wire = 3
                output_wire = print_exp_ir1(loop_body)
                current_wire = ocw
                emit(f'   $0 <- {output_wire};')
                emit(f'   @end')
                emit(f' @end')

                # step 2: run the loop "concretely" with actual values instead of abstracted function inputs
                # we want this step to output witness values to the .wit file
                # we want this step to NOT output anything to the .rel file

                WRITE_TO_REL = 0
                WRITE_TO_WIT = 1
                a_val = val_of(init)
                x_wire_vals = [WireVal(n, int, v) for n, v in zip(xs_wires, val_of(xs))]
                for x_val in x_wire_vals:
                    a_val = f(x_val, val_of(a_val))
                    print_exp_ir1(a_val)

                WRITE_TO_REL = 1
                return wires[-1]
            elif IR_MODE == 0:
                a_wire_name = print_exp_ir1(init)
                a_wire_val = WireVal(a_wire_name, int, val_of(init))
                old_statements = params['all_statements']

                for x_val in val_of(xs):
                    params['all_statements'] = []
                    new_a_val = f(SecretInt(x_val), a_wire_val)
                    for a in params['all_statements']:
                        print_exp_ir1(a)
                    a_wire_name = print_exp_ir1(new_a_val)
                    a_wire_val = WireVal(a_wire_name, int, val_of(new_a_val))

                params['all_statements'] = old_statements
                return a_wire_name

            else:
                raise RuntimeError('unknown IR mode:', IR_MODE)
        elif e.op == 'mux':
            e1, e2, e3 = e.args
            x1 = print_exp_ir1(e1)
            x2 = print_exp_ir1(e2)
            x3 = print_exp_ir1(e3)
            c = params['arithmetic_field'] - 1
            r1 = next_wire()
            emit(f'  {r1} <- @mul({x1}, {x2});')
            r2 = next_wire()
            emit(f'  {r2} <- @mulc({x1}, < {c} >);')
            r4 = next_wire()
            emit(f'  {r4} <- @addc({r2}, < {1} >);')
            r3 = next_wire()
            emit(f'  {r3} <- @mul({r4}, {x3});')
            r_val = next_wire()
            emit(f'  {r_val} <- @add({r1}, {r3});')
            return r_val
        elif e.op == 'equals':
            e1, e2 = e.args
            x1 = print_exp_ir1(e1)
            x2 = print_exp_ir1(e2)
            diff = e1 - e2
            temp_wire_1 = next_wire()
            wire_name_for_diff = next_wire()
            c = params['arithmetic_field'] - 1

            emit(f'  {temp_wire_1} <- @mulc({x2}, < {c} >);')
            emit(f'  {wire_name_for_diff} <- @add({x1}, {temp_wire_1}); // diff')

            if val_of(diff) != 0:
                res = 1
            else:
                res = val_of(diff)

            wire_name_for_res = add_to_witness(SecretInt(res), 'res')
            temp = next_wire()
            emit(f'  {temp} <- @mulc({wire_name_for_res}, < {c} >);')
            r_res = next_wire()
            emit(f'  {r_res} <- @addc({temp}, < 1 >);')

            diff_inv = SecretInt(modular_inverse(val_of(diff), c + 1))

            wire_name_for_diff_inv = add_to_witness(diff_inv, 'diff_inv')

            temp_wire_1 = next_wire()
            emit(f'  {temp_wire_1} <- @addc({wire_name_for_diff_inv}, < 1 >);')

            temp_wire_2 = next_wire()
            emit(f'  {temp_wire_2} <- @mul({wire_name_for_diff}, {temp_wire_1});')

            temp_wire_1 = next_wire()
            emit(f'  {temp_wire_1} <- @mul({temp_wire_2}, {wire_name_for_res});')

            temp_wire_2 = next_wire()
            emit(f'  {temp_wire_2} <- @mulc({wire_name_for_res}, < {c} >);')
            temp_wire_3 = next_wire()
            emit(f'  {temp_wire_3} <- @add({temp_wire_1}, {temp_wire_2});')

            temp_wire_1 = next_wire()
            emit(f'  {temp_wire_1} <- @mulc({wire_name_for_diff}, < {c} >);')
            temp_wire_4 = next_wire()
            emit(f'  {temp_wire_4} <- @add({temp_wire_3}, {temp_wire_1});')

            emit(f'  @assert_zero({temp_wire_4});')
            return r_res
        elif e.op == 'not_equals':
            exp = Prim('not', [Prim('equals', e.args, not val_of(e))], val_of(e))
            return print_exp_ir1(exp)
        elif e.op == 'sub':
            # implementation: multiply x2 by -1
            e1, e2 = e.args
            x1 = print_exp_ir1(e1)
            x2 = print_exp_ir1(e2)
            c = params['arithmetic_field'] - 1

            def negate_wire(w):
                negated_w = next_wire()
                emit(f'  {negated_w} <- @mulc({w}, < {c} >);')
                return negated_w

            def add_wires(w1, w2):
                r = next_wire()
                emit(f'  {r} <- @add({w1}, {w2});')
                return r

            if isinstance(x1, WireArray) and isinstance(x2, WireArray):
                assert x1.scale == x2.scale

                negated_x2_w = np.vectorize(negate_wire, otypes=[str])(x2.wires)
                output_w = np.vectorize(add_wires, otypes=[str])(x1.wires, negated_x2_w)
                return WireArray(output_w, x1.val - x2.val, x1.scale)
            else:
                r = next_wire()
                negated_x2 = negate_wire(x2)
                emit(f'  {r} <- @add({x1}, {negated_x2});')
                return r
        elif e.op == 'lt':
            e1, e2 = e.args
            x1 = print_exp_ir1(e1)
            x2 = print_exp_ir1(e2)
            r = next_wire()
            emit(f'  {r} <- @call(lt, {x1}, {x2});')
        elif e.op == 'and':
            e1, e2 = e.args
            x1 = print_exp_ir1(e1)
            x2 = print_exp_ir1(e2)
            r = next_wire()
            emit(f'  {r} <- @mul({x1}, {x2});')
            return r
        elif e.op == 'or':
            e1, e2 = e.args
            x1 = print_exp_ir1(e1)
            x2 = print_exp_ir1(e2)
            # approach: (x1+x2) - (x1*x2)
            c = params['arithmetic_field'] - 1
            tmp1 = next_wire()
            tmp2 = next_wire()
            neg_tmp2 = next_wire()
            r = next_wire()
            emit(f'  {tmp1} <- @add({x1}, {x2});')
            emit(f'  {tmp2} <- @mul({x1}, {x2});')
            emit(f'  {neg_tmp2} <- @addc({tmp2}, < {c} >);')
            emit(f'  {r} <- @add({tmp1}, {neg_tmp2});')
            return r
        elif e.op == 'log_softmax':
            assert len(e.args) == 1
            # TODO: implement
            warn('log_softmax unimplemented')
            return print_exp_ir1(e.args[0])
        elif e.op == 'relu':
            assert len(e.args) == 1
            x1 = print_exp_ir1(e.args[0])
            p = params['arithmetic_field']

            def eval_relu(x):
                if x > p//2:
                    return int(0)
                else:
                    return int(x // params['scaling_factor'])

            def mk_relu(w):
                r = next_wire()
                emit(f'  {r} <- @call(relu, {w});')
                return r

            output_w = np.vectorize(mk_relu, otypes=[str])(x1.wires)
            new_vals = np.vectorize(eval_relu, otypes=[object])(x1.val)
            new_scale = x1.scale // params['scaling_factor']

            return WireArray(output_w, new_vals, new_scale)
        elif e.op == 'matplus':
            p = params['arithmetic_field']

            def scale_array(ws, scale):
                if ws.scale == scale:
                    return ws
                else:
                    assert scale > ws.scale
                    s = params['scaling_factor']
                    ds = scale // ws.scale
                    assert ds < p

                    def scale_wire(w):
                        new_w = next_wire()
                        emit(f'  {new_w} <- @mulc({w}, < {ds} >);')
                        return new_w

                    new_vs = (ws.val * ds) % p
                    new_ws = np.vectorize(scale_wire, otypes=[str])(ws.wires)
                    return WireArray(new_ws, new_vs, scale)

            e1, e2 = e.args
            x1 = print_exp_ir1(e1)
            x2 = print_exp_ir1(e2)
            scale = max(x1.scale, x2.scale)

            x1s = scale_array(x1, scale)
            x2s = scale_array(x2, scale)
            assert isinstance(x1, WireArray)
            assert isinstance(x2, WireArray)

            output_vals = (x1s.val + x2s.val) % p

            def add_wires(w1, w2):
                r = next_wire()
                emit(f'  {r} <- @add({w1}, {w2});')
                return r

            output_wires = np.vectorize(add_wires, otypes=[str])(x1s.wires, x2s.wires)
            return WireArray(output_wires, output_vals, scale)
        elif e.op == 'matmul':
            e1, e2 = e.args
            p = params['arithmetic_field']
            w1 = print_exp_ir1(e1)
            w2 = print_exp_ir1(e2)

            assert len(w1.val.shape) == 2
            assert len(w2.val.shape) == 2

            a, b1 = w1.val.shape
            b2, c = w2.val.shape
            assert b1 == b2

            C = np.zeros((a, c), dtype = object)
            W = np.zeros((a, c), dtype = object)
            for row in range(a):
                for col in range(c):
                    for elt in range(b1):
                        m = (w1.val[row, elt] * w2.val[elt, col]) % p
                        C[row, col] = (C[row, col] + m) % p
                        m = next_wire()
                        emit(f'  {m} <- @mul({w1.wires[row, elt]}, {w2.wires[elt, col]}); // {row}, {elt} * {elt}, {col}')

                        if W[row, col] == 0:
                            W[row, col] = m
                        else:
                            r = next_wire()
                            emit(f'  {r} <- @add({W[row, col]}, {m});')
                            W[row, col] = r

            return WireArray(W, C, w1.scale * w2.scale)
        elif e.op == 'not' or e.op == 'neg':
            assert len(e.args) == 1
            e1 = e.args[0]
            x1 = print_exp_ir1(e1)
            negated_x2 = next_wire()
            c = params['arithmetic_field'] - 1
            emit(f'  {negated_x2} <- @mulc({x1}, < {c} >);')
            r = next_wire()
            emit(f'  {r} <- @addc({negated_x2}, < {1} >);')
            return r
        elif e.op == 'exp_mod':
            a, b, p = e.args
            field = params['arithmetic_field']

            if field != p:
                warn(f'attempting exponentiation mod {p} in field {field}')

            def exp_by_squaring(x, n):
                assert n > 0
                if n%2 == 0:
                    if n // 2 == 1:
                        return x * x
                    else:
                        return exp_by_squaring(x * x,  n // 2)
                else:
                    return x * exp_by_squaring(x * x, (n - 1) // 2)

            assert isinstance(b, int)
            exp = exp_by_squaring(a, b)
            exp.val = e.val
            return print_exp_ir1(exp)
        elif e.op == 'assert0':
            assert len(e.args) == 1
            x1 = print_exp_ir1(e.args[0])
            if isinstance(x1, WireArray):
                np.vectorize(lambda w: emit(f'  @assert_zero({w});'), otypes=[None])(x1.wires)
            else:
                emit(f'  @assert_zero({x1});')
            return None
        elif e.op == 'reveal_array':
            assert len(e.args) == 1
            x1 = print_exp_ir1(e.args[0])
            assert isinstance(x1, WireArray), e.args[0]
            p = params['arithmetic_field']
            c = p - 1
            total_scale = x1.scale

            def dec_one(x):
                assert x <= p
                if x <= (p-1)/2:
                    return x/total_scale
                else:
                    return (x-p)/total_scale

            for w, v in list(zip(x1.wires.ravel(), x1.val.ravel())):
                m = next_wire()
                vp = (v * c) % p
                vd = dec_one(v)
                emit(f'  {m} <- @addc({w}, < {vp} >); // reveal {v} = {vd}')
                emit(f'  @assert_zero({m});')

            return None
        elif e.op == 'assign':
            var, val = e.args
            if var.name in var_env:
                raise Exception(f'repeated assignment to variable {var}')
            r = print_exp_ir1(val)
            var_env[var.name] = r
            return None
        elif e.op == 'listref':
            e1, e2 = e.args
            v1 = print_exp_ir1(e1)
            v2 = print_exp_ir1(e2)

            r = next_wire()
            emit(f'  {r} <- @call(read_ram, {v1}, {v2});')
            return r
        elif e.op == 'listset':
            e1, e2, e3 = e.args
            v1 = print_exp_ir1(e1)
            v2 = print_exp_ir1(e2)
            v3 = print_exp_ir1(e3)

            emit(f'  @call(write_ram, {v1}, {v2}, {v3});')
        elif e.op == 'listindex':
            xs, val, start, length = e.args
            v_xs = print_exp_ir1(xs)
            v_val = print_exp_ir1(val)
            v_start = print_exp_ir1(start)
            v_length = print_exp_ir1(length)
            r = next_wire()
            emit(f'  {r} <- @call(list_idx, {v_xs}, {v_val}, {v_start}, {v_length});')
            return r
        elif e.op == 'stack_cond_push':
            stk, cond, val = e.args
            v_stk = print_exp_ir1(stk)
            v_cond = print_exp_ir1(cond)
            v_val = print_exp_ir1(val)
            emit(f'  @call(stack_cond_push, {v_stk}, {v_cond}, {v_val});')
            return None
        elif e.op == 'stack_push':
            stk, val = e.args
            v_stk = print_exp_ir1(stk)
            v_val = print_exp_ir1(val)
            emit(f'  @call(stack_push, {v_stk}, {v_val});')
            return None
        elif e.op == 'stack_cond_pop':
            stk, cond = e.args
            v_stk = print_exp_ir1(stk)
            v_cond = print_exp_ir1(cond)
            r = next_wire()
            emit(f'  {r} <- @call(stack_cond_pop, {v_stk}, {v_cond});')
            return r
        elif e.op == 'stack_pop':
            assert len(e.args) == 1
            stk = e.args[0]
            v_stk = print_exp_ir1(stk)
            r = next_wire()
            emit(f'  {r} <- @call(stack_pop, {v_stk});')
            return r
        else:
            raise Exception(f'unknown operator: {e.op}')
    else:
        raise Exception(f'unknown expression type ({type(e)}): {e}')

def emit_relu(bits_per_fe):
    global current_wire
    current_wire = 2

    emit('  @function(relu, @out: 0:1, @in: 0:1)')
    # convert the input field element into bits
    bit_wires = [next_wire() for _ in range(bits_per_fe)]
    emit(f'    1: {bit_wires[0]} ... {bit_wires[-1]} <- @convert(0: $1);')

    # check if it's negative
    non_neg = bit_wires[0]
    for i in range(1, bits_per_fe//2):
        non_neg_next = next_wire()
        emit(f'    {non_neg_next} <- @add({non_neg}, {bit_wires[i]});')
        non_neg = non_neg_next

    # shift top half to the right to re-scale
    bits_to_shift = bitsof(params['scaling_factor'])

    # create the output wires
    output_wires = [next_wire() for _ in range(bits_per_fe)]

    # top half, and first `bits_to_shift` bits: zeros
    for i in range(bits_per_fe//2 + bits_to_shift):
        emit(f'    {output_wires[i]} <- <0>;')

    # bottom half: shit by `bits_to_shift` and AND with `non_neg`
    for i in range(bits_per_fe//2 + bits_to_shift, len(output_wires)):
        emit(f'    {output_wires[i]} <- @mul({bit_wires[i-bits_to_shift]}, {non_neg});')

    # convert back to field element and return
    emit(f'    0: $0 <- @convert(1: {output_wires[0]} ... {output_wires[-1]});')

    emit(f'  @end')
    emit()


def emit_stack_ops():
    global current_wire

    def const(c):
        global current_wire
        r = current_wire
        current_wire += 1
        w = '$' + str(r)
        emit(f'    {w} <- < {c} >;')
        return w


    # --------------------------------------------------
    # PUSH
    # --------------------------------------------------
    current_wire = 2
    emit(f'  @function(stack_push, @in: {ram_type}:1, 0:1)')
    old_top = next_wire()
    new_top = next_wire()
    emit(f'    {old_top} <- @call(read_ram, $0, {const(0)});')
    emit(f'    {new_top} <- @addc({old_top}, <1>);')
    emit(f'    @call(write_ram, $0, {const(0)}, {new_top});')
    emit(f'    @call(write_ram, $0, {new_top}, $0);')
    emit(f'  @end')

    # --------------------------------------------------
    # COND_PUSH
    # --------------------------------------------------
    current_wire = 3
    emit(f'  @function(stack_cond_push, @in: {ram_type}:1, 0:1, 0:1)')

    # get the current top
    current_top = next_wire()
    emit(f'    {current_top} <- @call(read_ram, $0, {const(0)}); // current top idx')

    # construct the new top: (condition AND top+1) OR (NOT condition AND top)
    tmp1 = next_wire()
    negated_cond = next_wire()
    c = params['arithmetic_field'] - 1
    emit(f'    {tmp1} <- @mulc($0, <{c}>);')
    emit(f'    {negated_cond} <- @addc({tmp1}, <1>); // negated condition')

    tmp2 = next_wire()
    tmp3 = next_wire()
    tmp4 = next_wire()
    new_top = next_wire()
    emit(f'    {tmp2} <- @addc({current_top}, <1>);')
    emit(f'    {tmp3} <- @mul($0, {tmp2});')
    emit(f'    {tmp4} <- @mul({negated_cond}, {current_top});')
    emit(f'    {new_top} <- @add({tmp3}, {tmp4}); // new top idx')
    emit(f'    @call(write_ram, $0, {const(0)}, {new_top});')

    # read old_val from the new top
    old_val = next_wire()
    emit(f'    {old_val} <- @call(read_ram, $0, {new_top});')

    # write to the new top: (condition AND val) OR (NOT condition AND old_val)
    tmp5 = next_wire()
    tmp6 = next_wire()
    to_write = next_wire()
    emit(f'    {tmp5} <- @mul($0, $1);')
    emit(f'    {tmp6} <- @mul({negated_cond}, {old_val});')
    emit(f'    {to_write} <- @add({tmp5}, {tmp6}); // new top value')

    # write the new value to the top position
    emit(f'    @call(write_ram, $0, {new_top}, {to_write});')
    emit(f'  @end')

    # --------------------------------------------------
    # POP
    # --------------------------------------------------
    current_wire = 2
    emit(f'  @function(stack_pop, @out: 0:1, @in: {ram_type}:1)')
    # get the current top
    current_top = next_wire()
    emit(f'    {current_top} <- @call(read_ram, $0, {const(0)}); // current top idx')

    # update the top
    c = params['arithmetic_field'] - 1
    new_top = next_wire()
    emit(f'    {new_top} <- @addc({current_top}, <{c}>);')
    emit(f'    @call(write_ram, $0, {const(0)}, {new_top}); // update top')

    # read return val from the old top
    emit(f'    $0 <- @call(read_ram, $0, {current_top});')
    emit(f'  @end')

    # --------------------------------------------------
    # COND_POP
    # --------------------------------------------------
    current_wire = 2
    emit(f'  @function(stack_cond_pop, @out: 0:1, @in: {ram_type}:1, 0:1)')
    # get the current top
    current_top = next_wire()
    emit(f'    {current_top} <- @call(read_ram, $0, {const(0)}); // current top idx')

    # construct the new top: (condition AND top-1) OR (NOT condition AND top)
    tmp1 = next_wire()
    negated_cond = next_wire()
    c = params['arithmetic_field'] - 1
    emit(f'    {tmp1} <- @mulc($1, <{c}>);')
    emit(f'    {negated_cond} <- @addc({tmp1}, <1>); // negated condition')

    tmp2 = next_wire()
    tmp3 = next_wire()
    tmp4 = next_wire()
    new_top = next_wire()
    emit(f'    {tmp2} <- @addc({current_top}, <{c}>);')
    emit(f'    {tmp3} <- @mul($1, {tmp2});')
    emit(f'    {tmp4} <- @mul({negated_cond}, {current_top});')
    emit(f'    {new_top} <- @add({tmp3}, {tmp4}); // new top idx')
    emit(f'    @call(write_ram, $0, {const(0)}, {new_top});')

    # read old_val from the old top
    old_val = next_wire()
    emit(f'    {old_val} <- @call(read_ram, $0, {current_top});')

    # return the value: condition AND old_val
    emit(f'    $0 <- @mul($1, {old_val});')
    emit(f'  @end')
    emit()


def print_ir0(filename):
    global IR_MODE
    global current_wire
    current_wire = 0
    IR_MODE = 0
    print_ir1(filename)
    IR_MODE = 1

def print_ir1(filename):
    global all_defs
    global output_file
    global current_wire
    global var_env
    global ram_type
    var_env = {}
    current_wire = 0
    current_type = 0

    field = params['arithmetic_field']
    #print('field size:', field)

    # INSTANCE OUTPUT
    with open(filename + '.type0.ins', 'w') as f:
        output_file = f

        if IR_MODE == 0:
            emit(f'version 2.0.0-beta;')
            emit(f'public_input;')
            emit(f'@type field {field};')
            emit(f'@begin')
            emit(f'@end')
            emit()

        else:
            emit(f'version 1.0.0;')
            emit(f'field characteristic {field} degree 1;')
            emit(f'instance')
            emit(f'@begin')
            emit(f'@end')
            emit()

    if 'boolean' in params['options']:
        # INSTANCE OUTPUT (boolean)
        with open(filename + '.type1.ins', 'w') as f:
            output_file = f

            if IR_MODE == 0:
                emit(f'version 2.0.0-beta;')
                emit(f'public_input;')
                emit(f'@type field 2;')
                emit(f'@begin')
                emit(f'@end')
                emit()

            else:
                emit(f'version 1.0.0;')
                emit(f'field characteristic 2 degree 1;')
                emit(f'instance')
                emit(f'@begin')
                emit(f'@end')
                emit()

    # RELATION OUTPUT
    with open(filename + '.rel', 'w') as f:
        output_file = f
        bits_per_fe = bitsof(field)

        if IR_MODE == 0:
            emit(f'version 2.0.0-beta;')
            emit(f'circuit;')

            ram_used = params['ram_num_allocs'] > 0 or 'stack' in params['options']

            # if we're using ram, declare it
            if ram_used:
                emit(f'@plugin ram_arith_v0;')

            emit(f'@type field {field};')
            current_type += 1

            if 'boolean' in params['options']:
                emit(f'@type field 2;')
                current_type += 1

                emit(f'@convert(@out: 0:1, @in: 1:{bits_per_fe});')
                emit(f'@convert(@out: 1:{bits_per_fe}, @in: 0:1);')

            # if we're using ram, init the types
            if ram_used:
                ram_type = current_type
                s = '@type @plugin(ram_arith_v0, ram, 0, {0}, {1}, {2});'
                current_type += 1
                
                emit(s.format(params['ram_num_allocs'],
                              params['ram_total_alloc_size'],
                              params['ram_total_alloc_size'])) # TODO: should be live allocation

            emit(f'@begin')

            # if we're using ram, define read/write
            if ram_used:
                emit(f'  @function(read_ram, @out: 0:1, @in: {ram_type}:1, 0:1)')
                emit('    @plugin(ram_arith_v0, read);')
                emit(f'  @function(write_ram, @in: {ram_type}:1, 0:1, 0:1)')
                emit('    @plugin(ram_arith_v0, write);')
                emit()

            # relu for neural networks
            if 'relu' in params['options']:
                emit_relu(bits_per_fe)

            # stack operations
            if 'stack' in params['options']:
                emit_stack_ops()

        else:
            emit(f'version 1.0.0;')
            emit(f'field characteristic {field} degree 1;')
            emit(f'relation')
            emit(f'gate_set: arithmetic;')
            emit(f'features: @function, @for, @switch;')
            emit(f'@begin')

        for a in params['all_statements']:
            print_exp_ir1(a)

        emit('@end')

    # WITNESS OUTPUT
    with open(filename + '.type0.wit', 'w') as f:
        output_file = f

        if IR_MODE == 0:
            emit(f'version 2.0.0-beta;')
            emit(f'private_input;')
            emit(f'@type field {field};')
            emit(f'@begin')
        else:
            emit(f'version 1.0.0;')
            emit(f'field characteristic {field} degree 1;')
            emit(f'short_witness')
            emit(f'@begin')

        for x in witness_list:
            emit(f'< {val_of(x)} >;')

        emit("@end")

    if 'boolean' in params['options']:
        # WITNESS OUTPUT (boolean field)
        with open(filename + '.type1.wit', 'w') as f:
            output_file = f

            if IR_MODE == 0:
                emit(f'version 2.0.0-beta;')
                emit(f'private_input;')
                emit(f'@type field 2;')
                emit(f'@begin')
            else:
                emit(f'version 1.0.0;')
                emit(f'field characteristic 2 degree 1;')
                emit(f'short_witness')
                emit(f'@begin')

                emit("@end")

