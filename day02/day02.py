from enum import Enum

# Enums used to map the characters to their corresponding values, as described
# in the exercise.
class ActionABC(Enum):
    A = 0
    B = 1
    C = 2

class ActionXYZ(Enum):
    X = 0
    Y = 1
    Z = 2

class ResultsXYZ(Enum):
    X = -1
    Y = 0
    Z = 1

#1 first player wins
#0 draw
#-1 second player wins
results_table = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]
results_table_transposed = [[0, 1, -1], [-1, 0, 1], [1, -1, 0]]

def first_part(input_file):
    scores = []
    for line in input_file:
        current_score = 0
        line_split = line.rstrip().split(" ")
        first_action  = ActionABC[line_split[0]].value
        second_action = ActionXYZ[line_split[1]].value
        current_score = second_action + 1 
        # Our enum values are downshifted by 1 so they index into the results 
        # table, which of course is 0 index based. For the calculation of the 
        # score we therefore have to add 1 here. This is the only place 
        # we have to do this!
        
        # Lookup the result of the game, note that we use the transpose of the 
        # results table, this is due to the fact that __we__ are the second player
        # and not the first player.
        game_result = results_table_transposed[first_action][second_action]
        if(game_result == 0): # if its a draw
            current_score += 3
        if(game_result == 1): # if we win
            current_score += 6
        scores.append(current_score)
    return sum(scores)

def second_part(input_file):
    scores = []
    for line in input_file:
        current_score = 0
        line_split = line.rstrip().split(" ")
        first_action  = ActionABC[line_split[0]].value
        wanted_result = ResultsXYZ[line_split[1]].value 
        # note that here X, Y, Z represent different values, 
        # namely win loss or draw, ie 1, -1 or 0.   

        # now we lookup the action we need to take in order to get the wanted_result, 
        # given that the first player has taken his action. Again, since __we__ are
        # the second player, we have to use the transposed results matrix.
        needed_action = results_table_transposed[first_action].index(wanted_result)
        current_score = needed_action + 1 
        # note that we have to add 1 here, since we are 0 index based in the lookup 

        if(wanted_result == 0): 
            current_score += 3
        if(wanted_result == 1):
            current_score += 6
        scores.append(current_score)
    return sum(scores)

input_file_name = "day02.txt"

with open(input_file_name) as input_file:
    result_first = first_part(input_file)
    print("Result of the first part is: {}".format(result_first))

with open(input_file_name) as input_file:
    result_second = second_part(input_file)
    print("Result of the second part is: {}".format(result_second))
