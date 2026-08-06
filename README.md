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
- История изменения цен
- Управление складом
- Управление поставщиками
- JWT-аутентификация
- Хэширование паролей (Argon2)
- Личный кабинет пользователя
- Изменение логина
- Изменение пароля
- Защита административных страниц
- Современный адаптивный интерфейс

# 🚧 Планируется реализовать
- Управление заказами
- Учёт расходов
- Разграничение ролей
- Панель администратора
- Графики и аналитика

# Структура базы данных
<img width="828" height="604" alt="image" src="https://github.com/user-attachments/assets/84246cac-0810-4257-b2ce-8278ad315ed8" />

# 📸 Интерфейс
<img width="2518" height="1177" alt="image" src="https://github.com/user-attachments/assets/e1e5cb50-701f-4e3a-bf6c-a8fa56c7f59d" />
<img width="2514" height="1171" alt="image" src="https://github.com/user-attachments/assets/692b968c-7c95-47ba-941b-a0bb6198602e" />
<img width="2519" height="1172" alt="image" src="https://github.com/user-attachments/assets/71165432-fcbf-4058-9689-255821243844" />
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
