#!/bin/sh
# wait-for-postgres.sh
# проверяет готовность бд к миграциям
# Скрипт в цикле будет пробовать подключаться к базе данных и, когда произойдёт удачное
# подключение, совершит выход из бесконечного цикла.
set -e
host="$1"
shift
cmd="$@"
until PGPASSWORD="n12345" psql -h "$host" -d "webnotes_db" -U "n" -c '\q';
do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
>&2 echo "Postgres is up - executing command"
exec $cmd