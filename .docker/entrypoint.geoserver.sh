#!/bin/bash

python /tmp/wait_for_postgres.py

# Execute the command passed to the container
exec "$@"