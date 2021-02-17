import networkx as nx
import matplotlib.pyplot as plt

grammar = [
    'S->aS',
    'S->bS',
    'S->cD',
    'D->dD',
    'D->bF',
    'D->a',
    'F->bS',
    'F->a'
]


def drawGraph():
    G = nx.DiGraph()
    G.add_edges_from(
        [('S', 'S*'), ('S', 'D'), ('D', 'D*'), ('D', 'F'),
         ('D', '$'), ('F', 'S'), ('F', '$')])

    val_map = {'S': 1.0,
               'S*': 1.0,
               '$': 0.0}

    values = [val_map.get(node, 0.45) for node in G.nodes()]

    red_edges = [('S', 'S*'), ('D', 'D*')]
    black_edges = [edge for edge in G.edges() if edge not in red_edges]
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color=values, node_size=300)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=dict([
        (('S', 'S*'), 'a,b loop'),
        (('S', 'D'), 'c'),
        (('D', 'D*'), 'd loop'),
        (('D', 'F'), 'b'),
        (('D', '$'), 'a'),
        (('F', 'S'), 'b'),
        (('F', '$'), 'a')
    ])
                                 )
    nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
    nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=True)
    plt.show()


def parseGrammar(grammar):

    # initial empty finiteAutomaton dict
    finiteAutomaton = {}

    for grammarRules in grammar:
        rule = grammarRules.split('->')

    # additional dict that will have for key-0 as value a list of nonterminal symbols
    # for each of them we will define an addition dict
    # for key-1 as value is taken the list of terminal/nonterminal symbols from the right side

        subGrammar = {
            0: list(rule[0])[0],
            1: list(rule[1])
        }

    # if in the initial dict we don't have this nonterminal symbol
    # we create a dict in the finiteAutomaton dict that will have all the relations of this nonterminal symbol
        if not subGrammar[0] in finiteAutomaton:
            finiteAutomaton[subGrammar[0]] = {}

    # if the lenght of the expression to the right side of the rule is 1 => this expression is a final expression
        if len(subGrammar[1]) == 1:
            subGrammar[1].append('$')

    # for the dict of non-terminal symbol created in finiteAutomaton dict
    # as we have a right-linear grammar
    # the first character is set as the key that points to the value- the next character at the right
        finiteAutomaton[subGrammar[0]][subGrammar[1][0]] = subGrammar[1][1]

    return finiteAutomaton


def testGrammar(fa, initial, final, inputWord):

    state = initial

    # used for showing the steps of passing the grammar rules

    currword = ""
    print(state + "->")

    for ch in inputWord:
    # if in the initial dict we have this state, and the terminal character is present in this dict as a key value
        if state in fa and ch in fa[state]:
    # the state changes to the value that this key terminal chracter is pointing to
            state = fa[state][ch]
            currword += ch
            generatedWord = currword + state
            print('->' + generatedWord)
        else:
            return False

    return state in final


drawGraph()
finiteAutomaton = parseGrammar(grammar)
print(finiteAutomaton)
while True:
    print('Testing string: -> ')
    inputWord = input()
    if inputWord == '':
        break
    print(testGrammar(finiteAutomaton, 'S', {'$'}, inputWord))
