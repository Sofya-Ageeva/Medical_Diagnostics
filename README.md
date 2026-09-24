# 🏥 Сайт компании медицинской диагностики

Дипломный проект — веб-приложение для медицинской диагностической компании
с возможностью онлайн-записи на приём, управления услугами и врачами,
email-уведомлениями и личным кабинетом пациента.

---

## 📖 Описание проекта

**Медицинская диагностика** — веб-приложение для компании, предоставляющей
медицинские диагностические услуги. Проект позволяет:

- Пациентам записываться на приём онлайн
- Врачам получать уведомления о новых записях
- Администраторам управлять услугами, врачами, слотами и контентом сайта
- Отправлять email-уведомления о записях и напоминания

---

## 🎯 Функционал

### 👤 Для пациентов

- ✅ Регистрация и авторизация (по email)
- ✅ Просмотр каталога услуг с поиском и фильтрацией
- ✅ Просмотр врачей с фильтром по специализации
- ✅ Онлайн-запись на приём с выбором доступного времени
- ✅ Личный кабинет с историей записей
- ✅ Просмотр деталей приёма
- ✅ Просмотр результатов диагностики
- ✅ Отмена записи
- ✅ Email-уведомления о создании записи
- ✅ Напоминание за день до приёма

### 🩺 Для врачей

- ✅ Email-уведомления о новых записях

### 🔧 Для администраторов

- ✅ Управление пользователями
- ✅ Управление услугами и категориями
- ✅ Управление врачами и специализациями
- ✅ Управление рабочим графиком врачей
- ✅ Управление доступным временем приёма (слоты) с генерацией на неделю
- ✅ Управление записями на приём
- ✅ Управление результатами диагностики
- ✅ Управление контентом сайта (о компании, преимущества, карта)
- ✅ Просмотр заявок обратной связи

### 📧 Email-уведомления

- ✅ Письмо пациенту при создании записи
- ✅ Письмо врачу о новой записи
- ✅ Напоминание пациенту за день до приёма

---

## 🛠 Технологии

| Компонент | Технология |
|-----------|-----------|
| **Бэкенд** | Django 5.0.6 |
| **База данных** | PostgreSQL 15 (продакшен и Docker) |
| **Фронтенд** | Bootstrap 5, HTML5, CSS3, JavaScript |
| **Email** | SMTP (Gmail) |
| **Контейнеризация** | Docker, Docker Compose |
| **Веб-сервер** | Nginx + Gunicorn |
| **CI/CD** | GitHub Actions |
| **Тестирование** | Django TestCase, Coverage (82%) |

---

## 📁 Структура проекта

```
Medical_Diagnostics/
├── config/                  # Настройки Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                   # Пользователи (кастомная модель User)
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── services/                # Услуги и категории
├── doctors/                 # Врачи, специализации, графики, слоты
├── appointments/            # Записи, заявки, результаты диагностики
├── main/                    # Главная, о компании, контакты
├── templates/               # HTML-шаблоны
├── static/                  # CSS, JS, изображения
├── media/                   # Загруженные файлы (аватарки, результаты)
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── requirements.txt
├── .env.template
└── README.md
```

---

## 🚀 Установка и запуск через Docker

### Требования

- **Docker** и **Docker Compose** (Docker Desktop для Mac/Windows)
- **Git**
- Свободный порт **82**

### Шаг 1. Клонирование репозитория

```bash
git clone https://github.com/Sofya-Ageeva/Medical_Diagnostics.git
cd Medical_Diagnostics
```

### Шаг 2. Настройка переменных окружения

Скопируйте `.env.template` в `.env` и заполните своими данными:

```bash
cp .env.template .env
```

### Шаг 3. Запуск контейнеров

```bash
docker compose up -d --build
```

### Шаг 4. Применение миграций

```bash
docker compose exec web python manage.py migrate
```

### Шаг 5. Сбор статики

```bash
docker compose exec web python manage.py collectstatic --noinput
```

### Шаг 6. Создание суперпользователя

```bash
docker compose exec web python manage.py createsuperuser
```

---

## 🌐 Доступ

- **Сайт:** http://localhost:82/
- **Админка:** http://localhost:82/admin/

---

##  Переменные окружения (`.env`)

| Переменная | Описание | Пример |
|-----------|----------|--------|
| `SECRET_KEY` | Секретный ключ Django | `django-insecure-xxxxx` |
| `DEBUG` | Режим отладки | `False` (в Docker) |
| `ALLOWED_HOSTS` | Разрешённые хосты (через запятую) | `localhost,127.0.0.1,web` |
| `DB_NAME` | Имя базы данных | `medical_db` |
| `DB_USER` | Пользователь БД | `postgres` |
| `DB_PASSWORD` | Пароль БД | `your_password` |
| `DB_HOST` | Хост БД | `db` (для Docker) |
| `DB_PORT` | Порт БД | `5432` |
| `EMAIL_HOST` | SMTP-сервер | `smtp.gmail.com` |
| `EMAIL_PORT` | Порт SMTP | `587` |
| `EMAIL_USE_TLS` | Использовать TLS | `True` |
| `EMAIL_HOST_USER` | Email отправителя | `your_email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | App Password Gmail | `xxxx xxxx xxxx xxxx` |
| `DEFAULT_FROM_EMAIL` | Email «От кого» | `your_email@gmail.com` |

> 💡 **App Password Gmail:** получите на https://myaccount.google.com/apppasswords
> (требуется двухэтапная аутентификация).

---

## 🧪 Тестирование

### Запуск тестов

```bash
# Локально (в venv)
python manage.py test

# В Docker
docker compose exec web python manage.py test
```

### Покрытие кода

```bash
# Локально
coverage run --source='.' manage.py test
coverage report

# В Docker
docker compose exec web coverage run --source='.' manage.py test
docker compose exec web coverage report
```

---

## 🐳 Полезные команды Docker

```bash
# Остановить контейнеры
docker compose down

# Остановить и удалить тома (сброс БД)
docker compose down -v

# Пересобрать без кеша
docker compose build --no-cache

# Посмотреть логи
docker compose logs -f

# Войти в контейнер
docker compose exec web bash

# Проверить статус
docker compose ps
```

---

## 🔄 CI/CD (GitHub Actions)

Workflow автоматически при push в `main`, `develop` и `feature/*`:

- Запускает тесты с покрытием;
- Проверяет код через flake8;
- Собирает Docker-образ.

Secrets для деплоя: `SERVER_HOST`, `SERVER_USER`, `SERVER_SSH_KEY`.


