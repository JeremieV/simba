# Simba Documentation

## Pieces

- A **reader** is a procedure that reads a file and returns a Simba data structure.
  - the reader must ignore the (YAML) front matter at the top of the file]
  - this is used by the interpreter to select the correct reader and some other settings
- A **writer** is a procedure that outputs a text stream from an input Simba data structure.
- The interpreter evaluates Simba data structures.
- **interpreter plugins**

## Changelog

2 Nov 2021:
- created repository and REPL structure