# Overview

The goal of this library is to create a more useful debugging tool than the built-in function `dir`. The core issues this library addresses are:

1. Inclusion of dunder methods that are very rarely useful
2. No differentiation between attributes/methods
3. No docstring display
4. No grouping of similar functionality together, only alphabetical sorting

This library takes the output of `dir` and runs the following steps:

1. Groups the attributes and methods by the class they are defined by
2. Identifies if it is a dunder method, normal method, or attribute
3. Pulls the summary of the docstring for the attribute/method, if it exists
4. Colorizes the output to visually differentiate the classes, attributes, methods, and dunder methods

## Demo

Running the code in [demo.py](https://github.com/douglassimonsen/ppdir/blob/main/demo.py), you can see the difference between the built-in `dir` and `ppdir` here:

Before:

![before](https://raw.githubusercontent.com/douglassimonsen/ppdir/refs/heads/main/example_images/before.png)

After:

![after](https://raw.githubusercontent.com/douglassimonsen/ppdir/refs/heads/main/example_images/after.png)


# Dev Instructions


## Set Up

```shell
python -m venv venv
venv\Scripts\activate
python -m pip install .[dev]
```

## Build

```shell
python -m build .
```