from miniwizpl import SecretInt, Prim, print_ir1, assert0

vals = [SecretInt(i) for i in range(900)]
total = SecretInt(0)
for v in vals:
    total += v

assert0(total)

print_ir1("miniwizpl_test")
