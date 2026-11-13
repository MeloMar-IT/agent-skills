#!/bin/sh
set -eu
BACKUP_DIR=/var/backups/db
DATE=$(date +%Y%m%d-%H%M)
pg_dump "${DATABASE_URL}" > "${BACKUP_DIR}/${DATE}.sql"
tar -czf "${BACKUP_DIR}/${DATE}.tar.gz" -C "${BACKUP_DIR}" "${DATE}.sql"
aws s3 cp "${BACKUP_DIR}/${DATE}.tar.gz" "s3://db-backups-${region}/${cluster_name}/"
