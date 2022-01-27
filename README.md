 # Simba Documentation

How to use Simba:
You can use Simba from the command line by calling `src/simba.py` from the main directory.
You can execute some files with:
`src/simba.py <file-name> <eventual-other-file-names>*`; at which point the execution will always start in the main namespace.

<!--
## Pieces

- A **reader** is a procedure that reads a file and returns a Simba data structure.
  - the reader must ignore the (YAML) front matter at the top of the file]
  - this is used by the interpreter to select the correct reader and some other settings
- A **writer** is a procedure that outputs a text stream from an input Simba data structure.
- The interpreter evaluates Simba data structures.
- **interpreter plugins**

## Data representation

- `doc` documentation is conserved as metadata in the running program. Equivalent of doc-strings. -> user-facing
- `comment`s are not, they are only meant for the person trying to understand the inner-workings of the code -> implementer-facing
- they should **be ignored by the compiler**
- md and stuff compile down to `e`s

## Changelog

2 Nov 2021:
- created repository and REPL structure

## Questions:

- How do I import stuff

## Roadmap

- evaluate vectors
- evaluate maps
- namespaces!!
- interop: I can wrap all of the irregular functions, however there are the library functions, and methods:
- [x] Minus `-` should throw an error when given only one arg -->