import numpy as np
from miniwizpl import *

# n from Doerner, Evans, shelat
NUM_INDIVIDUALS = 35000

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

print("PREFERENCE LIST:")
#print(prefs)

preference_matrix = SecretIndexList(list(prefs.flatten()))

def prefers(w, m, m_p):
    comment('first index')
    v_m   = index(preference_matrix, m,   w*NUM_PREFS, NUM_PREFS)
    comment('second index')
    v_m_p = index(preference_matrix, m_p, w*NUM_PREFS, NUM_PREFS)
    comment('comparison')
    p = v_m < v_m_p
    #print(f'does {w} prefer {m} to {m_p}? {p}')
    return p

def gale_shapley():
    unmarried_men = SecretStack(men)
    marriages = SecretIndexList([-1 for _ in women])
    next_proposal = SecretIndexList([0 for _ in men])

    # while unmarried_men:
    for _ in range(ITERS):
        m = unmarried_men.pop()

        comment('set w')
        w = preference_matrix[m*NUM_PREFS + next_proposal[m]]

        comment('next proposal')
        next_proposal[m] += 1

        # print(marriages)
        # print(f'{m} proposes to {w}')
        log_int('NEW ROUND!!!! proposer:', m)
        log_int('NEW ROUND!!!! proposes TO:', w)
        wi = w-len(men)
        #log_int('wi', wi)

        comment('conditional branch 1')
        b1 = marriages[wi] == -1
        #log_bool('b1', b1)
        #log_int('m', m)
        marriages[wi] = mux(b1, m, marriages[wi])

        comment('conditional branch 2')
        b2 = prefers(w, m, marriages[wi])
        b22 = b2 & (- b1)
        #log_bool('b22', b22)
        unmarried_men.cond_push(b22, marriages[wi])
        #log_bool('b22 again', b22)
        marriages[wi] = mux(b22, m, marriages[wi])

        comment('conditional branch 3 (else)')
        b3 = (- b1) & (- b2)
        #log_bool('b3', b3)
        unmarried_men.cond_push(b3, m)

    return marriages

r = gale_shapley()
# for i in range(len(women)):
#     log_int(f'marriage of woman {i+len(men)}', r[i])
print('output:', r)
print_emp(r[0], 'miniwizpl_test.cpp')

#assert r == [1, 2, 0]
