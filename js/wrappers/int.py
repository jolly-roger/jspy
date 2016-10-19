MASK_32 = (2 ** 32) - 1
MASK_16 = (2 ** 16) - 1


def int32(n):
    if n & (1 << (32 - 1)):
        res = n | ~MASK_32
    else:
        res = n & MASK_32

    return res

def uint32(n):
    return n & MASK_32

def uint16(n):
    return n & MASK_16