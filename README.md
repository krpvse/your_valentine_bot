Запуск приложения / для разработчиков
----------------------------------------
**1. Установка зависимостей:** pip install -r requirements.txt

**2. Запуск бота:** python3 main.py

Описание функционала Telegram-бота / что может пользователь
----------------------------------------
Бот для анонимного получения валентинок на праздник 14 февраля - День Валентина

Как пользоваться ботом?
1. Запустить бот командой /start
2. Создать профиль, который будут видеть люди - нужно написать свое имя, придумать описание и загрузить фото
3. Получить персональную ссылку, по которой люди будут переходить и оставлять валентинки

Логика программы / как это работает
----------------------------------------

Основные технологии и библиотеки: python3.10, aiogram2.23.1, sqlite3, asyncio

**Всю работу бота можно разделить на 2 логических направления:**
1. Работа с собственным профилем - редактирование имени, описания и фото, получение персональной ссылки и просмотр своих валентинок
2. Отправка валентинок другим людям

Важно! Пользователь не может получить ссылку на профиль, пока не заполнит его.

