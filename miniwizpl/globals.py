params = {
    'bitwidth': 64,
    'arithmetic_field': 2**31-1
    'all_statements': []
}

bitwidth = 64

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
