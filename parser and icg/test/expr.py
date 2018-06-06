a = 1+7823 * 234 - 9 -------9 + 7^8 + 1<<8 
b = a* a + 7 * a -2 +a
c = 4
while a < 4 and b > 2 or c == 4:
	a = a + 1
	b = b -1 
	c = c*c +a -b 
	if a == b:
		break
	else :
		c = 10

	if a + b == 89:
		break

	a = b + a
	print a , b 
print c