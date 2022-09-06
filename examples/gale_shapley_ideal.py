
men = [0, 1, 2]
women = [3, 4, 5]

preference_matrix = [
    [3,4,5],
    [3,4,5],
    [3,4,5],
    [1,2,0],
    [2,1,0],
    [0,1,2]
    ]

def prefers(w, m, m_p):
    pl = preference_matrix[w]
    p = pl.index(m) < pl.index(m_p)
    print(f'does {w} prefer {m} to {m_p}? {p}')
    return p

def gale_shapley():
    unmarried_men = men
    marriages = {}
    next_proposal = [0 for _ in men]

    while unmarried_men:
        m = unmarried_men.pop()
        w = preference_matrix[m][next_proposal[m]]
        next_proposal[m] += 1
        print(marriages)
        print(f'{m} proposes to {w}')

        if w not in marriages:
            print('branch 1')
            marriages[w] = m
        elif prefers(w, m, marriages[w]):
            print('branch 2')
            unmarried_men.append(marriages[w])
            marriages[w] = m
        else:
            print('branch 3')
            unmarried_men.append(m)
    return marriages

print(gale_shapley())
    
