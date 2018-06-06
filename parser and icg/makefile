parser: src/*
	cp src/* bin/
	python2 -m py_compile bin/*.py
	mv bin/parser.py bin/irgen
	chmod +x bin/irgen
	bin/irgen test/tf.py   2>/dev/null > /dev/null # to create parsetable once
	rm parser.out
	mv parsetab.py bin/parsetab.py
	
clean:
	rm -f -rf bin/*
	rm -f *.dot
	rm -f *.png
	rm -f parse*
	rm -f dump
