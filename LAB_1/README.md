# 1 Лабораторная работа

## 1 Часть. Dockerfile

Для примера расмотрен Dockerfile в котором прописаны инструкции для сборки образа, отвечающего за запуск NGINX сервера и раздачу статических файлов.

### Плохой файл

```docker
FROM ubuntu:latest 

RUN apt-get update 
RUN apt-get install nginx vim curl wget net-tools telnet openssh-server -y

ENV ADMIN_PASSWORD=12345

COPY . /var/www/html/

EXPOSE 80 22

CMD ["nginx", "-g", "daemon off;"]
```


В "плохом" dockerfile привидены следующие ошибки:

1) Использование Ubuntu: использование громоздких дистрибутивов замедляет время сборки образа и запуска контейнера, создает дополнительные угрозы, т.к. чем больше в образе программ, тем больше потенциальных уязвимостей.

2) Использование latest версии: при последующий сборках образа поведение может менятся, т.к. может поменятся устройство дистрибутива.

3) НЕ использование готового образа: в данном примере правильным подходом было бы использование готового образа (например nginx:alpine)

4) Небезопасное использование `COPY`: в данном примере во время сборки будет скопировано все содержимое папки, в том числе секретные данные.

5) Открытие ненужных портов: `EXPOSE` сама по себе не открывает порты, но в некоторых случаях может (например: `docker run -P myimage`). Это приводит к лишним потенциальным уязвимостям

6) Хранение секретов в dockerfile: высокий риск случайно выложить секрет на github.

### Хороший файл

```docker
FROM nginx:1.24.0-alpine

COPY html/ /var/www/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

Данные ошибки были исправлены:

1) (1-3 проблемы) Вместо ubuntu:latest используется nginx:1.24.0-alpine

2) Добавлен .dockerignore файл + статические файлы вынесены в отдельный каталог

3) Используются только необходимые порты

4) Переменные окружения не хранятся в dockerfile

### Bad practice по работе с контейнером

1) Отсутствие ограничений ресурсов: не ограничивая контейнеры в ресурсах, они могут забирать слишком большое количество ресурсов и препятствовать стабильной работе хоста
Пример: `docker run myapp`

2) Передача секретов напрямую `docker run -e API_KEY="key_123123123" myapp`: так запись сохранится в логах

## 2 Часть. Docker-Compose

### Плохая версия

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: myapp
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/myapp
    depends_on:
      - db
    volumes:
      - .:/app
      - /:/host

volumes:
  postgres_data:
```

Ошибки:

1) Секреты прописаны в файле

2) Отсутствуют ограничения по ресурсам

3) Не указаны конкретные версии образов

4) Отсутствует healthcheck

### Хорошая версия 

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 5s
      timeout: 5s
      retries: 5

  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: ${DATABASE_URL}
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/app

volumes:
  postgres_data:
```

Исправления:

1) Серкеты передаются через файл

2) Добавлены ограничения по ресурсам

3) Добавлен healthcheck для БД

4) Удалено монтирование файловой системы хоста

### Изоляция контейнеров по сети

Далее файл docker-compose был изменен так, чтобы контейнеры не видели друг друга по сети. Для этого каждому из контейнеров была назначена своя сеть.

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - db_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 5s
      timeout: 5s
      retries: 5

  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: ${DATABASE_URL}
    volumes:
      - .:/app
    networks:
      - app_network

volumes:
  postgres_data:

networks:
  db_network:
    driver: bridge
    internal: false
  app_network:
    driver: bridge
    internal: false
```