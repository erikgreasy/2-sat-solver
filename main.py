"""Copyright 2022 Erik Masny.

2 SAT solver. Code inspired by https://www.geeksforgeeks.org/2-satisfiability-2-sat-problem/
"""

MAX = 100000


adj = [list() for _ in range(MAX)]
adjInv = [list() for _ in range(MAX)]

visited = [None for _ in range(MAX)]
visitedInv = [None for _ in range(MAX)]
stack = []

# this array will store the SCC that the
# particular node belongs to
# int
scc = [None for _ in range(MAX)]

counter = 1


def addEdges(a: int, b: int):
    '''
    adds edges to form the original graph
    '''
    adj[a].append(b)


def addEdgesInverse(a: int,  b: int):
    '''
    add edges to form the inverse graph
    '''
    adjInv[b].append(a)


def dfsFirst(u: int):
    '''
    for STEP 1 of Kosaraju's Algorithm
    '''
    if visited[u]:
        return

    visited[u] = 1

    for i in range(len(adj[u])):
        dfsFirst(adj[u][i])

    stack.append(u)


def dfsSecond(u: int):
    '''
    for STEP 2 of Kosaraju's Algorithm
    '''
    if visitedInv[u]:
        return

    visitedInv[u] = 1

    for i in range(len(adjInv[u])):
        dfsSecond(adjInv[u][i])

    scc[u] = counter


def is2Satisfiable(n: int, m: int, a: list, b: list):
    '''
    function to check 2-Satisfiability
    '''

    # adding edges to the graph
    for i in range(m):
        # variable x is mapped to x
        # variable - x is mapped to n+x = n-(-x)

        # for a[i] or b[i], addEdges - a[i] -> b[i]
        # AND - b[i] -> a[i]
        if a[i] > 0 and b[i] > 0:
            addEdges(a[i]+n, b[i])
            addEdgesInverse(a[i]+n, b[i])
            addEdges(b[i]+n, a[i])
            addEdgesInverse(b[i]+n, a[i])
        elif a[i] > 0 and b[i] < 0:
            addEdges(a[i]+n, n-b[i])
            addEdgesInverse(a[i]+n, n-b[i])
            addEdges(-b[i], a[i])
            addEdgesInverse(-b[i], a[i])
        elif a[i] < 0 and b[i] > 0:
            addEdges(-a[i], b[i])
            addEdgesInverse(-a[i], b[i])
            addEdges(b[i]+n, n-a[i])
            addEdgesInverse(b[i]+n, n-a[i])
        else:
            addEdges(-a[i], n-b[i])
            addEdgesInverse(-a[i], n-b[i])
            addEdges(-b[i], n-a[i])
            addEdgesInverse(-b[i], n-a[i])

    # STEP 1 of Kosaraju's Algorithm which
    # traverses the original graph
    for i in range(1, (2 * n) + 1):
        if not visited[i]:
            dfsFirst(i)

    # STEP 2 of Kosaraju's Algorithm which
    # traverses the inverse graph. After this,
    # array scc[] stores the corresponding value
    while not len(stack) == 0:
        number = stack.pop()

        if not visitedInv[number]:
            dfsSecond(number)
            global counter
            counter += 1

    for i in range(1, n+1):
        # for any 2 variable x and -x lie in
        # same SCC
        if scc[i] == scc[i+n]:
            print("NESPLNITEĽNÁ")
            return

    for i in range(1, n+1):
        if scc[i] < scc[i+n]:
            print(f'x{i}: False')
        else:
            print(f'x{i}: True')

    # no such variables x and -x exist which lie
    # in same SCC
    print("SPLNITEĽNÁ")
    return


# n is the number of variables
# 2n is the total number of nodes
# m is the number of clauses
n = 5
m = 7

# each clause is of the form a or b
# for m clauses, we have a[m], b[m]
# representing a[i] or b[i]

# Note:
# 1 <= x <= N for an uncomplemented variable x
# -N <= x <= -1 for a complemented variable x
# -x is the complement of a variable x

# The CNF being handled is:
# '+' implies 'OR' and '*' implies 'AND'
# (x1+x2)*(x2’+x3)*(x1’+x2’)*(x3+x4)*(x3’+x5)*
# (x4’+x5’)*(x3’+x4)
a = [1, -2, -1, 3, -3, -4, -3]
b = [2, 3, -2, 4, 5, -5, 4]

# We have considered the same example for which
# Implication Graph was made
# is2Satisfiable(n, m, a, b)

a = []
b = []


def main():
    """Main program code"""

    with open('test.txt', 'r') as file:
        first_line = file.readline().split()
        n = int(first_line[0])
        m = int(first_line[1])

        for line in file:
            a.append(int(line.split()[0]))
            b_item = int(line.split()[1])
            if b_item == 0:
                b.append(int(line.split()[0]))
            else:
                b.append(b_item)

    is2Satisfiable(n, m, a, b)


main()
