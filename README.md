# Система управления складом автозапчастей
Данный проект представляет собой веб-приложение для автоматизации учета автозапчастей. Система позволяет управлять пользователями, складом, поставщиками и историей изменения цен.

Проект разработан на FastAPI и PostgreSQL и находится в активной разработке.
# 🎯 Цель проекта
Разработка современной информационной системы учета автозапчастей с использованием Python и FastAPI. Проект основан на курсовой работе, но полностью переписывается с использованием современного стека технологий и новой архитектуры.
# Технологический стек:
- Python.
- FastAPI.
- SQLAlchemy.
- Pydantic.
- PostgreSQL.
- JWT
- Argon2
- HTML
- CSS
- Jinja2
- Git
# ✅ Реализовано
- Авторизация пользователей
- Регистрация пользователей
- JWT-аутентификация
- Хэширование паролей (Argon2)
- Личный кабинет пользователя
- Изменение логина
- Изменение пароля
- Защита административных страниц
- Современный адаптивный интерфейс

# 🚧 Планируется реализовать
- Управление складом
- Управление поставщиками
- Управление заказами
- История изменения цен
- Учёт расходов
- Разграничение ролей
- Панель администратора
- Графики и аналитика

# Структура базы данных
<img width="828" height="604" alt="image" src="https://github.com/user-attachments/assets/84246cac-0810-4257-b2ce-8278ad315ed8" />

# 📸 Интерфейс
<img width="2515" height="1171" alt="image" src="https://github.com/user-attachments/assets/3cf6a9ef-bc04-4dc1-9250-ca3cd0459ae9" />
<img width="2510" height="1222" alt="image" src="https://github.com/user-attachments/assets/3419fdae-db7a-4f6c-849f-6d9acc66ef0e" />
<img width="2515" height="1217" alt="image" src="https://github.com/user-attachments/assets/e14f540f-f74d-450e-8c15-2f26c2ff764b" />
<img width="2521" height="1217" alt="image" src="https://github.com/user-attachments/assets/d3f199d8-741b-49ff-8f52-38d1a04c3e2c" />
<img width="2515" height="1214" alt="image" src="https://github.com/user-attachments/assets/018e85e2-9745-427d-a78f-c53bc4b1c198" />
<img width="2516" height="1221" alt="image" src="https://github.com/user-attachments/assets/eb793268-ff86-413f-9484-fe7f6b9aee48" />





# Установка и запуск
1. **Клонирование репозитория:**
```bash
git clone https://github.com/Artemiyz05/lot-parser.git
cd inventory-management-system
```
2. **Настройка виртуального окружения:**
```bash
python -m venv .venv
source venv/bin/activate  # Для Linux/macOS
```
3. **Установка зависимостей:**
```bash
pip install -r requirements.txt
```
Запуск инструментов:
uvicorn app.main:app --reload
