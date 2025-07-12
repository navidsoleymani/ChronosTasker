#!/bin/sh

# ------------------------------------------------------------------
# Entrypoint Script for Django + PostgreSQL Docker Environment
# ------------------------------------------------------------------
# This script waits until PostgreSQL is ready to accept connections,
# and then proceeds to execute the command passed by the container.
# ------------------------------------------------------------------

echo "Waiting for PostgreSQL to be available..."

# Wait until PostgreSQL is accessible on the specified host and port
while ! nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
  sleep 0.5
done

echo "PostgreSQL is up - continuing with execution."

# Execute the command passed to the container (e.g. runserver or migrate)
exec "$@"
