#!/bin/bash
set -e

echo "=== [predeploy] collectstatic 실행 ==="
cd /var/app/staging/backend
source /var/app/venv/*/bin/activate
python manage.py collectstatic --noinput
echo "=== [predeploy] collectstatic 완료 ==="
