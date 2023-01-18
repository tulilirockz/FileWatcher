WatchFile(s)
=========

A python-based console script for watching files and running 
utilities if they were modified.

- You can use it, for example, when you are making a program
or something and 
- Well, it is versatile, pretty sure you can find an use 
case for this eventually.

# Usage
```sh
SHELL_SCRIPT_STRING="echo hi!!! it worked"

wf -s "$SHELL_SCRIPT_STRING" FILE FILE2 FILE3 FILE4 # ...
```

# Installation

```sh
# You can either just copy this to a folder in your path with 
install ./wf.py ${PATHFOLDER:~/.local/bin}/wf
# Or you can also install it through poetry
poetry install .
```


- This was made for fun! I hope it will be useful for you 
somehow!
