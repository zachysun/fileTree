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
python tree.py --if-merge --merge-type pdf
```

### Parameters:

```
python tree.py --help
---
usage: tree.py [-h] [--directory DIRECTORY] [--if-merge] [--merge-type {txt,pdf}] [--n N] [--ignore [IGNORE ...]] [--specific-ext [SPECIFIC_EXT ...]] [--nonspecific-ext [NONSPECIFIC_EXT ...]] [--max-depth MAX_DEPTH]
```
