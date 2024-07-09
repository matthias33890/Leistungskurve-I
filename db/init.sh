#!/bin/bash
set -e

# Initialize the database cluster if it does not exist
if [ ! -s "$PGDATA/PG_VERSION" ]; then
  echo "Initializing database..."
  initdb -D "$PGDATA"
fi

# Update pg_hba.conf to trust all connections
echo "host    all             all             0.0.0.0/0               trust" >> "$PGDATA/pg_hba.conf"

# Start the PostgreSQL service in the background
pg_ctl -D "$PGDATA" -o "-c listen_addresses='*'" -w start

# Wait for PostgreSQL to start
until pg_isready -q; do
  echo "Waiting for PostgreSQL to start..."
  sleep 2
done

# Execute the setup SQL script
psql -U postgres -f /docker-entrypoint-initdb.d/setup.sql

# Stop PostgreSQL
pg_ctl -D "$PGDATA" -m fast -w stop

# Start PostgreSQL in foreground (this will keep the container running)
exec postgres