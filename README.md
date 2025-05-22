# fileTree
### Description:

A simple Python script: 

(1)Customizes to output the structure of project files. 

(2)Concatenates the code in the project files into one PDF document.

### Usage:

**Generate file structure:**

```cmd
python tree.py
```

**Generate file structure and code pdf file:**

```cmd
python tree.py --merge --output-type pdf
```

### Parameters:

```
python tree.py --help
---
usage: tree.py [-h] [--d DIRECTORY] [--merge] [--output-type {txt,pdf}]
[--n N] [--ignore [IGNORE ...]] [--specific-ext [SPECIFIC_EXT ...]]
[--nonspecific-ext [NONSPECIFIC_EXT ...]]
[--max-depth MAX_DEPTH]
```
