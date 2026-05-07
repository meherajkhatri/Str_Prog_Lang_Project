import re

patterns = [
    (r"\/\/.*", "whitespace"), # Added support for single-line comments that start with '//' and continue to the end of the line - Project
    (r"\s+", "whitespace"),
    (r"\d+", "number"),
    (r"==", "=="),
    (r"!=", "!="),
    (r"<=", "<="),
    (r">=", ">="),
    (r"\+", "+"),
    (r"\-", "-"),
    (r"\/", "/"),
    (r"\*", "*"),
    (r"\(", "("),
    (r"\)", ")"),
    (r"\{", "{"),
    (r"\}", "}"),
    (r"\,", ","),
    (r"\=", "="),
    (r"\;", ";"),
    (r"\<", "<"),
    (r"\>", ">"),
    (r"\&\&", "&&"),
    (r"\|\|", "||"),
    (r"\!", "!"),
    (r"\:", ":"),       # Added ':' token that is used in 'for' loops to separate the initializer, condition, and incrementer - Project
    (r"function\b", "function"),
    (r"return\b", "return"),
    (r"print\b", "print"),
    (r"true\b", "true"),
    (r"false\b", "false"),
    (r"or\b", "or"),
    (r"and\b", "and"),
    (r"not\b", "not"),
    (r"if\b", "if"),
    (r"else\b", "else"),
    (r"while\b", "while"),
    (r"for\b", "for"),      # Added 'for' keyword that does work like 'while' but with an initializer and an incrementer - Project
    (r"to\b", "to"),        # Added 'to' keyword that is used in 'for' loops to specify the end condition - Project
    (r"[a-zA-Z_][\w]*", "identifier"),
    (r".", "error"),
]

patterns = [(re.compile(p), tag) for p, tag in patterns]

def tokenize(characters):
    tokens = []
    position = 0
    line = 1
    column = 1
    while position < len(characters):
        match = None
        for pattern, tag in patterns:
            match = pattern.match(characters, position)
            if match:
                current_tag = tag
                break
        if not match:
            raise Exception(f"Unexpected character at line {line}, col {column}")
        
        value = match.group(0)
        if current_tag == "error":
            raise Exception(f"Unexpected character: {value!r}")
        if current_tag != "whitespace":
            token = {"tag": current_tag, "line": line, "column": column}
            if current_tag == "number":
                token["value"] = int(value)
            if current_tag == "identifier":
                token["value"] = value
            tokens.append(token)

        for ch in value:
            if ch == "\n":
                line += 1
                column = 1
            else:
                column += 1
        position = match.end()
    tokens.append({"tag": None, "line": line, "column": column})
    return tokens