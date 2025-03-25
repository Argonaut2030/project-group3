# project-group3
Repository for the educational Python project. Start date 10/03/2025


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
