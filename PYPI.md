# Overview

How often have you wished for a more well organized output from Python's built-in `dir` function when looking through a deeply nested [pydantic](https://pydantic-docs.helpmanual.io/) model after seeing page due to tens of private methods? Running `dir` on a [pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) produces a list of **443 entries**!

The goal of this library is to create a more useful debugging tool than the built-in function `dir(<class>)`. The issues with the built-in `dir(<class>)` addressed by this library are:

1. Inclusion of dunder methods that are very rarely useful
2. No differentiation between attributes/methods
3. No docstring display
4. No grouping of similar functionality together, only alphabetical sorting
5. No way to jump to the source code of the 

This library takes the output of `dir` and runs the following steps:

1. Groups the attributes and methods by the class they are defined by
   - Identifies the source code location of the class, allowing you to quickly jump to them for a deeper dive in IDEs like VS Code.
   - Prints the docstring summary of the class.
2. Identifies if it is a dunder method, non-dunder method, or attribute
   - Within non-dunder methods, adds a "ᶜ" or "ˢ" to indicate if it is a classmethod or staticmethod rather than a standard instance method.
3. Pulls the summary of the docstring for each attribute/method, if it exists
   - For attributes, there is no `__doc__` attribute, but we follow the convention of [PEP-258](https://www.python.org/dev/peps/pep-0258/) and most autocompletion tools of the next literal expression if it exists
4. Colorizes the output to visually differentiate the classes, attributes, methods, and dunder methods

## Limitations

Currently, this library only works with classes. For all other entities - functions, modules, etc - it falls back to the built-in `dir` implementation.

# Installation

You can install the library using pip:

```bash
pip install pretty-dir
```

## Auto-loading in PDB (Breakpoint)

[PDB](https://docs.python.org/3/library/pdb.html) is the built-in Python debugger that you can invoke with the `breakpoint()` function (or `import pdb; pdb.set_trace()` in Python versions before 3.7). To make `ppdir` automatically available in every PDB session, you can include it in a [PDB configuration file](https://docs.python.org/3/library/pdb.html#debugger-commands).

To make and add `ppdir` to your global PDB configuration, create a file named `~/.pdbrc` if it doesn't already exist, and add the following lines to it:

```python
from ppdir import ppdir, defaults
defaults(include_docs=True)  # remember to set your preferred defaults!
```

Now `ppdir` will be automatically available whenever you call `breakpoint()` in your code.

# Basic Usage Example

```python
from ppdir import ppdir

class BaseClass:
    base: int

class MyClass(BaseClass):
    a: int
    "example attr docstring"
    b: str

    def my_method(self):
        """This is my method."""
        pass

ppdir(MyClass)
```

# Demo

Running the code in [demo.py](https://github.com/douglassimonsen/ppdir/blob/main/demo.py), you should see the difference between the built-in `dir` and `ppdir` like the following images:

Before:

![before](https://raw.githubusercontent.com/douglassimonsen/ppdir/refs/heads/main/example_images/before.png)

After:

![after](https://raw.githubusercontent.com/douglassimonsen/ppdir/refs/heads/main/example_images/after.png)
