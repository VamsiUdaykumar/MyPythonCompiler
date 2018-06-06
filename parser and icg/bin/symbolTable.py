import pprint

symbolTable = {
	"program" : {
		"scopeName"		: "program",
		"type"			: "FUNCTION",
		"returnType"	: "UNDEFINED",
	}
}
stackHistory = []
offsetStack	= [0]
functionlist = {'program':symbolTable['program']}
scopeStack	= [symbolTable["program"]]

def lookup(identifier):
	global scopeStack
	currentScope = len(scopeStack)
	return lookupScopeStack(identifier, currentScope - 1)

def lookupScopeStack(identifier, position):
	if position == -1:
		return None
	global scopeStack
	currentScope = scopeStack[position]
	# if sought identifier is not in current scope, it may be in parent
	if identifier in currentScope:
		return currentScope[identifier]
	else:
		return lookupScopeStack(identifier, position - 1)

def getCurrentScope():
	global scopeStack
	return scopeStack[len(scopeStack) - 1]["scopeName"]
	# ensure every scope has this key

def addScope(scopeName):
	global scopeStack
	currentScope = scopeStack[len(scopeStack) - 1]
	currentScope[scopeName] = {
		"scopeName"		: scopeName,
		"parentName"	: currentScope["scopeName"],
		"type"			: "FUNCTION",
		"returnType"	: "UNDEFINED"
	}
	addIdentifier('True', 'BOOLEAN')
	addAttribute('True', scopeName, 1)
	addIdentifier('False', 'BOOLEAN')
	addAttribute('False', scopeName, 0)	
	scopeStack.append(currentScope[scopeName])

	# start new relative addressing
	offsetStack.append(0)
	functionlist[scopeName] = currentScope[scopeName]

def addIdentifier(identifier, identifierType):
	global scopeStack
	currentScope = scopeStack[len(scopeStack) - 1]
	width = getWidthFromType(identifierType)
	# TODO Add other types

	currentOffset = offsetStack.pop()
	if not identifier in currentScope:
		currentScope[identifier] = dict()
	currentScope[identifier]["offset"] = currentOffset
	currentScope[identifier]["type"] = identifierType
	currentScope[identifier]["width"] = width	

	offsetStack.append(currentOffset + width)

def addAttribute(identifier, key, value):
	entry = lookup(identifier)
	entry[key] = value

def getAttribute(identifier, key):
	entry = lookup(identifier)
	if key in entry:
		return entry[key]
	else:
		return None

def getAttributeFromCurrentScope(key):
	global scopeStack
	currentScope = scopeStack[len(scopeStack) - 1]
	return currentScope[key]

def addAttributeToCurrentScope(key, value):
	global scopeStack
	currentScope = scopeStack[len(scopeStack) - 1]
	currentScope[key] = value

def exists(identifier):
	if lookup(identifier) != None:
		return True
	return False

def existsInCurrentScope(identifier):
	global scopeStack
	return scopeStack[len(scopeStack)-1].get(identifier, False) != False

def removeCurrentScope():
	global scopeStack, stackHistory
	currentScope = scopeStack.pop()
	currentScope["width"] = offsetStack.pop()
	stackHistory.append(currentScope)

# print scopeStack
def printST():
	print scopeStack

def getAttributeFromFunctionList(function, key):
	if function in functionlist:
		return functionlist[function][key]
	else :
		return None 	

def getBaseAddress(scopeName, key):
	return 100

def getWidthFromType(identifierType):
	if identifierType == 'NUMBER':
		width = 4
	elif identifierType == 'STRING':
		width = 256
	elif identifierType == 'UNDEFINED':
		width = 0
	elif identifierType == 'FUNCTION':
		width = 4
	elif identifierType == 'BOOLEAN':
		width = 1
	else:
		width = 0
	return width

def printSymbolTableHistory():
	print "\n\n SYMBOL TABLE"
	print     "--------------"
	for st in stackHistory:
		print "\nSCOPE: " + st['scopeName']
		print "-----------------------"
		pprint.pprint (st)
		print "-----------------------\n"
