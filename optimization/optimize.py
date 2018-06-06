import re
import sys
icg_file = "output_file.txt"
istemp = lambda s : bool(re.match(r"^t[0-9]*$", s)) 
isid = lambda s : bool(re.match(r"^[A-Za-z][A-Za-z0-9_]*$", s)) #can be temp also
binary_operators = {"+", "-", "*", "/", "*", "&", "|", "^", ">>", "<<", "==", ">=", "<=", "!=", ">", "<"}
def printicg(list_of_lines, message = "") :
	print(message.upper())
	for line in list_of_lines :
		print(line.strip())


def eval_wrap(line) :
	tokens = line.split()
	if len(tokens) != 5 :
		return line
	if tokens[1] != "=" or tokens[3] not in binary_operators:
		return line
	#tokens = tokens[2:]
	if tokens[2].isdigit() and tokens[4].isdigit() :
		result = eval(str(tokens[2] + tokens[3] + tokens[4]))
		return " ".join([tokens[0], tokens[1], str(result)])
	if tokens[2].isdigit() or tokens[4].isdigit() : #Replace the identifier with a number and evaluate
		op1 = "5" if isid(tokens[2]) else tokens[2]
		op2 = "5" if isid(tokens[4]) else tokens[4]
		op = tokens[3]
		try : 
			result = int(eval(op1+op+op2))
			if result == 0 : #multiplication with 0
				return " ".join([tokens[0],tokens[1], "0"])
			elif result == 5 : #add zero, subtract 0, multiply 1, divide 1
				if isid(tokens[2]) and tokens[4].isdigit() :
					return " ".join([tokens[0], tokens[1], tokens[2]])
				elif isid(tokens[4]) and tokens[2].isdigit():
					return " ".join([tokens[0], tokens[1], tokens[4]])
			elif result == -5 and tokens[2] == "0" : # 0 - id
				return " ".join([tokens[0], tokens[1], "-"+tokens[4]])
			return " ".join(tokens)

		except NameError :
			return line
		except ZeroDivisionError :
			print("Division By Zero is undefined")
			quit()
	return line


def fold_constants(list_of_lines) :
	"""
	Some expressions that can have a definite answer need not be waste run time resources :
	e.g.
	1. number + number, number - number etc.
	2. identifier + 0, identfier / 0, identifer - 0, identifier*0 and their commutatives
	3. identifier * 1, identifier / 1
	"""

	new_list_of_lines = []
	for line in list_of_lines :
		new_list_of_lines.append(eval_wrap(line))
	return new_list_of_lines

def remove_dead_code(list_of_lines) :
	"""
Temporaries that are never assigned to any variable nor used in any expression are deleted. Done recursively.
	"""
	num_lines = len(list_of_lines)
	temps_on_lhs = set()
	for line in list_of_lines :
		tokens = line.split()
		if istemp(tokens[0]) :
			temps_on_lhs.add(tokens[0])

	useful_temps = set()
	for line in list_of_lines :
		tokens = line.split()
		if len(tokens) >= 2 :
			if istemp(tokens[1]) :
				useful_temps.add(tokens[1])
		if len(tokens) >= 3 :
			if istemp(tokens[2]) :	
				useful_temps.add(tokens[2])

	temps_to_remove = temps_on_lhs - useful_temps
	new_list_of_lines = []
	for line in list_of_lines :
		tokens = line.split()
		if tokens[0] not in temps_to_remove :
			new_list_of_lines.append(line)
	if num_lines == len(new_list_of_lines) :
		return new_list_of_lines
	return remove_dead_code(new_list_of_lines)

if __name__ == "__main__" :
	if len(sys.argv) == 2 :
		icg_file = str(sys.argv[1])
	
	list_of_lines = []
	f = open(icg_file, "r")
	for line in f :
		list_of_lines.append(line)
	f.close()

	printicg(list_of_lines, "ICG")
	without_deadcode = remove_dead_code(list_of_lines)
	printicg(without_deadcode, "Optimized ICG after removing dead code")
	print("Eliminated", len(list_of_lines)-len(without_deadcode), "lines of code")

	printicg(list_of_lines, "ICG")
	folded_constants = fold_constants(list_of_lines)
	printicg(folded_constants, "Optimized ICG after constant folding")
	
	
	
