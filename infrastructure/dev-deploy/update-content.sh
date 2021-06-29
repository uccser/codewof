#!/bin/bash

source ./infrastructure/dev-deploy/load-dev-deploy-config-envs.sh

# Updates the database for the development system
cp ./infrastructure/cloud-sql-proxy/docker-compose.yml ./docker-compose.yml

# Decrypt secret files archive that contain credentials.
./infrastructure/dev-deploy/decrypt-dev-secrets.sh

# Load environment variables.
source ./codewof/load-dev-envs.sh

# Update the database and website sample content
./dev start
./dev migrate
docker-compose exec django /docker_venv/bin/python3 ./manage.py load_group_roles
./dev sampledata --skip_backdate
./dev raise_backdate_flags
