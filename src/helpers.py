def read_files(reader, files):
    """Opens, reads, and closes the files in order.
    Returns a Simba Symbolic Expression."""
    ast_list = []
    for file in files:
        with open(file, 'r') as f:
            program = f.read()
            readerObj = reader.SexpReader(program)
            while readerObj.position < len(readerObj.tokens):
                e = readerObj.read_form()
                # print(e)
                ast_list.append(e)
    return ast_list

def read_files_form_by_form(reader, procedure, files):
    """Same as read_files except that it reads the forms one by one and it can take a procedure to execute on each form.
    This function allows one to perform an operation on the data in one pass, unlike read_files.
    Furthermore, it is takes roughly 'constant' space where read_files takes linear space."""
    for file in files:
        with open(file, 'r') as f:
            program = f.read()
            readerObj = reader.SexpReader(program)
            while readerObj.position < len(readerObj.tokens):
                e = readerObj.read_form()
                # print(e)
                procedure(e)

def read_string_form_by_form(reader, procedure, string):
    """Similar to read_string_form_by_form, useful for the REPL."""
    readerObj = reader.SexpReader(string)
    while readerObj.position < len(readerObj.tokens):
        e = readerObj.read_form()
        # print(e)
        procedure(e)

def find_forms(startswith, ast_list):
    results = []
    for f in ast_list:
        if f.positional[:len(startswith)] == startswith:
            results.append(f)
    return results

def find_ns(name, ast_list):
    res = find_forms(["ns", name], ast_list)
    if len(res) > 1:
        raise Exception(f"There is more than one {name} namespace.")
    if len(res) == 0:
        raise Exception(f"No {name} namespace was found.")
    return res[0]