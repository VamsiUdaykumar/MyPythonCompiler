# Python program to find the factorial of a number provided by the user.

# change the value for a different result
num = 7

# uncomment to take input from the user
#num = int(input("Enter a number: "))

factorial = 1

# check if the number is negative, positive or zero
if num < 0:
   print("undefined")

else:
   for i in range(0,1):
	for j in range(0,1):
	       factorial = factorial*i
   print("fact=",factorial)
