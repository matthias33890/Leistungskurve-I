#!/bin/bash
set -e

# Start the PostgreSQL service in the background
pg_ctl -D /var/lib/postgresql/data start

# Wait for PostgreSQL to start
until pg_isready -q; do
  echo "Waiting for PostgreSQL to start..."
  sleep 2
done

# Update pg_hba.conf
echo "host    all             all             0.0.0.0/0               trust" >> /var/lib/postgresql/data/pg_hba.conf

# Restart PostgreSQL to apply changes
pg_ctl -D /var/lib/postgresql/data restart

# Keep the container running
tail -f /dev/null
