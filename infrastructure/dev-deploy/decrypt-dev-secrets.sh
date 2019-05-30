#!/bin/bash

# Decrypt secret files archive that contain credentials.
#
# This includes:
#   - Google Cloud Platform Service Account for using gcloud.
#   - Script to load environment variables used for running Django on development server.
openssl aes-256-cbc -K "${encrypted_3d841ac803f7_key}" -iv "${encrypted_3d841ac803f7_iv}" -in ./infrastructure/dev-deploy/dev-deploy-secrets.tar.enc -out ./codewof/dev-deploy-secrets.tar -d

# Unzip the decrypted secret archive.
tar -C ./codewof/ -xf ./codewof/dev-deploy-secrets.tar
