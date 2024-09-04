## Описание

Решение 1 задания находится в файле task_1.py

Решения 2 задания вынесены в отдельные файлы. Метод 1 в файле task_2_1.py и Метод 2 в файле task_2_2.py

Также реализовано приложение на Django для проверки работоспособности методов. В приложение добавлен импорт тестовых данных для удобства проверки

## Автор проекта

[Beliaev Mikhail](https://github.com/tooMike) – [Telegram](https://t.me/gusoyn)

## Установка и запуск Django приложения с Docker

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Gazprom-team-6/backend/
```

```
cd backend
```

Запустить сборку проекта (для запуска необходимо добавить файл с секретами .env):

```
docker compose up
```

Выполнить сбор статики в контейнере backend:

```
docker compose exec backend python manage.py collectstatic
```

Выполнить миграции в контейнере backend:

```
docker compose exec backend python manage.py migrate
```

Проект будет доступен по адресу:

```
http://localhost:8000/
```

Скачивание CSV файла будет доступно по адресу:

```
http://localhost:8000/get_csv/
```
