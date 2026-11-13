#!/bin/sh
set -eu
BACKUP_DIR=/var/backups/db
KEEP=14
find "${BACKUP_DIR}" -name '*.tar.gz' -mtime +${KEEP} -delete
aws s3 ls "s3://db-backups-${region}/${cluster_name}/" | tail -n +${KEEP}
