# dirs_compare
Compare two directories or files

To get help run
```
usage: python3 cmp.py [-h] -p1 PATH1 -p2 PATH2 [-m {directories,files}] [-sc] [-hd] [-l | -r]
options:
  -h, --help            show this help message and exit
  -p1 PATH1, --path1 PATH1, --left-path PATH1
                        Path to first (left) directory or file
  -p2 PATH2, --path2 PATH2, --right-path PATH2
                        Path to second (right) directory or file
  -m {directories,files}, --mode {directories,files}
                        Compare directories or files
  -sc, --show-common    Show common files
  -hd, --hide-diff      Hide different files
  -l, --left-only       Show left only difference
  -r, --right-only      Show right only difference
```