
file=open("out.txt",'r')
f=open("ot.txt",'w')
for i in file:
	line=i.split(" ")[3].split("\'")[1]
	f.write(str(line)+'\n')
	
f.close()
f2=open("op",'r')
f3=open("final",'w')
f1=open("ot.txt",'r')
for i in f1:

	v=str(i.split(" ")[0])
	print(type(v))
	for line in f2:
		l=line.split("=")[0]
		print(l)
		if(v in l):
			print('dd')
	#	else:
		#	f3.write(line)
