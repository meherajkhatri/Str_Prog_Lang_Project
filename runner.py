import sys
from tokenizer import tokenize
from parser import parse
from evaluator import evaluate

# This is the main entry point for the interpreter. It reads a source file, tokenizes it, parses it into an AST, and then evaluates it.
def main():
    # Check if a filename was provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python runner.py <filename.t>")
        return
    
    with open(sys.argv[1], 'r') as f:
        code = f.read()
    
    tokens = tokenize(code)
    ast = parse(tokens)
    evaluate(ast, {})

if __name__ == "__main__":
    main()