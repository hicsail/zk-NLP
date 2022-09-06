def bitsof(n):
    bits = 1
    while 2**bits < n:
        bits += 1
        if bits > 10000:
            raise Exception(f'Too many bits! {n}')
    return bits
