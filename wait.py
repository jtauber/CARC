def signed(x):
    if x >= 0x80:
        return x - 0x100
    return x


def sbc(A, M, C):
    value = A - M - (1 - C)
    if value < 0:
        C = 0
        value += 0x100
    else:
        C = 1
    A = value & 0xFF
    Z = 1 if A == 0 else 0
    return A, C, Z


def time(A):
    cycles = 0

    stack = []

    C = 1
    cycles += 2
    while True:
        stack.append(A)
        cycles += 3
        while True:
            A, C, Z = sbc(A, 1, C)
            cycles += 2
            if Z:
                cycles += 2
                break
            cycles += 3
        A = stack.pop()
        cycles += 4
        A, C, Z = sbc(A, 1, C)
        cycles += 2
        if Z:
            cycles += 2
            break
        cycles += 3
    cycles += 6  # RTS

    return cycles

for A in range(0, 10):
    print(A, time(A), A*A*2.5 + A*13.5 + 7, sep="\t")

print(time(86))  
