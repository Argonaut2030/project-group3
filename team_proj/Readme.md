# **Гайд: Запуск MinIO, Redis та PostgreSQL через Docker Compose**

## **1. Опис сервісів**
### **MinIO (S3-совісний сховище)**
- Працює на портах `9000` (API) та `9001` (Web UI).
- Використовує змінні оточення `MINIO_ROOT_USER` і `MINIO_ROOT_PASSWORD` для автентифікації.
- Дані зберігаються у `minio_data`.

### **Redis (Кешування та черги)**
- Працює на порту `6379`.
- Використовує `appendonly yes`, щоб зберігати дані між перезапусками.
- Дані зберігаються у `redis_data`.

### **PostgreSQL (Реляційна БД)**
- Працює на порту `5432`.
- Використовує змінні оточення `DB_NAME`, `DB_USER`, `DB_PASSWORD` для налаштування БД.
- Дані зберігаються у `postgres_data`.

---

## **2. Налаштування змінних оточення**
Перед запуском потрібно створити `.env` файл у цій самій директорії:

```ini
# .env
MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=supersecretpassword

DB_NAME=mydatabase
DB_USER=myuser
DB_PASSWORD=mypassword
```

> ⚠️ **Не зберігай цей файл у репозиторії, щоб уникнути витоку даних!**  
> Додай його в `.gitignore`.

---

## **3. Запуск контейнерів**
Щоб запустити всі сервіси, виконай:

```bash
docker-compose up -d
```

- `-d` запустить у фоновому режимі.

Щоб перевірити статус контейнерів:

```bash
docker ps
```

---

## **4. Доступ до сервісів**
- **MinIO Web UI:** [http://localhost:9001](http://localhost:9001)  
  Логін та пароль – з `.env`.
- **MinIO API (S3):** `http://localhost:9000`
- **Redis:** `redis://localhost:6379`
- **PostgreSQL:** `postgres://myuser:mypassword@localhost:5432/mydatabase`

---

## **5. Використання в Django**
### **Підключення PostgreSQL**
У `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### **Підключення MinIO до Django через `django-storages`**
Встанови бібліотеку:
```bash
pip install django-storages[boto3]
```

У `settings.py` додай:
```python
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_ENDPOINT_URL = "http://localhost:9000"
AWS_ACCESS_KEY_ID = os.getenv("MINIO_ROOT_USER")
AWS_SECRET_ACCESS_KEY = os.getenv("MINIO_ROOT_PASSWORD")
AWS_STORAGE_BUCKET_NAME = "mybucket"  # Спочатку створи цей бакет у MinIO UI
```

### **Підключення Redis у Django через `django-redis`**
Встанови бібліотеку:
```bash
pip install django-redis
```

У `settings.py` додай:
```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

---

## **6. Завершення роботи**
Щоб зупинити всі контейнери:
```bash
docker-compose down
```

Якщо потрібно видалити всі дані:
```bash
docker-compose down -v
```