from invertedindex import build_inverted_index, OR, AND, ANDNOT, Preprocessor
from parse import get_parser
import glob
import pprint

p = Preprocessor()

files = glob.glob("docs/*.txt")
docs = []
for file in files:
    with open(file, 'r') as f:
        docs.append(f.read())

iix = build_inverted_index(docs, p, 100)

FUNCTIONS = {
    'RET': lambda word: iix.sources(word),
    'OR': lambda a, b: OR(a, b),
    'AND': lambda a, b: AND(a, b),
    'ANDNOT': lambda a, b: ANDNOT(a, b)
}


def execute(ast):
    if not ast:
        return
    if isinstance(ast, tuple) and ast[0] == 'fncall':
        fn_name = ast[1]
        fn_args = execute(ast[2])
        return FUNCTIONS[fn_name](*fn_args)
    elif isinstance(ast, list):
        return [execute(item) for item in ast]
    elif isinstance(ast, str):
        return ast


parser = get_parser()
# pprint.pprint(iix.indexed_words)

x = parser.parseString("ANDNOT(RET(legolas), OR(RET(hobbit), RET(anillo)))")
print(x)

while True:
    try:
        line = input(">> ")
        ast = list(parser.parseString(line))
        print(ast)
        res = execute(ast)[0]
        print(res)
    except Exception:
        print("Error. Check input format.")
