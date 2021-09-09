#!/bin/bash

set -e

# Check for environment variables
checkEnvVariableExists() {
    if [ -z ${!1} ]
    then
        echo "ERROR: Define $1 environment variable."
        exit 1
    else
        echo "INFO: $1 environment variable found."
    fi
}
checkEnvVariableExists CODEWOF_IMAGE_TAG
checkEnvVariableExists CODEWOF_DOMAIN

docker stack deploy codewof -c docker-compose.prod.yml
docker service scale codewof_task-update-data=1 codewof_task-raise-backdate-flags=1
