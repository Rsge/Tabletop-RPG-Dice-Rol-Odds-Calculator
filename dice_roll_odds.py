#!/usr/bin/env python3

##################################################################
#                                                                #
# © 2021 - MPL 2.0 - Rsge, ColonelRoyMustang - v2.0.1            #
# https://github.com/Rsge/Tabletop-RPG-Dice-Roll-Odds-Calculator #
#                                                                #
##################################################################


# Imports
from functools import lru_cache
import matplotlib.pyplot as plt

while True:
    # Determining input
    print("----------------------------------------------------\n"
          "Welcome to the ndm dice sums propability calculator.\n"
          "This shows you the probability for your dice roll,\n"
          "the most probable one(s) and plots all probabilites.\n"
          "Please make sure to only input integers.\n"
          "----------------------------------------------------\n")
    while True:
        sides = input("How many sides? ")
        if sides.isdigit():
            sides = int(sides)
            if sides > 0:
                break
        print("Please input only positive integers!")
    while True:
        rolls = input("How many rolls? ")
        if rolls.isdigit():
            rolls = int(rolls)
            if rolls > 0:
                break
        print("Please input only positive integers!")
    while True:
        playersum = input("What is your sum? ")
        if playersum.isdigit():
            playersum = int(playersum)
            if playersum >= rolls and playersum <= sides * rolls:
                break
            print("This sum isn't possible with your specified roll.")
        else:
            print("Please input only integers!")

    print("\n\n\n")
    # Calculation functions
    @lru_cache(None)
    def sum_freq(total, rolls, faces):
        if not rolls:
            return not total
        return sum(sum_freq(total - die, rolls - 1, faces) for die in range(1, faces + 1))

    def probability_calculator(roll_total, num_of_rolls, dice_faces):
        return sum_freq(roll_total, num_of_rolls, dice_faces) / dice_faces ** num_of_rolls

    # Preparing plot data
    sums = []
    probabilities = []
    for i in range(rolls, rolls * sides + 1):
        sums.append(i)
        probabilities.append(round(probability_calculator(i, rolls, sides) * 100, 6))
    info_str = "The probability of your throw was {} %\n".format(probabilities[playersum - rolls])

    # Finding maximum/a
    maximum = max(probabilities)
    max_ind = probabilities.index(maximum)
    if probabilities[max_ind + 1] != maximum:
        info_str += "The highest probability is rolling a {} with a probability of {} %".format(sums[max_ind], maximum)
    else:
        info_str += "The highest probabilities are for rolling a {} or {} with a probability of {} %".format(sums[max_ind], sums[max_ind] + 1, maximum)

    # Plotting
    plt.title("Dice sum probabilities")
    plt.xlabel("Dice sum\n\n" + info_str)
    plt.ylabel("Probability / %")
    #plt.text(sums[len(sums) - 1] / 2, probabilities[1], info_str, horizontalalignment='center') # For putting it in the graph itself
    plt.plot(sums, probabilities, "r+")
    plt.vlines(playersum, 0, maximum)
    plt.tight_layout()
    plt.show()
