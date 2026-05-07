from tokenizer import tokenize

def parse_factor(tokens):
    token = tokens[0]
    if token["tag"] == "number":
        return {"tag": "number", "value": token["value"]}, tokens[1:]
    if token["tag"] == "identifier":
        return {"tag": "identifier", "value": token["value"]}, tokens[1:]
    if token["tag"] == "true":
        return {"tag": "true"}, tokens[1:]
    if token["tag"] == "false":
        return {"tag": "false"}, tokens[1:]
    if token["tag"] == "function":
        return parse_function_expression(tokens)
    if token["tag"] == "(":
        node, tokens = parse_expression(tokens[1:])
        if tokens[0]["tag"] != ")":
            raise SyntaxError(f"Expected ')', got {tokens[0]}")
        return node, tokens[1:]
    raise SyntaxError(f"Expected factor, got {tokens[0]}")

def parse_complex_expression(tokens):
    ast, tokens = parse_factor(tokens)
    while tokens[0]["tag"] == "(":
        tokens = tokens[1:]
        arguments = []
        if tokens[0]["tag"] != ")":
            arg, tokens = parse_expression(tokens)
            arguments.append(arg)
            while tokens[0]["tag"] == ",":
                tokens = tokens[1:]
                arg, tokens = parse_expression(tokens)
                arguments.append(arg)
        if tokens[0]["tag"] != ")":
            raise SyntaxError(f"Expected ')' but got {tokens[0]}")
        tokens = tokens[1:]
        ast = {"tag": "call", "function": ast, "arguments": arguments}
    return ast, tokens

def parse_function_expression(tokens):
    tokens = tokens[1:] # consume 'function'
    if tokens[0]["tag"] != "(": raise SyntaxError("Expected (")
    tokens = tokens[1:]
    parameters = []
    if tokens[0]["tag"] != ")":
        parameters.append(tokens[0]["value"])
        tokens = tokens[1:]
        while tokens[0]["tag"] == ",":
            tokens = tokens[1:]; parameters.append(tokens[0]["value"]); tokens = tokens[1:]
    tokens = tokens[1:] # consume )
    tokens = tokens[1:] # consume {
    body, tokens = parse_statement_list(tokens)
    tokens = tokens[1:] # consume }
    return {"tag": "function", "parameters": parameters, "body": body}, tokens

def parse_unary(tokens):
    minus_count = 0
    while tokens[0]["tag"] == "-":
        minus_count += 1
        tokens = tokens[1:]
    node, tokens = parse_complex_expression(tokens)
    for _ in range(minus_count):
        node = {"tag": "unary-", "operand": node}
    return node, tokens

def parse_term(tokens):
    left, tokens = parse_unary(tokens)
    while tokens[0]["tag"] in ["*", "/"]:
        op = tokens[0]["tag"]
        right, tokens = parse_unary(tokens[1:])
        left = {"tag": op, "left": left, "right": right}
    return left, tokens

def parse_arithmetic_expression(tokens):
    left, tokens = parse_term(tokens)
    while tokens[0]["tag"] in ["+", "-"]:
        op = tokens[0]["tag"]
        right, tokens = parse_term(tokens[1:])
        left = {"tag": op, "left": left, "right": right}
    return left, tokens

def parse_comparison(tokens):
    left, tokens = parse_arithmetic_expression(tokens)
    if tokens[0]["tag"] in ["==", "!=", "<", "<=", ">", ">="]:
        op = tokens[0]["tag"]
        right, tokens = parse_arithmetic_expression(tokens[1:])
        left = {"tag": op, "left": left, "right": right}
    return left, tokens

def parse_logic_not(tokens):
    if tokens[0]["tag"] == "not":
        operand, tokens = parse_logic_not(tokens[1:])
        return {"tag": "not", "operand": operand}, tokens
    return parse_comparison(tokens)

def parse_logic_and(tokens):
    left, tokens = parse_logic_not(tokens)
    while tokens[0]["tag"] == "and":
        right, tokens = parse_logic_not(tokens[1:])
        left = {"tag": "and", "left": left, "right": right}
    return left, tokens

def parse_logic_or(tokens):
    left, tokens = parse_logic_and(tokens)
    while tokens[0]["tag"] == "or":
        right, tokens = parse_logic_and(tokens[1:])
        left = {"tag": "or", "left": left, "right": right}
    return left, tokens

def parse_expression(tokens):
    return parse_logic_or(tokens)

# --- STATEMENTS ---

def parse_print_statement(tokens):
    tokens = tokens[1:]
    ast, tokens = parse_expression(tokens)
    return {"tag": "print", "expression": ast}, tokens

def parse_assignment_statement(tokens):
    target = tokens[0]["value"]
    tokens = tokens[2:] # identifier and =
    ast, tokens = parse_expression(tokens)
    return {"tag": "assign", "target": target, "expression": ast}, tokens

def parse_if_statement(tokens):
    tokens = tokens[2:] # if and (
    cond, tokens = parse_expression(tokens)
    tokens = tokens[2:] # ) and {
    then_b, tokens = parse_statement_list(tokens)
    tokens = tokens[1:] # }
    ast = {"tag": "if", "condition": cond, "then_block": then_b}
    if tokens[0]["tag"] == "else":
        tokens = tokens[2:] # else and {
        else_b, tokens = parse_statement_list(tokens)
        tokens = tokens[1:] # }
        ast["else_block"] = else_b
    return ast, tokens

def parse_while_statement(tokens):
    tokens = tokens[2:] # while and (
    cond, tokens = parse_expression(tokens)
    tokens = tokens[2:] # ) and {
    body, tokens = parse_statement_list(tokens)
    tokens = tokens[1:] # }
    return {"tag": "while", "condition": cond, "do_block": body}, tokens

# ----------------------------------------
# Project - Added support for 'for' loops and function definitions
# -----------------------------------------
def parse_for_statement(tokens):
    tokens = tokens[1:] # for
    var_name = tokens[0]["value"]
    tokens = tokens[2:] # identifier and =
    start_expr, tokens = parse_expression(tokens)
    tokens = tokens[1:] # to
    end_expr, tokens = parse_expression(tokens)
    tokens = tokens[1:] # {
    body, tokens = parse_statement_list(tokens)
    tokens = tokens[1:] # }

    # Desugar 'for' loop into an equivalent 'while' loop with an initializer and an incrementer
    init = {"tag": "assign", "target": var_name, "expression": start_expr}
    cond = {"tag": "<=", "left": {"tag": "identifier", "value": var_name}, "right": end_expr}
    inc = {"tag": "assign", "target": var_name, "expression": {"tag": "+", "left": {"tag": "identifier", "value": var_name}, "right": {"tag": "number", "value": 1}}}
    body["statements"].append(inc)
    
    return {"tag": "statement_list", "statements": [init, {"tag": "while", "condition": cond, "do_block": body}]}, tokens

def parse_function_statement(tokens):
    name_token = tokens[1]
    # Desugar named function definition into an assignment of a function expression to an identifier
    new_tokens = [name_token, {"tag": "="}] + tokens[2:]
    return parse_assignment_statement(new_tokens)

def parse_statement(tokens):
    tag = tokens[0]["tag"]
    if tag == "print": return parse_print_statement(tokens)
    if tag == "if": return parse_if_statement(tokens)
    if tag == "while": return parse_while_statement(tokens)
    if tag == "for": return parse_for_statement(tokens) # New Branch for For Loop - Project
    if tag == "function": return parse_function_statement(tokens)
    if tag == "identifier": return parse_assignment_statement(tokens)
    raise SyntaxError(f"Unknown statement: {tokens[0]}")

def parse_statement_list(tokens):
    statements = []
    while tokens[0]["tag"] == ";": tokens = tokens[1:]
    if tokens[0]["tag"] in [None, "}"]:
        return {"tag": "statement_list", "statements": statements}, tokens
    
    s, tokens = parse_statement(tokens)
    statements.append(s)
    
    while tokens[0]["tag"] == ";":
        tokens = tokens[1:]
        if tokens[0]["tag"] in [None, "}"]: break
        s, tokens = parse_statement(tokens)
        statements.append(s)
    return {"tag": "statement_list", "statements": statements}, tokens

def parse(tokens):
    ast, tokens = parse_statement_list(tokens)
    return {"tag": "program", "statements": ast}