// This is an example source file for the interpreter.
// It demonstrates the use of a 'for' loop, which is a new feature added in this project.
// The 'for' loop is syntactic sugar that gets desugared into a 'while' loop in the parser. The evaluator then executes the resulting AST as usual.
sum = 0;
for i = 1 to 5 {
    print i;
    sum = sum + i;
};
print sum;