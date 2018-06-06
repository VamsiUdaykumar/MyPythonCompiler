import ply.lex as lex
import csv

reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'elif' : 'ELIF',
   'while' : 'WHILE',
   'import' : 'IMPORT',
   'def' : 'DEF',
   'print' : 'PRINT',
   'global' : 'GLOBAL',
   'lambda' : 'LAMBDA',
}

rl = [] #reserved word list
for k in reserved:
    rl.append(reserved[k])

# List of token names.   This is always required
tokens = ['LBRACE','RBRACE','NAME',
          'LPAREN','RPAREN',
          'ID','FUNC',
          'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
          'NEWLINE','WHITE','NUMBER','INDENT',
            'COMMENT',#'MULTCOM',
            'ERROR','COL',
            'INTEGER','FLOAT','STRING',
            'GRT','LSR','EQ','GRTEQ','LSREQ',] + list(reserved.values())

literals = [ '{', '}' , '(' , ')']

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS = r'\='
t_GRT = r'>'
t_LSR = r'<'
t_GRTEQ = r'>='
t_LSREQ = r'<='
t_EQ = r'=='
t_COL = r':'
t_INTEGER = r'\d+'
t_FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_STRING = r'\".*?\"'
t_LPAREN = r'\('
t_RBRACE = r'\}'
t_RPAREN = r'\)'
t_LBRACE = r'\{'

#def t_lbrace(t):
#    r'\{'
#    t.type = '{'      # Set token type to the expected literal
#    return t

#def t_rbrace(t):
#    r'\}'
#    t.type = '}'      # Set token type to the expected literal
#    return t

#def t_lparen(t):
#    r'\('
#    t.type = '('      # Set token type to the expected literal
#    return t

#def t_rparen(t):
#    r'\)'
#    t.type = ')'      # Set token type to the expected literal
#    return t

#def t_FUNC(t):
#    r'[d][e][f][\s][a-zA-Z_]*[a-zA-Z_0-9]*[(]*'
#    t.value = str(t.value)[4:len(str(t.value))-2]
#    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

#def t_indent(t):
#    c = 0
#    for i in str(t.value):
#        if i in ['\s']:
#            c=c+1
#        else:
#            break

#    global indent
#    if c>0:
#        indent = [True, c]
#    else:
#        indent = [False, 0]


# Define a rule so we can track line numbers
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    op.write('\n')
    return t

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0],"on line no",t.lexer.lineno )
    t.lexer.skip(1)

def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded

def t_WHITE(t):
    r'\s+'
    op.write(str(t.value))
    return t


#def t_MULTCOM(t):
#    r'\""".*.\"""'
#    pass

# Build the lexer
lex.lex()


# Give the lexer some input
data = open('temp.py','r')
lex.input(data.read())
data.close()

#modified code file
op = open('code.py','w')

#symbol table file
st = open('st','w')
st.write('TYPE'+'\t'+'VALUE'+'\t'+'LINE_NO'+'\t'+'LEXPOS'+'\n\n')

l=[] #tokens list of lists
al =[] #all tokens

newl = [0 , 0] # [ lineno , lexpos ] 

ti = 0 #token index
# Tokenize
while True:
    tok = lex.token()

    if not tok: 
        break      # No more input
#    print(tok)
    al.append([tok.type,tok.value,tok.lineno,tok.lexpos])
    op.write(str(tok.value))    #modified code
    
#    if (tok.type == 'NEWLINE'):
#        newl = [tok.lineno , tok.lexpos]
#        print(newl)
    
#    if (tok.type == 'WHITE'):
#        if(tok.lexpos == newl[1]+1):
#            indent[0] = True
#            indent[1] = indent[1] + 1
#    else:

#    if (tok.type == 'ID'):
#        plno = tok.lineno-1 #present line no -1
#        while(plno>0 and 'WHITE' in [str(x[1]) for x in l if x[2]==plno ] ):
#            plno -= 1
        
            
    
    #symbol table file
    if(tok.type in rl or str(tok.type) in ['NUMBER','INTEGER','FLOAT','STRING']):
        line = str(tok.type)+'\t'+str(tok.value)+'\t'+str(tok.lineno)+'\t'+str(tok.lexpos)+'\n'
        st.write(line)
    
        l.append([tok.type,tok.value,tok.lineno,tok.lexpos])
        ti += 1
        
    if (str(tok.type) == 'ID'):
#        print([x[1] for x in l])
        if tok.value not in [x[1] for x in l]:
            line = str(tok.type)+'\t'+str(tok.value)+'\t'+str(tok.lineno)+'\t'+str(tok.lexpos)+'\n'
            st.write(line)
            l.append([tok.type,tok.value,tok.lineno,tok.lexpos])
        else:
            ln = tok.lineno - 1
            while len([ x[0] for x in al if int(x[2])==ln ])>0 and [ x[0] for x in al if int(x[2])==ln ][0] == 'WHITE' and str(tok.value) not in [ x[0] for x in al if int(x[2])==ln ]:
                ln -= 1
                
            if  len([x[0] for x in al if int(x[2]==ln)])>0 and [x[0] for x in al if int(x[2]==ln)][0] == 'DEF' and str(tok.value) not in [ x[0] for x in al if int(x[2])==ln ]:
                line = str(tok.type)+'\t'+str(tok.value)+'\t'+str(tok.lineno)+'\t'+str(tok.lexpos)+'\n'
                st.write(line)
                l.append([tok.type,tok.value,tok.lineno,tok.lexpos])                
    total = tok.lineno
    
"""x=[]
print('\n\n\n')
for i in range(1,total+1):
    temp = []
    for j in al:
        if (int(j[2]) == i):
            temp.append(j)
    x.append(temp)

for i in x:
    print(i)
"""
print('\n\n')
#[print(x) for x in l]


#writing to csv file
myFile = open('symbol_table.csv', 'w')
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(l)
                                     #yacc 

# Precedence rules for the arithmetic operators
precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

# dictionary of names (for storing variables)
names = { }

def p_while(p):
    'statement : WHILE LPAREN expression RPAREN COL statement'
    if p[3] > 0 : print(p[6])  

def p_check_if(p):
    '''statement : IF LPAREN expression RPAREN COL statement ELIF LPAREN expression RPAREN statement
               | IF LPAREN expression RPAREN COL statement ELSE COL statement
	       | IF LPAREN expression RPAREN COL statement'''
          
    if p[3] > 0: print(p[6])
    elif p[3]<0 and p[9]>0: print(p[9])
    elif p[3]<0 : print(p[8])

def p_statement_assign(p):
    'statement : NAME EQUALS expression'
    names[p[1]] = p[3]

def p_statement_expr(p):
    'statement : expression'
    print(p[1])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if p[2] == '+'  : p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_name(p):
    'expression : NAME'
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_error(p):
    print("Syntax error at '%s'" % p.value)

import ply.yacc as yacc
yacc.yacc()

o=open('op','r')
for line in o:
    try:
        yacc.parse(line)
    except EOFError:
        break 
