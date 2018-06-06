def sum(a,b):
	if a > b:
		mysum = a + b
	else:
		if a == b:
			mysum = a + b
		else:
			mysum = b + a
	return a + b

x = sum(1,2)

def noarg():
	life = 42
	universe = 0
	ans = sum(life, universe)
	return ans

val = noarg()
print val