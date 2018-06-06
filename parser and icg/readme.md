CS335A: Compiler Design (Assignment 3: INTERMEDIATE CODE GENERATOR)
===================================================================

* Source Language: *Python*
* Target Language: *MIPS Assembly*
* Implementation Language: *Python*
* Authors: Abhilash Kumar, Arnab Ghosh and Saurav Kumar

* Tool Used : PLY (Python Lex and Yacc)

### Three Address Code Representation
_____________________________________

1. Representation: ```regDest, regSrc1, regSrc2, op```

2. Operators:

	- HALT
	- JUMP_RETURN
	- PARAM
	- SW
	- LW
	- =
	- PRINT
	- GOTO
	- RETURN
	- COND_GOTO
	- %
	- /
	- *
	- +
	- -
	- >
	- <
	- >=
	- <=	
	- ==
	- !=
	- |
	- ^
	- &
	- not
	- and
	- or
	- <<
	- >>



### Running Instruction
_______________________
1. Run the makefile 
```
make
```
2. To run the IR Generator, pass the path of filename as argument.
```
bin/irgen test/<filename>.py
```

3. To clean the executables and other helper files, run make clean.
```
make clean
```

### Directory Structure
_______________________
* bin:
	* converter.py [Python source file to convert the dump of parser into dot file: may be needed for debugging]
	* lex.py [Python source file from PLY for lexing]
	* lexer.py [Python source file to specify language lexemes]
	* irgen [Python dependent bytecode for parsing and semantic analysis]
	* parser.py [Python source file to specify grammar]
	* yacc.py [Python source file from PLY for parsing ]
	* symbolTable.py [Python source file with necessary functions related to symbol table]
	* tac.py [Python scource file with necessary functions related to Three Address Code Representation]
* src:
	* converter.py [Python source file to convert the dump of parser into dot file: may be needed for debugging]
	* lex.py [Python source file from PLY for lexing]
	* lexer.py [Python source file to specify language lexemes]
	* irgen [Python dependent bytecode for parsing and semantic analysis]
	* parser.py [Python source file to specify grammar]
	* yacc.py [Python source file from PLY for parsing ]
	* symbolTable.py [Python source file with necessary functions related to symbol table]
	* tac.py [Python scource file with necessary functions related to Three Address Code Representation]
* test:
	* 'filename'.py [Test files]
* .gitignore
* makefile [To move the source files to bin directory and compile bytecode for lexer and making it executable]
* readme.md

