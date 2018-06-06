'''

Parses a Python source file into an AST in JSON format. can be viewed
online in a viewer like: http://jsonviewer.stack.hu/

Usage:

python parse_python_to_json.py --pyfile=test.py      # pass in code within a file
python parse_python_to_json.py 'print "Hello world"' # pass in code as a string

Try running on its own source code; whoa very META!

python parse_python_to_json.py --pyfile=parse_python_to_json.py


Output: prints JSON to stdout

Created on 2017-01-20 by Philip Guo
'''

import ast
import json
import optparse
#import pprint
import pythonparser # based on https://github.com/m-labs/pythonparser
import os
import sys

#pp = pprint.PrettyPrinter()

class Visitor:
    def visit(self, obj, level=0):
        """Visit a node or a list of nodes. Other values are ignored"""
        if isinstance(obj, list):
            return [self.visit(elt, level) for elt in obj]

        elif isinstance(obj, pythonparser.ast.AST):
            typ = obj.__class__.__name__
            #print >> sys.stderr, obj
            loc = None
            if hasattr(obj, 'loc'):
                loc = {
                    'start': {'line': obj.loc.begin().line(), 'column': obj.loc.begin().column()},
                    'end':   {'line': obj.loc.end().line(),   'column': obj.loc.end().column()}
                }
            # TODO: check out obj._locs for more details later if needed

            d = {}
            d['type'] = typ
            d['loc'] = loc
            d['_fields'] = obj._fields
            for field_name in obj._fields:
                val = self.visit(getattr(obj, field_name), level+1)
                d[field_name] = val
            return d

        else:
            # let's hope this is a primitive type that's JSON-encodable!
            return obj


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("--pyfile", action="store", dest="pyfile",
                      help="Take input from a Python source file")
    parser.add_option("--pp", action="store_true",
                      help="Pretty-print JSON for human viewing")
    (options, args) = parser.parse_args()

    if options.pyfile:
        code = open(options.pyfile).read()
    else:
        code = args[0]
        # make sure it ends with a newline to get parse() to work:
        if code[-1] != '\n':
            code += '\n'

    indent_level = None
    if options.pp:
        indent_level = 2

    try:
        p = pythonparser.parse(code)

        v = Visitor()
        res = v.visit(p)
        print json.dumps(res, indent=indent_level)
    except pythonparser.diagnostic.Error as e:
        error_obj = {'type': 'parse_error'}
        diag = e.diagnostic
        loc = diag.location

        error_obj['loc'] = {
                    'start': {'line': loc.begin().line(), 'column': loc.begin().column()},
                    'end':   {'line': loc.end().line(),   'column': loc.end().column()}
        }

        error_obj['message'] = diag.message()
        print json.dumps(error_obj, indent=indent_level)
        sys.exit(1)
