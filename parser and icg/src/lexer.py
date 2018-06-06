import sys
import lex
from lex import TOKEN
import tokenize

NO_INDENT = 0
MAY_INDENT = 1
MUST_INDENT = 2
errorList=[]
tokens=[]
keywordlist = [
		'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 
		'del', 'elif', 'else', 'except', 'exec', 'finally', 'for', 
		'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'not', 
		'or', 'pass', 'print', 'raise', 'return', 'try', 'while', 
		'with', 'yield'
		]

RESERVED = {}
for keyword in keywordlist:
	name = keyword.upper()
	RESERVED[keyword] = name
	tokens.append(name)

tokens = tuple(tokens) + (
		'EQEQUAL','NOTEQUAL','LESSEQUAL','LEFTSHIFT','GREATEREQUAL',
		'RIGHTSHIFT','PLUSEQUAL','MINEQUAL','STAREQUAL','SLASHEQUAL','PERCENTEQUAL',
		'STARSTAR','SLASHSLASH','STARSTAREQUAL','SLASHSLASHEQUAL',
		'COLON','COMMA','SEMI','PLUS','MINUS','STAR','SLASH','VBAR','AMPER','LESS',
		'GREATER','EQUAL','DOT','PERCENT','BACKQUOTE','CIRCUMFLEX','TILDE',	'AT',

	    'LPAREN', 'RPAREN',
	    'LBRACE', 'RBRACE',
	    'LSQB', 'RSQB',
		'NEWLINE',
		'INUMBER','FNUMBER',
		'BINARYNUMBER','OCTALNUMBER','HEXADECIMALNUMBER', 
		'NUMBER',
		'INDENT', 'DEDENT',
		'TRIPLESTRING', 'STRING', 
		'RAWSTRING','UNICODESTRING',
		'NAME','WS',
		'ENDMARKER'
	)

# Regular expression rules for simple tokens
t_EQEQUAL = r'=='
t_NOTEQUAL =  r'!='
t_LESSEQUAL = r'<='
t_LEFTSHIFT = r'<<'
t_GREATEREQUAL = r'>='
t_RIGHTSHIFT  = r'>>'
t_PLUSEQUAL = r'\+='
t_MINEQUAL = r'-='
t_STAREQUAL = r'\*='
t_SLASHEQUAL = r'/='
t_PERCENTEQUAL = r'%='
t_STARSTAR = r'\*\*'
t_SLASHSLASH = r'//'
t_STARSTAREQUAL = r'\*\*='
t_SLASHSLASHEQUAL = r'//='

t_COLON = r':'
t_COMMA = r','
t_SEMI  = r';'
t_PLUS  = r'\+'
t_MINUS = r'-'
t_STAR  = r'\*'
t_SLASH = r'/'
t_VBAR  = r'\|'
t_AMPER = r'&'
t_LESS  = r'<'
t_GREATER = r'>'
t_EQUAL = r'='
t_DOT  = r'\.'
t_PERCENT = r'%'
t_BACKQUOTE  = r'`'
t_CIRCUMFLEX = r'\^'
t_TILDE = r'~'
t_AT = r'@'

def newToken(newType, lineno):
	tok = lex.LexToken()
	tok.type = newType
	tok.value = None
	tok.lineno = lineno
	tok.lexpos = -100
	return tok
def t_LPAREN(t):
	r"\("
	t.lexer.parenthesisCount+=1
	return t
def t_RPAREN(t):
	r"\)"
	t.lexer.parenthesisCount-=1
	return t
def t_LBRACE(t):
	r"\{"
	t.lexer.parenthesisCount+=1
	return t
def t_RBRACE(t):
	r"\}"
	t.lexer.parenthesisCount-=1
	return t
def t_LSQB(t):
	r"\["
	t.lexer.parenthesisCount+=1
	return t
def t_RSQB(t):
	r"\]"
	t.lexer.parenthesisCount-=1
	return t

#ignore comments in source code
def t_comment(t):
	r"[ ]*\043[^\n]*"
	pass
@TOKEN(tokenize.Imagnumber)
def t_INUMBER(t):
    return t
@TOKEN(tokenize.Floatnumber)
def t_FNUMBER(t):
    return t
# FP number above integers
def t_BINARYNUMBER(t):
	r'0[bB]([0-1]+)'
	return t
def t_OCTALNUMBER(t):
	r'0[oO]([0-7]+)'
	return t
def t_HEXADECIMALNUMBER(t):
	r'0[xX]([0-9a-fA-F]+)'
	return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_TRIPLESTRING(t):
	r'"{3}([\s\S]*?"{3}) | \'{3}([\s\S]*?\'{3})'
	return t
def t_RAWSTRING(t):
	r'[rR](\"(\\.|[^\"\n]|(\\\n))*\") | [rR](\'(\\.|[^\'\n]|(\\\n))*\')'
	return t
def t_UNICODESTRING(t):
	r'[uU](\"(\\.|[^\"\n]|(\\\n))*\") | [uU](\'(\\.|[^\'\n]|(\\\n))*\')'
	return t
def t_STRING(t):
	r'(\"(\\.|[^\"\n]|(\\\n))*\") | (\'(\\.|[^\'\n]|(\\\n))*\')'
	return t
def t_continueLine(t):
	r'\\(\n)+'
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = "NEWLINE"
    if(t.lexer.parenthesisCount == 0):
    	return t

def t_NAME(t):
	r"[a-zA-Z_][a-zA-Z0-9_]*"
	t.type = RESERVED.get(t.value, "NAME")
	return t

# Error handling rule
def t_error(t):
    message = "\n# ERROR: Illegal character '%s' in %s at line %d" % (t.value[0], t.value, t.lineno)
    print message
    errorList.append(message)
    t.lexer.skip(1)

# REFERENCE: https://docs.python.org/2/reference/lexical_analysis.html
# WHITESPACE
def t_WS(t):
	r" [ \t\f]+ "
	value = t.value
	value = value.rsplit("\f", 1)[-1]
	pos = 0
	while True:
		pos = value.find("\t")
		if pos == -1:
			break
		n = 8 - (pos % 8)								# Convert each \t to 8 spaces (Python Documentation)
		value = value[:pos] + " "*n + value[pos+1:]
	t.value = value
	if t.lexer.atLineStart and t.lexer.parenthesisCount == 0:
		return t
def INDENT(lineno):
	return newToken("INDENT", lineno)
def DEDENT(lineno):
	return newToken("DEDENT",lineno)
# From Python 2 documentation:
# The indentation levels of consecutive lines are used to generate INDENT and DEDENT tokens, 
# using a stack, as follows.
# Before the first line of the file is read, a single zero is pushed on the stack; 
# this will never be popped off again. The numbers pushed on the stack will always 
# be strictly increasing from bottom to top. At the beginning of each logical line, 
# the line's indentation level is compared to the top of the stack. If it is equal, 
# nothing happens. If it is larger, it is pushed on the stack, and one INDENT token 
# is generated. If it is smaller, it must be one of the numbers occurring on the stack; 
# all numbers on the stack that are larger are popped off, and for each number popped 
# off a DEDENT token is generated. At the end of the file, a DEDENT token is generated 
# for each number remaining on the stack that is larger than zero.

def identifyIndenations(lexer, token_stream):
	lexer.atLineStart = atLineStart = True
	indent = NO_INDENT
	saw_colon = False
	for token in token_stream:
		token.atLineStart = atLineStart
		if token.type == "COLON":
			atLineStart = False
			indent = MAY_INDENT
			token.must_indent = False
		elif token.type == "NEWLINE":
			atLineStart = True
			if indent == MAY_INDENT:
				indent = MUST_INDENT  			# MUST INDENT
			token.must_indent = False
		elif token.type == "WS":
			assert token.atLineStart == True
			atLineStart = True
			token.must_indent = False
		else:
			if indent == MUST_INDENT:
				token.must_indent = True
			else:
				token.must_indent = False
			atLineStart = False
			indent = NO_INDENT

		yield token
		lexer.atLineStart = atLineStart

def assignIndentations(token_stream):
	levels = [0]
	token = None
	depth = 0
	lastSeenWhitespace = False
	for token in token_stream:
		if token.type == "WS":
			assert depth == 0
			depth = len(token.value)
			lastSeenWhitespace = True
			continue
		if token.type == "NEWLINE":
			depth = 0
			if lastSeenWhitespace or token.atLineStart:
				continue
			yield token
			continue
		lastSeenWhitespace = False
		if token.must_indent:
			if not (depth > levels[-1]):
				# raise IndentationError("Expected an indented block")
				print "Indentation Error in line no "+str(token.lineno)
				sys.exit()
			levels.append(depth)
			yield INDENT(token.lineno)
		elif token.atLineStart:
			if depth == levels[-1]:
				pass
			elif depth > levels[-1]:
				print "Indentation Error in line no "+str(token.lineno)
				sys.exit()
				# raise IndentationError("IndentationError: not in new block")
			else:
				try:
					i = levels.index(depth)
				except ValueError:
					print "Indentation Error in line no "+str(token.lineno)
					sys.exit()
					# raise IndentationError("Inconsistent Indentation")
				for z in range(i+1, len(levels)):
					yield DEDENT(token.lineno)
					levels.pop()
		yield token
	if len(levels) > 1:
		assert token is not None
		for z in range(1, len(levels)):
			yield DEDENT(token.lineno)

# This filter was in main() of previous lexer
def filter(lexer, addEndMarker = True):
	token_stream = iter(lexer.token, None)
	token_stream = identifyIndenations(lexer, token_stream)
	token_stream = assignIndentations(token_stream)
	tok = None
	for tok in token_stream:
		yield tok
	if addEndMarker:
		lineno = 1
		if tok is not None:
			lineno = tok.lineno
		yield newToken("ENDMARKER", lineno)

# To merge ply's lexer with indent feature
# Built from previous main()
class G1Lexer(object): 
	def __init__(self):
		self.lexer = lex.lex()
		self.token_stream = None
	def input(self, data, addEndMarker=True):
		self.lexer.parenthesisCount = 0
		data+="\n"
		self.lexer.input(data)
		self.token_stream = filter(self.lexer, addEndMarker)
	def token(self):
		try:
			return self.token_stream.next()
		except StopIteration:
			return None

# g1 = G1Lexer()
# data = open('../test/test1.py').read()
# g1.input(data)
# t = g1.token()
# while t:
# 	print t
# 	t = g1.token()