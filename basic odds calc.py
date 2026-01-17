import json
import numpy as np
from scipy.stats import norm # Fixed typo

values = '{"auto":35, "transition":10, "phase1" :50, "phase2": 0, "phase3": 53, "phase4": 0, "endgame" : 45}'
other_values = '{"auto":35, "transition":10, "phase1" :50, "phase2": 0, "phase3": 53, "phase4": 0, "endgame" : 45}'
def basic_odds(values, other_values):
    #if json loads json
    data = json.loads(values)
    data2 = json.loads(other_values)
    #calculations
    #ignores the keys makes the values into a list
    value_list = list(data.values())
    other_value_list = list(data2.values())
    #differnce between the array indexes ex: a[0] -b[0]
    diffs = np.array(value_list) - np.array(other_value_list)
    #calculates the mean and standard deviation
    mean_other_diff = np.mean(diffs)
    std_other_diff = np.std(diffs)
    #prints the stuff
    print(f"Mean: {mean_other_diff}")
    print(f"Standard Deviation: {std_other_diff}")
    #calculates the area under the curve to perdict probablility
    prob_3464 = norm.sf(0, loc=mean_other_diff, scale=std_other_diff)
    prob_3464_percentage = prob_3464*100
    print(f"Probability: {prob_3464_percentage}")
basic_odds(
    '{"auto":35, "transition":10, "phase1" :50, "phase2": 0, "phase3": 53, "phase4": 0, "endgame" : 45}',
    '{"auto":25, "transition":5, "phase1" :5, "phase2": 0, "phase3": 23, "phase4": 0, "endgame" : 25}'


)