import ply.lex as lex
import csv

reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'elif' : 'ELIF',
   'for' : 'FOR',
   'import' : 'IMPORT',
   'def' : 'DEF',
   'print' : 'PRINT',
   'global' : 'GLOBAL',
   'lambda' : 'LAMBDA',
   'in'	:	'IN',
   'range':	'RANGE',
   'not in' :	'NOTIN'
}

rl = [] 
for k in reserved:
    rl.append(reserved[k])

tokens=['LBRACE','RBRACE','RSBRACE','LSBRACE','LPAREN','RPAREN','ID','FUNC','PLUS','MINUS','TIMES','DIVIDE','EQUALS','NEWLINE','WHITE','NUMBER','COMMENT','ERROR','COL' ,'INTEGER','FLOAT','DOUBLE','STRING','MSTR',  'GRT','LSR','EQ','GRTEQ','LSREQ',] + list(reserved.values())

literals = [ '{', '}','[',']' , '(' , ')']

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
t_MSTR = r'\"\"\"[\n**\n*]*\"\"\"'
t_STRING = r'\".*?\"'
t_INTEGER = r'\d+'
t_FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_LPAREN = r'\('
t_RBRACE = r'\}'
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_LSBRACE = r'\['
t_RSBRACE = r'\]'

indent = [False,0]

def t_lbrace(t):
    r'\{'
    t.type = '{'      
    return t

def t_rbrace(t):
    r'\}'
    t.type = '}'      
    return t

def t_lparen(t):
    r'\('
    t.type = '('     
    return t

def t_rparen(t):
    r'\)'
    t.type = ')'      
    return t

def t_rsbrace(t):
    r'\]'
    t.type = ']'      
    return t
def t_lsbrace(t):
    r'\['
    t.type = '['      
    return t

status = 0 #to keep track of indentation
def t_tab(t):
    r'\t+'
    global status
    status = len(str(t.value)) - len(str(t.value).strip('\t'))

def t_FUNC(t):
    '[d][e][f][\s]'r'[a-zA-Z_]*[a-zA-Z_0-9]*[(]*'
    t.value = str(t.value)[4:len(str(t.value))-2]
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID') 
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_indent(t):
    r'[:]\n'
    global indent
    indent=[True, len(str(t.value)) - len( str(t.value).strip() )  ]
    t.lexer.lineno += len(t.value)
    op.write('\n\t')


def t_newline(t):
    r'\t+'
    t.lexer.lineno += len(t.value)
    op.write('\n')
    c = 0
    for i in str(t.value):
        if i in [' ','  ','\n','\t','\s']:
            c=c+1
        else:
            break
    global indent
    if c>0:
        indent = [True, c]
    else:
        indent = [False, 0]
    


def t_error(t):
    print("Illegal character '%s'" % t.value[0],"on line no",t.lexer.lineno )
    t.lexer.skip(1)

def t_COMMENT(t):
    r'\#.*'
    t.lexer.lineno += len(t.value)
    pass

def t_WHITE(t):
    r'\s+'
    op.write(str(t.value))
    pass


lex.lex()


data = open('/home/vamsi/Desktop/lexer/for.py','r')
lex.input(data.read())
data.close()


op = open('/home/vamsi/Desktop/lexer/code','w')

st = open('/home/vamsi/Desktop/lexer/symbol_table','w')
st.write('TYPE'+'\t'+'VALUE'+'\t'+'LINE_NO'+'\t'+'LEXPOS'+'\n\n')

l=[]

while True:
    tok = lex.token()
    if not tok: 
        break       
    print(tok,'\t\t\t',indent)
    op.write(str(tok.value))   
    
    if(tok.type in rl or str(tok.type) in ['ID','NUMBER','INTEGER','FLOAT','DOUBLE','STRING']):
        if tok.value not in [x[1] for x in l]:
            line = str(tok.type)+'\t'+str(tok.value)+'\t'+str(tok.lineno)+'\t'+str(tok.lexpos)+'\n'
            st.write(line)
    
            l.append([tok.type,tok.value,tok.lineno,tok.lexpos])
    

print('\n\n')
#[print(x) for x in l]

myFile = open('symbol_table.csv', 'w')
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(l)
