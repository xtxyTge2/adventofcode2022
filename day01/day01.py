def calculate_calories_of_all_elves():
    calories = []
    current_calories = 0
    with open("2022_python/day01/day01.txt") as f:
        for line in f:
            if len(line.strip()) == 0: # empty line check, includes whitespaces!
                calories.append(current_calories)
                current_calories = 0
            else:
                current_calories += int(line)
        calories.append(current_calories) # add last item, 
        # when at the end of the file
    return calories
    
def first_part():
    "Result of the first part is: 74198"
    calories = calculate_calories_of_all_elves()
    return max(calories)

def second_part():
    "Result of the second part is: 209914"
    calories = calculate_calories_of_all_elves()
    return sum(sorted(calories, reverse=True)[:3])


result_first = first_part()
print("Result of the first part is: {}".format(result_first))

result_second = second_part()
print("Result of the second part is: {}".format(result_second))
