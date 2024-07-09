#!/bin/bash
set -e

# Start the PostgreSQL service in the background
pg_ctl -D "$PGDATA" -o "-c listen_addresses='*'" -w start

# Wait for PostgreSQL to start
until pg_isready -q; do
  echo "Waiting for PostgreSQL to start..."
  sleep 2
done

# Update pg_hba.conf
echo "host    all             all             0.0.0.0/0               trust" >> "$PGDATA/pg_hba.conf"

# Stop PostgreSQL
pg_ctl -D "$PGDATA" -m fast -w stop

# Start PostgreSQL in foreground (this will keep the container running)
exec postgres
