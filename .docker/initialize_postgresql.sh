#!/bin/sh
set -e

# Initialize postgres database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f /tmp/initialize_postgresql/init.sql

# List your additional databases here
DATABASES=("$POSTGRES_DB_BACKEND" "$POSTGRES_DB_GEOSERVER")

# Loop through and create each database
for db in "${DATABASES[@]}"; do
  echo "Creating database: $db"
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE $db;
EOSQL
  echo "Database $db created successfully"
done

# Initialize the django database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB_BACKEND" -f /tmp/initialize_postgresql/backend.sql


# Initialize the geoserver database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB_GEOSERVER" -f /tmp/initialize_postgresql/geoserver.sql

# Add test data to the geoserver database
if [ "$TEST_DATA" = "True" ]; then
  for sql_file in /tmp/test_data_database/*.sql;
  do
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB_GEOSERVER" -f "$sql_file"
  done
fi
