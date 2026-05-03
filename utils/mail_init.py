#  создаем через отдельный файл, чтобы не допустить циклического импорта
from flask_mail import Mail

mail = Mail()  # Создаём объект Mail
