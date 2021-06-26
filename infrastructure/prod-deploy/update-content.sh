#!/bin/bash

source ./infrastructure/prod-deploy/load-prod-deploy-config-envs.sh

# Updates the database for the production system
cp ./infrastructure/cloud-sql-proxy/docker-compose.yml ./docker-compose.yml

# Decrypt secret files archive that contain credentials.
./infrastructure/prod-deploy/decrypt-prod-secrets.sh

# Load environment variables.
source ./codewof/load-prod-envs.sh

# Update the database and website sample content
./dev start
./dev migrate
docker-compose exec django /docker_venv/bin/python3 ./manage.py load_user_types
docker-compose exec django /docker_venv/bin/python3 ./manage.py load_group_roles
./dev load_questions
./dev load_style_errors
./dev load_achievements
./dev raise_backdate_flags
