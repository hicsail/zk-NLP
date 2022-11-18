import numpy as np
from miniwizpl import *

# n from Doerner, Evans, shelat
NUM_INDIVIDUALS = 35

# q from Doerner, Evans, shelat
NUM_PREFS = 15

# iterations <= n^2
ITERS = NUM_INDIVIDUALS**2
ITERS = 1

# men are 0..n, women are n..2n
men = list(range(NUM_INDIVIDUALS))
women = list(range(NUM_INDIVIDUALS, 2*NUM_INDIVIDUALS))

men_prefs = np.asarray([np.random.choice(women, size=NUM_PREFS, replace=False) for _ in men])
women_prefs = np.asarray([np.random.choice(men, size=NUM_PREFS, replace=False) for _ in women])
prefs = np.vstack([men_prefs, women_prefs])

preference_matrix = list(prefs.flatten())

def prefers(w, m, m_p):
    v_m   = index(preference_matrix, m,   w*NUM_PREFS, NUM_PREFS)
    v_m_p = index(preference_matrix, m_p, w*NUM_PREFS, NUM_PREFS)
    return v_m < v_m_p

def gale_shapley():
    unmarried_men = list(men)
    marriages = [-1 for _ in women]
    next_proposal = [0 for _ in men]

    # while unmarried_men:
    for _ in range(ITERS):
        m = unmarried_men.pop()
        w = preference_matrix[m*NUM_PREFS + next_proposal[m]]
        next_proposal[m] += 1

        wi = w-len(men)

        # branch 1
        if marriages[wi] == -1:
            marriages[wi] = m

        # branch 2
        elif prefers(w, m, marriages[wi]):
            unmarried_men.push(marriages[wi])
            marriages[wi] = m

        # branch 3 (else)
        else:
            unmarried_men.push(m)

    return marriages

r = gale_shapley()
# for i in range(len(women)):
#     log_int(f'marriage of woman {i+len(men)}', r[i])
print('output:', r)
print_emp('miniwizpl_test.cpp')

#assert r == [1, 2, 0]
