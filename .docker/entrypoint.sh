#!/bin/bash

# Check the hostname and set the appropriate entrypoint script
if [ "$(hostname)" = "app-backend" ]; then
    exec /tmp/entrypoint.backend.sh "$@"
else
    echo "Unknown hostname: $(hostname)"
    exit 1
fi