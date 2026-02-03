#!/bin/bash
set -e

if [ -n "$HOST_UID" ]; then

  useradd -u "$HOST_UID" -o -m appuser

  chown -R appuser /app

  exec gosu appuser "$@"

else

  exec "$@"

fi
