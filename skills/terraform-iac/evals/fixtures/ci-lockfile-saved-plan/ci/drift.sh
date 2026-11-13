#!/bin/sh
# Nightly: report changes made outside terraform.
set -eu
terraform init -input=false
terraform plan -input=false -detailed-exitcode
if [ $? -eq 2 ]; then
  echo DRIFT
fi
