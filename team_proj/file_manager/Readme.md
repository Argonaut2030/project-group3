# File Manager

## Опис
`file_manager` — це додаток Django для завантаження, збереження та управління файлами в AWS S3. Файли зберігаються у вигляді:

```
S3 Bucket /
    user_{id}/
        images/
        videos/
        audio/
        documents/
```

## Функціональність
- **Завантаження файлів**: Користувачі можуть завантажувати файли через форму.
- **Автоматичне сортування**: Файли зберігаються в категоріях (`images`, `videos`, `audio`, `documents`) на основі їх розширення.
- **Фільтрація**: Користувачі можуть переглядати файли за категоріями.

## Налаштування AWS S3

Файл `settings.py` містить наступні налаштування для підключення до S3:

```python
AWS_ACCESS_KEY_ID = "your-access-key"
AWS_SECRET_ACCESS_KEY = "your-secret-key"
AWS_STORAGE_BUCKET_NAME = "your-bucket-name"
AWS_S3_REGION_NAME = "your-region"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

AWS_S3_FILE_OVERWRITE = False

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
    }
}
```

### Пояснення:
- **`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`** — ключі доступу до AWS S3.
- **`AWS_STORAGE_BUCKET_NAME`** — ім'я S3-бакета, де зберігаються файли.
- **`AWS_S3_REGION_NAME`** — регіон S3, де знаходиться бакет.
- **`AWS_S3_CUSTOM_DOMAIN`** — кастомний домен для доступу до файлів у S3.
- **`AWS_S3_FILE_OVERWRITE`** — встановлює перепис файлів на заборону
- **`STORAGES`** — встановлює S3 як сховище для медіафайлів.




## Модель `UploadedFile`
Файл `models.py` містить модель `UploadedFile`, яка визначає структуру збереження файлів.

### Пояснення моделі:
- **`user`** — ForeignKey, що зв'язує файл із користувачем.
- **`file`** — поле для файлу, яке використовує `user_directory_path` для визначення шляху.
- **`uploaded_at`** — автоматично зберігає дату завантаження файлу.
- **`user_directory_path`** — функція, яка сортує файли за категоріями.

## Views у `views.py`
Файл `views.py` містить функції для завантаження та відображення файлів.

### Пояснення Views:
- **`upload_file`** — дозволяє користувачам завантажувати файли.
  - Якщо `POST`, зберігає файл, прив'язуючи його до користувача.
  - Якщо `GET`, відображає форму для завантаження файлу.
- **`list_files`** — показує список файлів користувача з можливістю фільтрації за категоріями.
  - Використовує `GET`-параметр `category` для фільтрації за папками (`images`, `videos`, `audio`, `documents`).

## Як використовувати

### 1. Встановлення залежностей
```sh
pip install django-storages boto3
```

### 2. Налаштування `.env`
Створи `.env` файл і додай:
```ini
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=your-region
```
### 3. Переконайтеся що ваша база даних працює


