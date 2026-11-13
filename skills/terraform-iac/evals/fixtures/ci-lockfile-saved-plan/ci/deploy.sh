#!/bin/sh
# Runs on every merge to main.
set -eu
terraform init -input=false -upgrade
terraform plan -input=false -lock=false -out=tfplan
terraform show -no-color tfplan > plan.txt
terraform apply -input=false -auto-approve
