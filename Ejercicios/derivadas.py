# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 19:43:58 2016

@author: Juan
"""

# imports required modules
import matplotlib.pyplot as plt
import numpy as np

# sets the functions and their derivatives
functions = [np.cos, np.exp]        # example functions
derivatives = [np.sin, np.exp]      # exact derivatives, minus sign in sine will later be introduced
functions_labels = ["$\cos x$", "$e^x$"]        # LaTex representation of the functions

# sets the positions to be evaluated, differents widths and method used
positions = [0.1, 10, 100]
widths = [10**(-i) for i in range(1, 12)]
methods = ["Forward", "Central"]

def differentiation(method, function, position, width):
    """
        Method that calculates a derivative using central or forward differences formula.
    """
    def central(f, t, h):
        return (f(t+h/2.) - f(t-h/2.))/h
        
    def forward(f, t, h):
        return (f(t+h)-f(t))/h
        
    if method == "Forward":
        return forward(function, position, width)
        
    elif method == "Central":
        return central(function, position, width)

fig = plt.figure(figsize=(10, 5))      # creates figure
ax = fig.add_axes([0.1, 0.1, 0.55, 0.8])        # makes up enough space for legend
for method in methods:
    for (function, derivative, f_label) in zip(functions, derivatives, functions_labels):       # usefull to interate over various elements of different lists, arrays, tuples, etc
        for position in positions:
            log_error = []      # sets up a buffer to store values
            for width in widths:
                result = differentiation(method, function, position, width)     # calculates derivative
                exact = derivative(position)
                if f_label == "$\cos x$":       # includes minus sign of sine derivative
                    exact *= -1
                error = abs((result-exact)/exact)
                error = np.log10(error)
                log_error.append(error)     # stores the value
            
            text = method + " " + f_label + r", $x=" + str(position) + r"$"         # sets the text to be shown at the legend
            
            # plots different lines depending on the method used            
            if method == "Forward":
                style = "-"
            else:
                style = "--"
            ax.plot(np.log10(widths), log_error, style, label = text)       # makes the plot
            
# additional plot data            
ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
ax.set_xlabel("$\log_{10}h$")
ax.set_ylabel("$\log_{10}\epsilon$")
plt.grid()      # includes a grid
plt.show()      # shows the plot
