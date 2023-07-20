.PHONY: requirements contrib api postgres

all: local containers 

local: requirements contrib

containers: api postgres

container: requirements contrib

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

api:
	docker build -t api -f api.dockerfile .

postgres:
	docker build -t postgresql -f postgres.dockerfile .

clean: 
	rm -rf .venv \
	&& make -C contrib clean \
	&& docker rmi --force postgresql \
	&& docker rmi --force api 

