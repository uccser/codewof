#!/bin/bash

docker service create \
    --name codewof_update-data \
    --detach \
    --mode replicated-job \
    --label traefik.enable=false \
    --network codewof_backend \
    --constraint node.role==worker \
    --constraint node.labels.role==apps \
    --env POSTGRES_HOST="postgres" \
    --env=POSTGRES_PORT="5432" \
    --env=DEPLOYMENT_ENVIRONMENT_FILE="/codewof_deployment_environment" \
    --env=DJANGO_SECRET_KEY_FILE="/run/secrets/codewof_django_secret_key" \
    --env=POSTGRES_DB_FILE="/run/secrets/codewof_postgres_db" \
    --env=POSTGRES_USER_FILE="/run/secrets/codewof_postgres_user" \
    --env=POSTGRES_PASSWORD_FILE="/run/secrets/codewof_postgres_password" \
    --config codewof_deployment_environment \
    --secret codewof_django_secret_key \
    --secret codewof_postgres_db \
    --secret codewof_postgres_user \
    --secret codewof_postgres_password \
    --restart-condition none \
    ghcr.io/uccser/codewof:develop python ./manage.py update_data
