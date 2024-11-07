#!/bin/bash
# Ждём, пока MySQL станет доступен
until mysql -u root -p12345 -e "SELECT 1" &> /dev/null; do
  echo "Ожидание запуска MySQL..."
  sleep 2
done

# Проверка существования таблицы
if ! mysql -u root -p12345 -e "USE std_2414_exam; SHOW TABLES;" | grep -q "books"; then
  echo "Таблица не найдена, выполняется импорт..."
  mysql -u root -p12345 std_2414_exam < /docker-entrypoint-initdb.d/database.sql
else
  echo "Таблица уже существует, импорт не требуется."
fi
