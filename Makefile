.PHONY: requirements contrib

all: requirements contrib
	
requirements: 
	python -m venv .venv \
	&& ( \
		source .venv/bin/activate \
		&& \
		pip install --upgrade pip \
		&& \
		 pip install -r requirements.txt \
	)

contrib: 
		make -C contrib

clean: 
		rm -rf .venv \
		&& make -C contrib clean


