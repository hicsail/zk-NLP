params = {
    'bitwidth': 32,
    'arithmetic_field': 2**31-1,
    'scaling_factor': 2**7,
    'all_statements': [],
    'produce_warnings': True,
    'ram_num_allocs': 0,
    'ram_total_alloc_size': 0,
    'options': set(),
}

bitwidth = 32
arithmetic_field = 97
all_pubvals = {}
all_defs = []
assertions = []
all_statements = []

gensym_num = 0
def gensym(x):
    """
    Constructs a new variable name guaranteed to be unique.
    :param x: A "base" variable name (e.g. "x")
    :return: A unique variable name (e.g. "x_1")
    """

    global gensym_num
    gensym_num = gensym_num + 1
    return f'{x}_{gensym_num}'

def global_set_field(b):
    global arithmetic_field
    print('setting field! old val:', arithmetic_field)
    arithmetic_field = b
    print('setting field! new val:', arithmetic_field)
