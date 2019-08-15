#!/bin/bash

# Decrypt secret files archive that contain credentials.
#
# This includes:
#   - Google Cloud Platform Service Account for using gcloud.
#   - Script to load environment variables used for running Django on production server.
openssl aes-256-cbc -K "${encrypted_df5e7fd79851_key}" -iv "${encrypted_df5e7fd79851_iv}" -in ./infrastructure/prod-deploy/prod-deploy-secrets.tar.enc -out ./codewof/prod-deploy-secrets.tar -d

# Unzip the decrypted secret archive.
tar -C ./codewof/ -xf ./codewof/prod-deploy-secrets.tar
