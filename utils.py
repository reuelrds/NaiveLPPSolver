# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 13:16:30 2021
@author: Reuel R. D'silva

A set of Utility functions to help aid the LPP module
"""

# Import required pacakges
import re
import string

import numpy as np
import matplotlib.pyplot as plt

from tabulate import tabulate
from scipy.spatial import ConvexHull


def read_lp(input_filename = "input.txt"):
    """Read The LPP from the input text file

    read_lp is a Generator Function that reads a text file
    and yields one single LPP.

    The Yield is triggered when it encounters a blank line.
    It ignores the Comments, which are lines starting with a # sign.


    Parameters
    ----------
    input_filename : str, optional
        The Input file Name. The default is "input.txt".

    Yields
    ------
    lp_lines : list
        Yields a LPP as a list of strings.

    """
    with open(input_filename, "r", encoding="utf8") as input_file:

        lp_lines = []
        for line in input_file:

            # Remove the leading and the trailing whiteshapces
            line = line.strip()

            # We can test if line is None as the strip() function
            # returns None it the line is empty
            if not line:
                
                # Yield the LP to the main function to parse and solve
                yield lp_lines
                lp_lines = []

            # Ignore Subject to and Comments 
            elif line[:7] == "Subject" or line[0] == "#":
                continue

            # Else append the line to the current LP
            elif line != "":
                lp_lines.append(line)
                
        # This else loop runs when the for loop exits successfully.
        # It is used to yield last LP which is not yielded by the first
        # yield if there is no empty line at the end of the file.
        else:
            if len(lp_lines) != 0:
                yield lp_lines


def parse_equation(equation_string):
    """Parse an function

    This function parses the coefficients and variables from a funtion
    that is represented as a string using Regular Expressions.

    Parameters
    ----------
    equation_string : str
        function represented as a string.

    Returns
    -------
    c : list
        list of coeffieients as integers.
    X : list
        list of variables as strings.

    """
    
    # A regular Expression to group coefficient and variable
    # eg: 5x_1: 
    #       first group 5, second group x_1.
    pattern = r"([-+]{0,1}\d*)([\w\d]+)"

    # Use findall to find all pairs of variables and coeffieients
    match = re.findall(pattern, equation_string)

    X = []
    c = []

    for pair in match:
        X.append(pair[1])

        # Takes care of case like -x_1 (no coefficient present)
        if pair[0] == "-":
            c.append(-1)
        
        # takes care of case like x_1 or +x_1 (coefficient is implied to be 1)
        elif pair[0] == "" or pair[0] == "+":
            c.append(1)
        else:
            c.append(int(pair[0]))

    return c, X


def display_result(lpp):
    """Print the Solution of the LPP to the console window.
    Uses tabulate to create pretty tables to print the intersection
    and corner points.
    
    Parameters
    ----------
    lpp : Object of type LPP
        An LPP Object with its solve method already called.
    """

    print("\n{}: {} = {}".format(lpp.problem_type.capitalize(), lpp.obj_var, lpp.obj_fn))
    print("Subject to:")
    for constraint in lpp.constraints:
        print("\t{}".format(constraint.constraint_str))

    # Print Intersection Points
    print("\nIntersection Points")
    table = tabulate(lpp.intersection_points, lpp.X, tablefmt="pretty")
    print(table)

    # Print Corner Points
    print("\nCorner Points")
    data = []
    data_headers = lpp.X.copy()
    data_headers.append("z")
    
    for point, value in zip(lpp.corner_points, lpp.z_values):
        point = point.tolist()
        point.append(value)
        data.append(point)
    
    # table = tabulate([lpp.corner_points, lpp.z_values], [lpp.X, "z"], tablefmt="pretty")
    table = tabulate(data, data_headers, tablefmt="pretty")
    print(table)
    
    
    # Print Solution
    if lpp.sol_point is not None:
        print("\nThe above LP is optimized at: ")
        for idx, var in enumerate(lpp.X):
            print("\t{:} = {:.2f}".format(var, lpp.sol_point[idx].item()))

        print("With Optimal Solution: z = {}".format(lpp.z))
    else:
        print("The above LP does not have a Fesiable Solution")


def plot(lpp, title=""):
    """Plot the LPP.

    The Plot method only plots the LPP which has two variabless

    Parameters
    ----------
    lpp : Object of type LPP
        An LPP Object with its solve method already called.

    """

    # Plot only if the LPP has two variables and a Solution
    if lpp.sol_point is None or len(lpp.X) != 2:
        return

    # Using ConvexHull gurantees the points to be in
    # Anti-clockwise order. This helps matplotlib to print the
    # points in the correct order to get a polygon

    points = np.array(lpp.corner_points).squeeze()
    hull = ConvexHull(points)

    points_plot = points[hull.vertices.astype(int), :]
    x, y = points_plot[:, 0], points_plot[:, 1]
    plt.figure(figsize=(8, 8))
    plt.axis('equal')
    plt.fill(x, y, hatch="\\", alpha=0.5)
    plt.plot(x, y, "bo")
    
    # Add Grid to the plot
    plt.grid(True)
    
    # Add horizontal and vertical axis
    plt.axhline(0, color="black")
    plt.axvline(0, color="black")
    
    
    # Add Markers to the points that were plotted
    for point, marker in zip(points_plot, string.ascii_uppercase[:len(points_plot)]):
        label = f"{marker} ({point[0]:.1f}, {point[1]:.1f})"
        plt.text(
            point[0],
            point[1],
            label,
            label=label,
            fontsize="medium",
            position=(point[0]+0.2, point[1]+0.2)
        )

    # Plot constraint lines
    axes = plt.gca()
    for constraint in lpp.constraints:
        slope, intercept = constraint.slope(), constraint.intercept()

        if slope is not None and intercept is not None:
            x_vals = np.array(axes.get_xlim())
            y_vals = intercept + slope * x_vals
            plt.plot(x_vals, y_vals, label = constraint.constraint_str)

    # Add title, display legend and show the plot
    plt.title(title)
    plt.legend()
    plt.show()
