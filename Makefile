SHELL := /bin/bash
.DEFAULT: help
help:
	@echo "==========================================================="
	@echo "            Contacts Makefile                              "
	@echo "==========================================================="
	@echo "make clean"
	@echo "    - Remove all Python compile & cache files"
	@echo "make deps"
	@echo "    - Install Python dependencies. Recommended to have an active venv"
	@echo "==========================================================="
	@echo "Launch Options"
	@echo "make run"
	@echo "    - Run flask server"
	@echo "make debug-run"
	@echo "    - Run flask server with debug option"
	@echo "make develop"
	@echo "    - Run flask server with debug option and watch option for hot reloading"
	

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -Rf {} +

deps:
	pip3 install -r requirements.txt

debug-run:
	flask run --debug

styles:
	sass --watch --silence-deprecation mixed-decls,color-functions,global-builtin,import ./static/styles.scss ./static/styles.css 
	
develop:
	flask run --host 0.0.0.0 --debug --port 2000
 
run:
	flask run
	
staging:
	docker-compose up -d --build --force-recreate
	
#deploy:

.PHONY: help clean deps debug-run styles develop run staging