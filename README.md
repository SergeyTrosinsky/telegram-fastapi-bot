# Sports Infrastructure Platform

Проект представляет собой информационную систему спортивной инфраструктуры, построенную на базе SQLite, Telegram-бота и FastAPI.

В основе системы находится реляционная база данных, содержащая информацию о спортсменах, тренерах, спортивных клубах, соревнованиях и результатах выступлений. Для работы с данными были разработаны SQL-запросы различной сложности, включая выборки с использованием JOIN, агрегатных функций и группировок.

Для взаимодействия с базой данных реализован Telegram-бот, который позволяет получать информацию о спортсменах, искать призёров соревнований, обновлять спортивные разряды и формировать статистические отчёты непосредственно из мессенджера.

На следующем этапе проект был расширен собственным REST API на FastAPI. API предоставляет доступ к данным спортивной системы через HTTP-запросы и возвращает результаты в формате JSON. Дополнительно Telegram-бот был интегрирован с разработанным API, что позволило использовать единый источник данных для разных клиентов.

## Используемые технологии
* Python
* SQLite
* SQL
* FastAPI
* Uvicorn
* pyTelegramBotAPI
* Requests

## Архитектура проекта

`SQLite Database → FastAPI → Telegram Bot / HTTP Client`

Проект разделен на три независимых слоя. Telegram-бот выступает в роли интерфейса для пользователя и не общается с базой данных напрямую - вместо этого он отправляет HTTP-запросы к REST API. FastAPI выступает в роли бэкенд-сервера, который принимает запросы, валидирует данные и через модуль db_operations выполняет транзакции в SQLite

Схема БД:

<img width="912" height="786" alt="изображение" src="https://github.com/user-attachments/assets/23a12ed3-154a-4e3c-b64f-a759b6bf5e6d" />

---

## Скриншоты. Работа Telegram-бота

### Команда /start

<img width="598" height="963" alt="изображение" src="https://github.com/user-attachments/assets/220e91e6-c7f8-4a57-aceb-700247f6d3a7" />

### Добавление спортсмена

<img width="745" height="220" alt="изображение" src="https://github.com/user-attachments/assets/61dd7978-4651-48b4-b28d-3727cbca9dfb" />

### Получение призёров

<img width="749" height="253" alt="изображение" src="https://github.com/user-attachments/assets/f5f04286-0efd-466c-b3ee-e0bd3cee8c2e" />

### Статистика по клубам

<img width="720" height="337" alt="изображение" src="https://github.com/user-attachments/assets/7479589b-031c-4fab-b916-bec23a56290d" />

### Работа эндпоинта FastAPI

<img width="674" height="660" alt="изображение" src="https://github.com/user-attachments/assets/99a9506f-7364-4118-9bca-7964a3801395" />

### Получение данных через API

<img width="630" height="436" alt="изображение" src="https://github.com/user-attachments/assets/6a3750db-c17b-4fa7-a9c1-86956e847db1" />

---

## Запуск

Сначала необходимо создать базу данных:

```bash
python create_sport_db.py
```

<img width="1064" height="107" alt="изображение" src="https://github.com/user-attachments/assets/a2dc056d-d950-408c-b2dc-5f8ec91adfd6" />

После этого можно запустить API:

```bash
uvicorn api:app --reload
```

И отдельно запустить Telegram-бота:

```bash
python bot.py
```

<img width="1064" height="244" alt="изображение" src="https://github.com/user-attachments/assets/8060fde4-fcfb-4621-96a4-28511eaf61fd" />

## Что было реализовано

В рамках проекта были освоены проектирование реляционных баз данных, написание SQL-запросов, создание Telegram-ботов, разработка REST API и интеграция нескольких компонентов в единую клиент-серверную систему.
