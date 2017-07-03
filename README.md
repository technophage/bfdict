bruteforce dictonary generation tool/module

command line options;

	-i		Interactive setup mode [Use alone]
	-m MNLEN	Minimum word length
	-x MXLEN	Maximum word length
	-l		Use lowercase characters
	-u		Use uppercase characters
	-n		Use number characters
	-s		Use standard symbols
	-c CUSTDICT	Set custom character set
	-f FILE		Output filename [Default is to screen]

## 
Can also be used as an importable module like this;

	from passlib.hash import des_crypt
	from bfdict import bfdict

	bf = bfdict()

	bf.mnlen = 1
	bf.mxlen = 3
	bf.uselower = True

	passwd = bf.nextword()
	while passwd:
		print(des_crypt.hash(passwd))
		passwd = bf.nextword()

