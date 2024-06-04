#!/bin/sh

# create database schema
set -e

echo "Initializing database schema..."

# Run the SQL script to list tables
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /docker-entrypoint-initdb.d/init-schema.sql

echo "Schema initialization completed."