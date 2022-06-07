from miniwizpl import SecretInt, SecretStack, SecretIndexList, print_emp, comment

men = [0, 1, 2]
women = [3, 4, 5]
NUM_PREFS = 3

preference_matrix = SecretIndexList([
    3,4,5,
    3,4,5,
    3,4,5,
    1,2,0,
    2,1,0,
    0,1,2,
    ])

def index(arr, val, start, end):
    return arr[start:end].index(val)

def prefers(w, m, m_p):
    v_m   = index(preference_matrix, m,   w*NUM_PREFS, w*(NUM_PREFS+1))
    v_m_p = index(preference_matrix, m_p, w*NUM_PREFS, w*(NUM_PREFS+1))
    p = v_m < v_m_p
    print(f'does {w} prefer {m} to {m_p}? {p}')
    return p

def gale_shapley():
    unmarried_men = SecretStack(men)
    marriages = SecretIndexList([-1 for _ in women])
    next_proposal = SecretIndexList([0 for _ in men])

    # while unmarried_men:
    for _ in range(2):
        m = unmarried_men.pop()

        comment('set w')
        w = preference_matrix[m*NUM_PREFS + next_proposal[m]]

        comment('next proposal')
        next_proposal[m] += 1
        print(marriages)
        print(f'{m} proposes to {w}')
        wi = w-len(men)

    #     if marriages[wi] == -1:
    #         marriages[wi] = m
    #     elif prefers(w, m, marriages[wi]):
    #         unmarried_men.add(marriages[wi])
    #         marriages[wi] = m
    #     else:
    #         unmarried_men.add(m)
    return marriages

r = gale_shapley()
print(r)
print_emp(r, 'miniwizpl_test.cpp')

#assert r == [1, 2, 0]
