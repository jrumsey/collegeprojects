
import sys
import random
import advsearch

def create_grid():
    # grid is 6x7 so we'll create a list of size 42
    return [' ' for _ in range(42)]

def print_grid(grid):
    s = ""
    s += "---------------\n"
    for i in range(6):
        for j in range(7):
            s += "|%c" % grid[i*7+j]
        s += "|\n"
    s += "---------------\n"
    s += " 0 1 2 3 4 5 6 \n\n"
    print s

def column_full(grid, col):
    return (grid[col] != ' ')

def add_to_column(grid, col, player):
    newgrid = grid[:]
    pos = -1
    for i in range(5,-1,-1):
        if(grid[i*7+col] == ' '):
            pos = i
            break
    if pos != -1:
        newgrid[pos*7+col] = player
    return newgrid

def win_horizontal(grid, player):
    for i in range(6):
        player_count = 0
        for j in range(7):
            if grid[i*7+j] == player:
                player_count += 1
                if player_count == 4:
                    return True
            else:
                player_count = 0
    return False

def win_vertical(grid, player):
    for j in range(7):
        player_count = 0
        for i in range(6):
            if grid[i*7+j] == player:
                player_count += 1
                if player_count == 4:
                    return True
            else:
                player_count = 0
    return False

def win_downleft(grid, player):
    for i in range(6):
        for j in range(7):
            player_count = 0
            for (ii,jj) in zip(range(i, 6), range(j, -1, -1)):
                if grid[ii*7+jj] == player:
                    player_count += 1
                    if player_count == 4:
                        return True
                else:
                    player_count = 0
    return False

def win_downright(grid, player):
    for i in range(6):
        for j in range(7):
            player_count = 0
            for (ii,jj) in zip(range(i, 6), range(j, 7)):
                if grid[ii*7+jj] == player:
                    player_count += 1
                    if player_count == 4:
                        return True
                else:
                    player_count = 0
    return False

def won(grid, player):
    return (win_vertical(grid, player) or win_horizontal(grid, player) or \
                win_downleft(grid, player) or win_downright(grid, player))

def is_terminal(grid):
    free_moves = False
    for i in range(7):
        if not column_full(grid, i):
            free_moves = True
            break
    return (won(grid, 'A') or won(grid, 'B') or not free_moves)

def switch_player(player):
    if player == 'A':
        return 'B'
    else:
        return 'A'

def estimate_utility(grid, player, depth):
    return 1.0 

# TODO
def estimate_utility_improved(grid, player, depth):
    cur_util = utility(grid, player, depth)
    if(depth > 1):
	depth = depth - 1
    parent_util = utility(grid, player, depth)
    if(parent_util > cur_util):
	return 0
    else:
	return 1.0 

#    return estimate_utility(grid, player, depth)

def utility(grid, player, depth):
    if won(grid, player):
        return 1.0
    elif won(grid, switch_player(player)):
        return -1.0
    else:
        return 0.0

# TODO
def utility_improved(grid, player, depth):
   if won(grid, player):
	return 1.0 / depth
   elif won(grid, switch_player(player)):
	return -1.0 / depth
   else:
	return 0.0 

#    return utility(grid, player, depth)

def possible_transitions(grid, player, depth, minimizing):
    moves = []
    for i in range(7):
        if not column_full(grid, i):
            moves.append((i, add_to_column(grid, i, player)))
    random.shuffle(moves)
    return moves

# TODO
# note: minimizing parameter is True or False
def possible_transitions_improved(grid, player, depth, minimizing):
   moves = []
   for i in range(7):
	if not column_full(grid, i):
	   moves.append((i, add_to_column(grid, i, player)))
	if estimate_utility_improved(grid, player, depth) < utility_improved(grid, player, depth):
	  del moves[(i, add_to_column(grid, i, player))]
   random.shuffle(moves)
	
#	if not minimizing:
#	    if estimate_utility_improved(grid, player, depth) > utility_improved(grid, player, depth):
#  		del moves[i]
		
#		else:
#		if estimate_utility_improved(grid, player, depth) > utility_improved(grid, player, depth):
#		    if moves[i] != ' ':
#			 moves.append((i, add_to_column(grid, i, player)))		   
   return moves		
	
#   return possible_transitions(grid, player, depth, minimizing)

def random_initial_state(n):
    grid = create_grid()
    # perform n random moves (each player gets n moves)
    for i in range(n):
        trans = possible_transitions(grid, 'A', 1, False)
        (_, grid) = random.choice(trans)
        trans = possible_transitions(grid, 'B', 1, False)
        (_, grid) = random.choice(trans)
    return grid

def experiment():
    print "moves, depth, minimax, alphabeta, pct_improvement"
    for i in range(20):
        for n in range(11):
            for d in range(1,7):
                if d == 0: depth_limit = None
                else: depth_limit = d
                grid = random_initial_state(n)
                advsearch.minimax(grid, 'A', possible_transitions, is_terminal, utility,
                                  switch_player, False, depth_limit, estimate_utility)
                nonab_checked = advsearch.checked
                advsearch.minimax(grid, 'A', possible_transitions, is_terminal, utility,
                                  switch_player, True, depth_limit, estimate_utility)
                ab_checked = advsearch.checked
                pct_improved = 100.0*float(nonab_checked-ab_checked)/float(nonab_checked)
                print "%d, %d, %d, %d, %.2f" % (n, d, nonab_checked, ab_checked, pct_improved)
                sys.stdout.flush()

def experiment_improved():
    print "moves, improved_won, alphabeta, improved, pct_improvement, firstmove"
    for i in range(30):
        for n in range(6):
            depth_limit = 3
            grid = random_initial_state(n)
            if is_terminal(grid): continue # skip games with winning starting states

            # play until end-game from this random initial state;
            # determine if original or improved strategy won and
            # measure strategy's checked states;
            # note, need to randomize who goes first
            ab_checked = 0
            imp_checked = 0
            goes_first = random.choice(["ab", "imp"])
            while (not is_terminal(grid)):
                if goes_first == "ab":
                    col = advsearch.minimax(grid, 'A', possible_transitions, is_terminal, utility,
                                            switch_player, True, depth_limit, estimate_utility)
                    ab_checked += advsearch.checked
                else:
                    col = advsearch.minimax(grid, 'A', possible_transitions_improved, is_terminal, utility_improved,
                                            switch_player, True, depth_limit, estimate_utility_improved)
                    imp_checked += advsearch.checked
	        grid = add_to_column(grid, col, 'A')
                if is_terminal(grid): break
                if goes_first == "ab":
                    col = advsearch.minimax(grid, 'B', possible_transitions_improved, is_terminal, utility_improved,
                                            switch_player, True, depth_limit, estimate_utility_improved)
                    imp_checked += advsearch.checked
                else:
                    col = advsearch.minimax(grid, 'B', possible_transitions_improved, is_terminal, utility_improved,
                                            switch_player, True, depth_limit, estimate_utility_improved)
                    ab_checked += advsearch.checked
                grid = add_to_column(grid, col, 'B')

            if ab_checked == 0 or imp_checked == 0:
                continue # skip cases where a single move won the game

            # did improved strategy win?
            if goes_first == "ab":
                if won(grid, 'A'):
                    won_imp = 0
                else:
                    won_imp = 1
            else:
                if won(grid, 'B'):
                    won_imp = 0
                else:
                    won_imp = 1                    
            pct_improved = 100.0*float(ab_checked-imp_checked)/float(ab_checked)
            print "%d, %d, %d, %d, %.2f, %s" % (n, won_imp, ab_checked, imp_checked, pct_improved, goes_first)
            sys.stdout.flush()

def game_loop():
    grid = create_grid()
    player = 'A'
    while (not is_terminal(grid)):
        print_grid(grid)
        if player == 'A':
            print "Searching..."
            col = advsearch.minimax(grid, 'A', possible_transitions_improved, is_terminal,
                                    utility_improved, switch_player, True, 4, estimate_utility_improved)
            print "I choose %d\n\n" % col
            grid = add_to_column(grid, col, player)
        else:
            col = input("Player %c, which column (0-6)? " % player)
            if column_full(grid, col):
                print "\n\nCan't, column full.\n\n"
                continue
            else:
                grid = add_to_column(grid, col, player)
        player = switch_player(player)

    print_grid(grid)
    if won(grid, 'A'):
        print "Player A wins!!"
    elif won(grid, 'B'):
        print "Player B wins!!"

#game_loop()
experiment_improved()

