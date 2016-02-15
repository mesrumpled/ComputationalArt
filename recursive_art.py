""" 
Software Design 2016 at Olin College of Engineering.

Generates computational art using random recurvive functions.

@author: March Saper 


"""

import random
from PIL import Image
from math import *


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    first_choices = ["prod", "avg", "cos_pi", "sin_pi", "sqr", "cube"]
    middle_choices = ["prod", "avg", "cos_pi", "sin_pi", "sqr", "cube", "x", "y"]
    last_choices = ["x", "y"]


    if min_depth > 0:
        chosen_function = random.choice(first_choices)
    elif max_depth > 0:
        chosen_function = random.choice(middle_choices)
    else:
        chosen_function = random.choice(last_choices)


    min_depth = min_depth - 1
    max_depth = max_depth - 1


    if chosen_function in ["prod", "avg"]:
        first_argument = build_random_function(min_depth, max_depth)
        second_argument = build_random_function(min_depth, max_depth)
        return [chosen_function, first_argument, second_argument]

    elif chosen_function in ["cos_pi", "sin_pi", "sqr", "cube"]:
        argument = build_random_function(min_depth, max_depth)
        return [chosen_function, argument]

    else:
        return [chosen_function]



def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    if f[0] == "x":
        return x
    if f[0] == "y":
        return y
    if f[0] == "prod":
        a = evaluate_random_function(f[1], x, y)
        b = evaluate_random_function(f[2], x, y)
        return a * b
    if f[0] == "avg":
        a = evaluate_random_function(f[1], x, y)
        b = evaluate_random_function(f[2], x, y)
        return 0.5 * (a + b)
    if f[0] == "cos_pi":
        a = evaluate_random_function(f[1], x, y)
        return cos(pi * a)
    if f[0] == "sin_pi":
        a = evaluate_random_function(f[1], x, y)
        return sin(pi * a)
    if f[0] == "sqr":
        a = evaluate_random_function(f[1], x, y)
        return a ** 2
    if f[0] == "cube":
        a = evaluate_random_function(f[1], x, y)
        return a ** 3
    
# print evaluate_random_function(build_random_function(5, 7), 1, 1)

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
        >>> remap_interval(3, 0, 4, 0, 12)
        9.0
    """
    value = float(val)
    input_start = float(input_interval_start)
    input_end = float(input_interval_end)
    output_start = float(output_interval_start)
    output_end = float(output_interval_end)
    
    fraction = (input_end - value)/(input_end - input_start)
    new_value = output_end - fraction * (output_end - output_start) 

    return new_value



def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    generate_art("myart3.png")