#!/usr/bin/env python3

##################################################################
#                                                                #
# © 2021 - MPL 2.0 - Rsge, ColonelRoyMustang - v2.1.1            #
# https://github.com/Rsge/Tabletop-RPG-Dice-Roll-Odds-Calculator #
#                                                                #
##################################################################


# Imports
from functools import lru_cache
import matplotlib.pyplot as plt

# String constants
NON_NUMERIC_INPUT_WARNING = "Please input only positive integers!"
IMPOSSIBLE_INPUT_WARNING = "This sum isn't possible with your specified roll."
GIVEN_ROLL_INFO = "The probability of your throw using {}d{} was {} %\n"
BEST_ROLL_INFO = "The most probable roll{} with a probability of {} %"
SINGLE_ROLL = " was a {}"
MULTIPLE_ROLLS = "s were a {} or {}"
PLOT_TITLE =  "Dice sum probabilities"
PLOT_XLABEL = "Dice sum\n\n"
PLOT_YLABEL = "Probability / %"


while True:
    # Determine input.
    print("----------------------------------------------------\n"
          "Welcome to the ndm dice sums propability calculator.\n"
          "This shows you the probability for your dice roll,\n"
          "the most probable one(s) and plots all probabilites.\n"
          "Please make sure to only input integers.\n"
          "----------------------------------------------------\n")
    while True:
        rolls = input("How many rolls? ")
        if rolls.isdigit():
            rolls = int(rolls)
            if rolls > 0:
                break
        print(NON_NUMERIC_INPUT_WARNING)
    while True:
        sides = input("How many sides? ")
        if sides.isdigit():
            sides = int(sides)
            if sides > 0:
                break
        print(NON_NUMERIC_INPUT_WARNING)
    while True:
        playersum = input("What is your sum? ")
        if playersum.isdigit():
            playersum = int(playersum)
            if playersum >= rolls and playersum <= sides * rolls:
                break
            print(IMPOSSIBLE_INPUT_WARNING)
        else:
            print(NON_NUMERIC_INPUT_WARNING)

    print("\n\n\n")
    # Calculate functions.
    @lru_cache(None)
    def sum_freq(total, rolls, faces):
        if not rolls:
            return not total
        return sum(sum_freq(total - die, rolls - 1, faces) for die in range(1, faces + 1))

    def probability_calculator(roll_total, num_of_rolls, dice_faces):
        return sum_freq(roll_total, num_of_rolls, dice_faces) / dice_faces ** num_of_rolls

    # Prepare plot data.
    sums = []
    probabilities = []
    for i in range(rolls, rolls * sides + 1):
        sums.append(i)
        probabilities.append(round(probability_calculator(i, rolls, sides) * 100, 6))
    info_str = GIVEN_ROLL_INFO.format(rolls, sides, probabilities[playersum - rolls])

    # Find maximum/a.
    maximum = max(probabilities)
    max_ind = probabilities.index(maximum)
    if probabilities[max_ind + 1] != maximum:
        info_str += BEST_ROLL_INFO.format(SINGLE_ROLL.format(sums[max_ind]), maximum)
    else:
        info_str += BEST_ROLL_INFO.format(MULTIPLE_ROLLS.format(sums[max_ind], sums[max_ind] + 1), maximum)

    # Plot.
    plt.title(PLOT_TITLE)
    plt.xlabel(PLOT_XLABEL + info_str)
    plt.ylabel(PLOT_YLABEL)
    #plt.text(sums[len(sums) - 1] / 2, probabilities[1], info_str, horizontalalignment='center') # For putting info_str in the graph itself.
    plt.plot(sums, probabilities, "r+")
    plt.vlines(playersum, 0, maximum)
    plt.tight_layout()
    plt.show()
