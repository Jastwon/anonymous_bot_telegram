# 🤖 Anonymous Telegram Bot

**Anonymous Telegram Bot** — это бот для Telegram, позволяющий пользователям отправлять анонимные сообщения другим пользователям.
Проект включает в себя бота, базу данных для хранения информации и файл конфигурации для развертывания.

## 🚀 Функциональность

- Отправка анонимных сообщений другим пользователям Telegram.
- Хранение сообщений в базе данных.
- Возможность развертывания на Heroku с использованием Procfile.

## 🧱 Структура проекта

```
anonymous_bot_telegram/
├── __pycache__/        # Кэшированные файлы Python
├── db/                 # База данных
├── bot.py              # Основной файл бота
├── database.py         # Работа с базой данных
├── requirements.txt    # Зависимости проекта
├── Procfile            # Конфигурация для Heroku
└── README.md           # Документация проекта
```

## ⚙️ Установка и запуск

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/Jastwon/anonymous_bot_telegram.git
   cd anonymous_bot_telegram
   ```

2. **Создайте виртуальное окружение и активируйте его:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Unix
   venv\Scripts\activate   # Для Windows
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Запустите бота:**
   ```bash
   python bot.py
   ```

## 🛠️ Используемые технологии

- **Python** — основной язык программирования.
- **SQLite** — база данных для хранения сообщений.
- **Heroku** — платформа для развертывания приложения.


---

Если у вас есть дополнительные вопросы или предложения по улучшению проекта, не стесняйтесь создавать [issues](https://github.com/Jastwon/anonymous_bot_telegram/issues) или отправлять [pull requests](https://github.com/Jastwon/anonymous_bot_telegram/pulls).
