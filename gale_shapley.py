
men = [0, 1, 2]
women = [3, 4, 5]
NUM_PREFS = 3

preference_matrix = [
    3,4,5,
    3,4,5,
    3,4,5,
    1,2,0,
    2,1,0,
    0,1,2,
    ]

def index(arr, val, start, end):
    return arr[start:end].index(val)

def prefers(w, m, m_p):
    v_m   = index(preference_matrix, m,   w*NUM_PREFS, w*(NUM_PREFS+1))
    v_m_p = index(preference_matrix, m_p, w*NUM_PREFS, w*(NUM_PREFS+1))
    p = v_m < v_m_p
    print(f'does {w} prefer {m} to {m_p}? {p}')
    return p

def gale_shapley():
    unmarried_men = set(men)
    marriages = [-1 for _ in women]
    next_proposal = [0 for _ in men]

    while unmarried_men:
        m = unmarried_men.pop()
        w = preference_matrix[m*NUM_PREFS + next_proposal[m]]
        next_proposal[m] += 1
        print(marriages)
        print(f'{m} proposes to {w}')
        wi = w-len(men)

        if marriages[wi] == -1:
            marriages[wi] = m
        elif prefers(w, m, marriages[wi]):
            unmarried_men.add(marriages[wi])
            marriages[wi] = m
        else:
            unmarried_men.add(m)
    return marriages

r = gale_shapley()
print(r)
assert r == [1, 2, 0]
