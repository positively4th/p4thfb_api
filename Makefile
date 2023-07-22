.PHONY: \
	setup setup-requirements setup-contrib \
	docker docker-api docker-postgres \

default: setup docker

all: setup docker

container: setup

#setup
setup: setup-requirements setup-contrib

setup-requirements: 
	python -m venv .venv \
	&& ( \
		source .venv/bin/activate \
		&& \
		pip install --upgrade pip \
		&& \
		pip install -r requirements.txt \
	)

setup-contrib: 
	make -C contrib

#docker
docker: docker-api docker-postgres

docker-api:
	docker build -t api -f api.dockerfile .

docker-postgres:
	docker build -t postgresql -f postgres.dockerfile .

clean: 
	rm -rf .venv \
	&& make -C contrib clean \
	&& docker rmi --force postgresql \
	&& docker rmi --force api 

