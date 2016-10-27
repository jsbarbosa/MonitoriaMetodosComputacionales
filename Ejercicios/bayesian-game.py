import time
import numpy as np
from numpy.random import rand

N = int(1e6)
random = rand(N, 12)
lines = random[:,0]


def with_loops():
    """
    Method that uses loops to solve the task
    """
    first_condition = random[:,1:9]     # first condition happens within the first 8 numbers
    last_condition = random[:,9:]   # last condition happens within the last 3 numbers
    bob_3 = 0.0
    bob_wins = 0.0
    for (i, value) in enumerate(lines):
        temp = first_condition[i] < value   # boolean array
        temp = first_condition[i, temp]     # positions at which temp is True
        if len(temp) == 3:
            bob_3 += 1
            if all(last_condition[i] < value):  # checks that all 3 remaning numbers are for bob
                bob_wins += 1
                
    return bob_wins/bob_3


def with_masks():
    """
    Method that uses masks to solve the task
    """
    first_condition = random[:, 1:]     # conditions are threated as one
    comparator = np.einsum('ij,i->ij', np.ones_like(first_condition), lines) # makes an array of the same shape of first_conditions containing the position of the line

    bool_mask = first_condition < comparator    # generates a mask
    bob_numbers = np.sum(bool_mask[:, :8], axis=1)  # checks the number of times bob wins withing the first 8 games
    bob_3 = np.where(bob_numbers == 3)[0]   # position (in array) where bob has won 3 times

    end_numbers = np.sum(bool_mask[bob_3, 8:], axis=-1)     # gets the number of remaining bob scores, at the games in which bob had 3 wins already
    bob_wins = np.where(end_numbers == 3)[0]    # position in which all last scores are for bob
    
    return float(len(bob_wins))/len(bob_3)


names = {'masks': with_masks, 'loops': with_loops}
for name in names:    
    init = time.perf_counter()
    ratio = names[name]()
    end = time.perf_counter()
    
    print("With %s P = %.6f and time = %.4fs"%(name, ratio, end-init))

