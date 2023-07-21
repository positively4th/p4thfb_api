all = pyas p4thcson p4thpymap p4thpydb p4thpymisc p4thpyplot

.PHONY: $(all)

all: $(all)

p4thcson: 
	(git clone https://github.com/positively4th/p4thcson.git || echo) \
	&& (cd p4thcson && git pull) \
	&& ([ -f "p4thcson/Makefile" ] && make -C p4thcson || echo)

pyas: 
	(git clone https://github.com/positively4th/pyas.git || echo) \
	&& (cd pyas && git pull) \
	&& ([ -f "pyas/Makefile" ] && make -C pyas || echo)

p4thpymap: 
	(git clone https://github.com/positively4th/p4thpymap.git || echo) \
	&& (cd p4thpymap && git pull) \
	&& ([ -f "p4thcson/Makefile" ] && make -C p4thpymap || echo)

p4thpydb: 
	(git clone https://github.com/positively4th/p4thpydb.git || echo) \
	&& (cd p4thpydb && git pull) \
	&& ([ -f "p4thpydb/Makefile" ] && make -C p4thpydb || echo)

p4thpymisc: 
	(git clone https://github.com/positively4th/p4thpymisc.git || echo) \
	&& (cd p4thpymisc && git pull) \
	&& ([ -f "p4thpymisc/Makefile" ] && make -C p4thpymisc || echo)

p4thpyplot: 
	(git clone https://github.com/positively4th/p4thpyplot.git || echo) \
	&& (cd p4thpyplot && git pull) \
	&& ([ -f "p4thpyplot/Makefile" ] && make -C p4thpyplot || echo)

clean: 
	rm -rf $(all)


