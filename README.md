# Sports Infrastructure Platform

Проект представляет собой информационную систему спортивной инфраструктуры, построенную на базе SQLite, Telegram-бота и FastAPI.

В основе системы находится реляционная база данных, содержащая информацию о спортсменах, тренерах, спортивных клубах, соревнованиях и результатах выступлений. Для работы с данными были разработаны SQL-запросы различной сложности, включая выборки с использованием JOIN, агрегатных функций и группировок.

Для взаимодействия с базой данных реализован Telegram-бот, который позволяет получать информацию о спортсменах, искать призёров соревнований, обновлять спортивные разряды и формировать статистические отчёты непосредственно из мессенджера.

На следующем этапе проект был расширен собственным REST API на FastAPI. API предоставляет доступ к данным спортивной системы через HTTP-запросы и возвращает результаты в формате JSON. Дополнительно Telegram-бот был интегрирован с разработанным API, что позволило использовать единый источник данных для разных клиентов.

## Используемые технологии

- Python
- SQLite
- SQL
- FastAPI
- Uvicorn
- pyTelegramBotAPI
- Requests

## Архитектура проекта

SQLite Database → FastAPI → Telegram Bot / HTTP Client

## Скриншоты. Работа Telegram-бота

#### Команда /start

<img width="912" height="786" alt="изображение" src="https://github.com/user-attachments/assets/c7354405-4dbd-4e38-b57d-5579146551a0" />

#### Добавление спортсмена

<img width="598" height="963" alt="изображение" src="https://github.com/user-attachments/assets/b5978e54-23b1-44a9-b260-e8be5e17ed59" />

#### Получение призёров

<img width="745" height="220" alt="изображение" src="https://github.com/user-attachments/assets/b0caed54-dc2a-41d0-a06f-6eb2774c0f68" />

#### Статистика по клубам

<img width="749" height="253" alt="изображение" src="https://github.com/user-attachments/assets/cac09b76-0c51-4d2d-bd7a-aa3171c55856" />

### Работа эндпоинта FastAPI

<img width="674" height="660" alt="изображение" src="https://github.com/user-attachments/assets/f4750b7b-372b-4612-922a-1ec1ce42568f" />

### Получение данных через API

<img width="630" height="436" alt="изображение" src="https://github.com/user-attachments/assets/79d8178f-7da8-4309-8ead-b2adee290550" />

## Запуск

Сначала необходимо создать базу данных:

```bash
python create_sport_db.py
```

<img width="1064" height="107" alt="изображение" src="https://github.com/user-attachments/assets/1c00bd5d-a456-45b1-b201-f6b812e81601" />

После этого можно запустить API:

```bash
uvicorn api:app --reload
```

И отдельно запустить Telegram-бота:

```bash
python bot.py
```

<img width="1064" height="244" alt="изображение" src="https://github.com/user-attachments/assets/c5c85969-a574-41c6-a695-5485ab337983" />

## Что было реализовано

В рамках проекта были освоены проектирование реляционных баз данных, написание SQL-запросов, создание Telegram-ботов, разработка REST API и интеграция нескольких компонентов в единую клиент-серверную систему.
