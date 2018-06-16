
from advsearch import *

initial_state = [[' ', ' ', ' '],
                 [' ', ' ', ' '],
                 [' ', ' ', ' ']]

def switch_player(player):
    if player == 'x': return 'o'
    else: return 'x'

def is_winning(state, player):
    winning = False
    for i in [0,1,2]:
        if state[i][0] == state[i][1] == state[i][2] == player:
            winning = True
    for j in [0,1,2]:
        if state[0][j] == state[1][j] == state[2][j] == player:
            winning = True
    if state[0][0] == state[1][1] == state[2][2] == player:
        winning = True
    if state[0][2] == state[1][1] == state[2][0] == player:
        winning = True
    return winning

def is_tie(state):
    blanks = 0
    for i in [0,1,2]:
        for j in [0,1,2]:
            if state[i][j] == ' ': blanks += 1
    return(blanks == 0 and not is_winning(state, 'x') and not is_winning(state, 'o'))

def is_terminal(state):
    return is_winning(state, 'x') or is_winning(state, 'o') or is_tie(state)

def utility(state, player):
    if is_winning(state, player): return 1
    if is_winning(state, switch_player(player)): return -1
    return 0

def copy_state(state):
    nextstate = list(state)
    nextstate[0] = list(state[0])
    nextstate[1] = list(state[1])
    nextstate[2] = list(state[2])
    return nextstate

def possible_transitions(state, player):
    transitions = {}
    for y in [0,1,2]:
        for x in [0,1,2]:
            if state[y][x] == ' ':
                nextstate = copy_state(state)
                nextstate[y][x] = player
                transitions[(x,y)] = nextstate
    return transitions

def print_state(state):
    print "  0 1 2"
    for i in [0,1,2]:
        print i,
        for j in [0,1,2]:
            print state[i][j],
        print
        print "  ------"
    print "  ======"

def make_graphviz_node(state, trans):
    color = "black"
    s = "<table border=\"0\">"
    for i in [0, 1, 2]:
        s += "<tr>"
        for j in [0, 1, 2]:
            if trans is not None and trans[0] == i and trans[1] == j:
                token = ("<font color=\"grey50\">%c</font>" % state[i][j])
            else:
                token = ("<font color=\"%s\">%c</font>" % (color, state[i][j]))
                s += "<td border=\"1\" width=\"20\" color=\"" + color + "\">" + \
                     str(token) + "</td>"
        s += "</tr>"
    s += "</table>"
    return s

# for experiments:
def random_initial_state(n):
    xs = ['x' for _ in range(n)]
    os = ['o' for _ in range(n)]
    spaces = [' ' for _ in range(9 - 2 * n)]
    arranged = (xs + os + spaces)
    random.shuffle(arranged)
    state = []
    for i in [0,1,2]:
        state.append([])
        for j in [0,1,2]:
            state[i].append(arranged[i*3+j])
    return state

# for experiments:
def experiment():
    print "n, minimax, alphabeta"
    for i in range(10):
        for n in range(5):
            state = random_initial_state(n)
            (trans_minimax, um, checked_minimax, _) = \
                run_minimax(state, possible_transitions, 'x', switch_player,
                            utility, is_winning, make_graphviz_node, False)
            (trans_alphabeta, ua, checked_alphabeta, _) = \
                run_minimax(state, possible_transitions, 'x', switch_player,
                            utility, is_winning, make_graphviz_node, True)
            print "%d, %d, %d" % (n, checked_minimax, checked_alphabeta)

## manually create search tree graph for a certain starting state:
# (trans, val, checked, graphviz) = run_minimax([['x', 'x', ' '],
#                                                ['o', 'o', ' '],
#                                                [' ', ' ', ' ']],
#                                               possible_transitions, 'x',
#                                               switch_player, utility, is_winning, make_graphviz_node, True)

## print trans, val, checked
# create_graph(graphviz, False)


def game_loop():
    state = copy_state(initial_state)
    player = 'x'
    while (not is_terminal(state)):
        print_state(state)
        if player == 'x':
            print "Searching..."
            (x,y) = minimax(state, 'x', possible_transitions, is_terminal,
                            utility, switch_player)
            state[y][x] = 'x'
        else:
            x = input("Move x coordinate? ")
            y = input("Move y coordinate? ")
            state[y][x] = 'o'
        player = switch_player(player)

    print_state(state)

    if is_winning(state, 'x'):
        print "Computer wins."
    elif is_winning(state, 'o'):
        print "Human wins."
    elif is_tie(state):
        print "Tie."

game_loop()
