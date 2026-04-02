# URL Shortener

Простой сервис сокращения ссылок на **FastAPI** с хранением данных в **PostgreSQL**.

Проект умеет:
- создавать короткие ссылки;
- автоматически добавлять `https://`, если пользователь вводит только домен;
- редиректить по короткому коду;
- хранить ссылки в базе данных;
- отображать список всех ссылок в HTML-странице;
- запускаться локально и через Docker Compose.

---

## Возможности

- Создание короткой ссылки через API
- HTML-интерфейс для создания ссылок
- Страница со списком всех сохраненных ссылок
- Хранение данных в PostgreSQL
- Подсчет количества переходов по ссылке
- Кнопка копирования короткой ссылки
- Запуск через Docker Compose

---

## Стек

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Jinja2
- JavaScript
- Docker
- Docker Compose



## Структура проекта

~~~text
url_shortener/
├── app/
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── schemas.py
│   └── utils.py
├── templates/
│   ├── index.html
│   └── links.html
├── static/
│   ├── style.css
│   └── script.js
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── .env.docker
└── README.md
~~~

---

## Как это работает

1. Пользователь вводит длинную ссылку на главной странице
2. Сервис нормализует URL
3. Генерируется короткий код
4. Ссылка сохраняется в PostgreSQL
5. Пользователь получает короткий URL
6. При переходе по короткому URL происходит редирект на оригинальную ссылку
7. Количество переходов увеличивается

---

## Запуск локально

### 1. Клонировать репозиторий

```bash
git clone <URL_РЕПОЗИТОРИЯ>
cd url_shortener
```

### 2. Создать виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Настроить `.env`

Пример:

```env
POSTGRES_DB=urlshortener
POSTGRES_USER=urluser
POSTGRES_PASSWORD=urlpass
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 5. Подготовить PostgreSQL

Нужно, чтобы база и пользователь существовали.

Пример команд:

```sql
CREATE USER urluser WITH PASSWORD 'urlpass';
CREATE DATABASE urlshortener OWNER urluser;
GRANT ALL PRIVILEGES ON DATABASE urlshortener TO urluser;
```

### 6. Запустить приложение

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

После запуска приложение будет доступно по адресам:
- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/links-page`

---

## Запуск через Docker Compose

### 1. Настроить `.env.docker`

Пример:

```env
POSTGRES_DB=urlshortener
POSTGRES_USER=urluser
POSTGRES_PASSWORD=urlpass
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### 2. Запустить контейнеры

```bash
docker compose up --build
```

### 3. Открыть приложение

- `http://localhost:8000/`
- `http://localhost:8000/docs`
- `http://localhost:8000/links-page`

---

## Основные маршруты

### HTML
- `GET /` — главная страница
- `GET /links-page` — страница со всеми ссылками

### API
- `GET /health` — проверка состояния сервиса
- `POST /shorten` — создать короткую ссылку
- `GET /links` — получить все ссылки в JSON
- `GET /{code}` — редирект на оригинальную ссылку

---

## Пример запроса

```bash
curl -X POST "http://127.0.0.1:8000/shorten" \
-H "Content-Type: application/json" \
-d '{"url":"google.com"}'
```

Пример ответа:

```json
{
  "original_url": "https://google.com",
  "short_code": "Ab12Cd",
  "short_url": "http://127.0.0.1:8000/Ab12Cd"
}
```


