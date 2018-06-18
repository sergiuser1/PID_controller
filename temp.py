def concModelMussels (c_i, iterations):
    if 20000.0 - c_i > 500.0:
        return iterations
    else:
        c_inew = c_i - 2.0
        return concModelMussels(c_inew, iterations + 1)

print(concModelMussels(20000, 0))

def concModelAlgae (c_i, iterations):
    if iterations == 0:
        return c_i
    else:
        return concModelAlgae(c_i*(2.0**(1/86400)), iterations - 1)

print(concModelAlgae(50000, 86400))
print(50000*(2**(86400/86400)))