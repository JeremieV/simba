 # Simba Documentation

Simba is a Clojure-like, interpreted programming language that easily interoperates with all Python libraries.
Features:
- multimethods
- persistent immutable data structures via Pyrsistent
- easy interoperability
- macros
- Clojure-like standard library based on similar abstractions
- named arguments

## Install
You can use Simba from the command line by calling `src/simba.py` from the main directory.
You can execute some files with:
`src/simba.py <file-name> <eventual-other-file-names>*`; at which point the execution will always start in the main namespace.

## Build

From the root folder, run:
- `pip install -r requirements.txt`
- `python .simba`

## License

Copyright (c) Rich Hickey. All rights reserved. The use and distribution terms for this software are covered by the Eclipse Public License 1.0 (http://opensource.org/licenses/eclipse-1.0.php) which can be found in the file epl-v10.html at the root of this distribution. By using this software in any fashion, you are agreeing to be bound by the terms of this license. You must not remove this notice, or any other, from this software.

<!-- Links
# https://python-ast-explorer.com/
# https://github.com/octoml/synr
 -->