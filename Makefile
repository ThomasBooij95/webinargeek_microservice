# Makefile for Django Commands

# Define the Python interpreter to use (e.g., python3 or python)
PYTHON = python

# Define the default command to run when "make" is executed
.DEFAULT_GOAL := help

# Help message
help:
	@echo "Django Makefile Commands:"
	@echo "  make env                  - Activate the poetry environment"
	@echo "  make rs                   - Start the development server"
	
# start new Django project
up:
	docker compose up -d

ssh-wg:
	ssh root@stresslessdogs.booijanalytics.nl

build:
	docker build -t app ./

run:
	docker run -t port 5000:80 app

start-network:
	docker network create traefik-public

