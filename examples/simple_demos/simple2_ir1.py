from miniwizpl import SecretInt, Prim, print_ir1, assert0

vals = [SecretInt(i) for i in range(9)]
total = SecretInt(0)
for v in vals:
    total += v

assert0(total - total)

print_ir1("miniwizpl_test")
