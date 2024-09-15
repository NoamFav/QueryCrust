#!/bin/bash
# Script to set up the database
echo 'Setting up the database...'
psql -h localhost -U myuser -d mydatabase -a -f src/tables/create_tables.sql
psql -h localhost -U myuser -d mydatabase -a -f src/data/initial_data.sql

