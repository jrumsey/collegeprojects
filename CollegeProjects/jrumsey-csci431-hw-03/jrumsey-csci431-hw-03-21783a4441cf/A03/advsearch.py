from sys import stdout
from subprocess import Popen, PIPE
import re

def create_graph(graphviz, last_only):
    if last_only:
        first = len(graphviz) - 1
    else:
        first = 0
    for i in range(first, len(graphviz)):
        g = "digraph G {\n"
        for j in range(i+1):
            g += graphviz[j]
        if i != (len(graphviz)-1):
            g += "node [color=\"white\"]; edge [color=\"white\"];\n"
        for j in range(i+1, len(graphviz)):
            s = graphviz[j]
            s = re.sub(r'color=".*?"', 'color="white"', s)
            g += s
        g += "}\n"
        p = Popen(['dot', '-Tpng', '-o', "%03d.png" % i],
                  stdin=PIPE, stdout=PIPE, stderr=PIPE)
        p.stdin.write(g)
        p.communicate()

def show_graph(graphviz):
    p = Popen(['dot', '-Txlib'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    p.stdin.write("digraph G {\n")
    for g in graphviz:
        p.stdin.write(g)
    p.stdin.write("}\n")
    p.communicate()

checked = 0
graphviz = []

def run_graph_minimax(state, possible_transitions, player,
                      switch_player, utility, is_winning, make_graphviz_node,
                      use_alphabeta):
    global checked, graphviz
    checked = 0
    graphviz = []
    this = 0

    alpha = None
    beta = None
    (best_trans, best_u, _) = minimax("max", state, None, possible_transitions,
                                      player, player, switch_player,
                                      utility, is_winning, make_graphviz_node, None, 1,
                                      alpha, beta, use_alphabeta)
    return (best_trans, best_u, checked, graphviz)

def graph_minimax(min_or_max, state, trans, possible_transitions, oplayer, player,
                  switch_player, utility, is_winning, make_graphviz_node, parent, depth,
                  alpha, beta, use_alphabeta):
    global checked, graphviz
    checked += 1
    this = len(graphviz)
    if parent is not None:
        graphviz.append(("%d [label=<%s>, shape=\"none\"];"
                         "\n%d->%d [label=\" %s%s\", fontcolor=\"black\"];\n") % \
                            (this, make_graphviz_node(state, trans), parent, this,
                             ("max" if min_or_max == "min" else "min"),
                             ((", &alpha;=%s,&beta;=%s" % \
                                   (("%.2f" % alpha) if alpha is not None else "?",
                                    ("%.2f" % beta) if beta is not None else "?")
                               if use_alphabeta else ""))))
    else:
        graphviz.append("0 [label=<%s>, shape=\"none\"];\n" % make_graphviz_node(state, None))

    transitions = possible_transitions(state, player)
    if is_winning(state, player) or \
            is_winning(state, switch_player(player)) or \
            len(transitions) == 0:
        this2 = len(graphviz)
        graphviz.append(("%d [label=\"%.2f\", color=\"black\", fontcolor=\"black\"];"
                         "\n%d->%d [dir=\"none\"];\n") % \
                            (this2, utility(state, oplayer, depth), this, this2))

        return (trans, utility(state, oplayer, depth), this)
    else:
        best_trans = None
        best_u = None
        best_child = None
        tried = 0
        for trans in transitions:
            (_, u, child) = minimax(("max" if min_or_max == "min" else "min"),
                                    transitions[trans], trans, possible_transitions,
                                    oplayer, switch_player(player), switch_player,
                                    utility, is_winning, make_graphviz_node, this, depth+1,
                                    alpha, beta, use_alphabeta)
            tried += 1
            if best_u is None or \
                    (min_or_max == "min" and u < best_u) or \
                    (min_or_max == "max" and u > best_u):
                best_trans = trans
                best_u = u
                best_child = child
            if use_alphabeta and min_or_max == "min" and alpha is not None and u <= alpha:
                graphviz.append("%d->%d [label=\" %.2f%s \", fontcolor=\"black\"];" % \
                                    (best_child, this, best_u, "*" if tried < len(transitions) else ""))
                return (best_trans, best_u, this)
            if use_alphabeta and min_or_max == "max" and beta is not None and u >= beta:
                graphviz.append("%d->%d [label=\" %.2f%s \", fontcolor=\"black\"];" % \
                                    (best_child, this, best_u, "*" if tried < len(transitions) else ""))
                return (best_trans, best_u, this)
            if use_alphabeta and min_or_max == "min" and (beta is None or u < beta):
                beta = u
                graphviz.append("%d->%d [label=\" &beta;=%.2f \", fontcolor=\"black\"];" % \
                                    (child, this, u))
            if use_alphabeta and min_or_max == "max" and (alpha is None or u > alpha):
                alpha = u
                graphviz.append("%d->%d [label=\" &alpha;=%.2f \", fontcolor=\"black\"];" % \
                                    (child, this, u))
        if not use_alphabeta:
            graphviz.append("%d->%d [label=\" %s=%.2f \", fontcolor=\"black\"];" % \
                                (best_child, this, min_or_max, best_u))
        return (best_trans, best_u, this)

checked = 0

def minimax(state, player, possible_transitions, is_terminal, utility, switch_player,
            alpha_beta = False, depth_limit = None, estimate_utility = None, depth = 1,
            initial_player = None, minimizing = False, alpha = None, beta = None):
    global checked
    if depth == 1:
        checked = 0
        initial_player = player
    checked += 1
    best_trans = None
    best_u = None

    transitions = possible_transitions(state, player, depth, minimizing)
    # Find the transition (move) that provides the maximum
    # utility, assuming the opponent also makes a best move
    for trans, nextstate in transitions:
        # if the current state is a win/loss/tie, stop searching
        if is_terminal(nextstate):
            u = utility(nextstate, initial_player, depth)
        elif depth_limit is not None and depth >= depth_limit:
            return estimate_utility(nextstate, initial_player, depth)
        else:
            # after making our move, find the best move the
            # opponent can make (best for opponent = worse for us;
            # if we consider the opponent winning as negative
            # utility, we want to find the minimum utility move
            # of the opponent's possible moves)
            u = minimax(nextstate, switch_player(player), possible_transitions,
                        is_terminal, utility, switch_player,
                        alpha_beta, depth_limit, estimate_utility, depth+1,
                        initial_player, not minimizing, alpha, beta)
        if best_u is None or (minimizing and u < best_u) or (not minimizing and u > best_u):
            best_trans = trans
            best_u = u
        if alpha_beta:
            if minimizing:
                # if the utility we just found is smaller than alpha, and
                # these utilities can only get smaller (because we're in a
                # min stage), then there is no reason to check further
                if alpha is not None and u <= alpha:
                    break
                # if the utility we just found (from the max stage) is
                # smaller than beta, we found a new smallest max; this
                # will restrict future searches not to look further if
                # they are maximizing and they find a utility greater than
                # beta
                if beta is None or u < beta:
                    beta = u
            else:
                # if the utility we just found is greater than beta, and these
                # utilities can only get bigger (because we're in a max
                # stage), then there is no reason to check further
                if beta is not None and u >= beta:
                    break
                # if the utility we just found (from the min stage) is
                # greater than alpha, we found a new greatest min; this
                # will restrict future searches not to look further if
                # they are minimizing and they find a utility less than
                # alpha
                if alpha is None or u > alpha:
                    alpha = u
    if depth == 1:
        return best_trans
    else:
        return best_u

