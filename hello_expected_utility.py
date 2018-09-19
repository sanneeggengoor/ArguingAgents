# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 11:29:55 2018

@author: soenk
"""

# Function to calculate expected utility of an action(in this case, restaurant)
def expected_utility(p, v):
    exp_u = 0
    for i in range(len(p)):
        exp_u += p[i] * v[i]
    return exp_u

# Probability list of the expensive restaurant, action 1
p_thelibrije = [
        0.05, # Probability of a low bill
        0.9   # Probability of high quality food
        ]

p_febo = [
        0.86,
        0.2 
        ]

# Value list of the agents

v_wa_van_buren = [
        0.01,  # Importance of low bill
        0.95   # Importance of high quality food
        ]

v_tokkie = [
        0.9,
        0.1
        ]

# Calculating expected utility for both agents

eu_wa_lib = expected_utility(p_thelibrije,v_wa_van_buren)
eu_wa_feb = expected_utility(p_febo,v_wa_van_buren)
eu_tok_lib = expected_utility(p_thelibrije,v_tokkie)
eu_tok_feb = expected_utility(p_febo,v_tokkie)

print("WA has an Expected Utility for de Librije of: " + str(eu_wa_lib) + 
      " and an Expected Utility for Febo of: " + str(eu_wa_feb) + ".")

print("Tokkie has an Expected Utility for de Librije of: " + str(eu_tok_lib) + 
      " and an Expected Utility for Febo of: " + str(eu_tok_feb) + ".")