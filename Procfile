# Запуск Django сервера (Web Service)
web: gunicorn FlowerShop.wsgi:application --bind 0.0.0.0:$PORT

# Запуск Telegram бота как фоновый процесс (Background Worker)
worker: python run_bot.py