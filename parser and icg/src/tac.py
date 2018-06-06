#Code stores array of all three address codes
code = {'program': []}
quad = {'program': -1}
nextQuad = {"program": 0}

tempVarBaseName = "var"
varCount = 0

def getNewTempVar():
	global varCount
	varCount += 1
	return tempVarBaseName + str(varCount)

def incrementQuad(functionName):
	global quad
	quad[functionName] = nextQuad[functionName]
	nextQuad[functionName] += 1
	return quad[functionName]

def getNextQuad(functionName):
	return nextQuad[functionName]

def getCodeLength(functionName):
	return quad[functionName]

def emit(functionName, regDest, regSrc1, regSrc2, op):
	global code
	incrementQuad(functionName)
	code[functionName].append([regDest, regSrc1, regSrc2, op])

def createNewFucntionCode(functionName):
	global code , quad
	code[functionName] = []
	quad[functionName] = -1
	nextQuad[functionName] = 0

def printCode():
	for functionName in code.keys():
		print functionName,":"
		for i in range(len(code[functionName])):
			print  "%5d: \t" %i, code[functionName][i]

def merge(list1, list2):
	return list1+list2

def backpatch(functionName, locationList, location):
	global code
	for position in locationList:
		code[functionName][position][2] = location

def noop(functionName, locationList):
	global code
	for position in locationList:
		code[functionName][position][3] = 'NOOP'