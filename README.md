# GridPuzzles
Python project for programming book

Text for the book for this project is located here: https://docs.google.com/document/d/13-bG9_2Dcl3PHeKNWAaYTmCeLY4aH8liWOVOP9fXglw/edit?usp=sharing

This program uses external modules. For them to work they need to be installed in the 
python version used. To do this:

```shell
> pip install termcolor
```
TODO:

* Explain how to run program
* Explain how to control logging (turn on debug logging in particular)

## Logging

To turn on logging you'll need a line like this:

```python
logging.basicConfig(format='%(message)s', filename='grid-puzzle.log', filemode='w', level=logging.DEBUG)
```

That will write logging messages to a file. To see them in the console use:

```python
logging.basicConfig(format='%(message)s',level=logging.DEBUG)
```

Only the first call to *basicConfig* will do anything. All others are silently ignored.