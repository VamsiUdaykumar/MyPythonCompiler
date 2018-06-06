'''import json
from ast import parse
import ast2json

ast = ast2json(parse(open('for.py').read()))
print (json.dumps(ast, indent=4))
'''
import ast
fn=open("/home/vamsi/Desktop/CDnew/for.py","r")
op=ast.parse(fn)
ast.dump(tree)
