#!/bin/bash
while true; do
    # Check that database is ready
    python3 -c 'import os, sqlalchemy; engine = sqlalchemy.create_engine(os.getenv("DATABASE_URL")); conn = engine.connect()'
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Waiting for database...
    sleep 10
done

exec gunicorn -k gevent -w 4 "api.app:create_app('production')" -b 0.0.0.0:8000