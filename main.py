# -*- coding: utf-8 -*-
"""
Created on Fri Feb ? 15:58:34 2021
@author: Reuel R. D'silva

Main Script to run the LPP module
"""

# Imports
import argparse

import utils
from lpp import LPP


# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-i", "--inputfile", help = "Input File Name")
 
# Read arguments from command line
args = parser.parse_args()

if args.inputfile is None:
    print("Usage: python main.py -i input_filename")
else:
    for idx, lp in enumerate(utils.read_lp(args.inputfile)):
    
        print("Problem {}:".format(idx+1))
        print("==================================================")
    
        # Parse the Linear Programming Problem and Solve it
        lpp_obj = LPP(objective = lp[0], constraints = lp[1:])
        lpp_obj.solve()
    
        # Display the Results
        utils.display_result(lpp_obj)
        
        # Plot the Corner Points and the Feasible Region
        utils.plot(lpp_obj, title="LPP Problem {}".format(idx+1))
        print("\n\n\n\n")