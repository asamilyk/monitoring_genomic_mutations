#!/bin/bash

# Создание суперпользователя Django
echo "Создание администратора..."

# Ждем готовности базы данных
python manage.py shell << EOF
import django
django.setup()

from django.contrib.auth.models import User

# Проверяем, существует ли уже пользователь admin
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@admin.ru',
        password='admin'
    )
    print("Суперпользователь 'admin' успешно создан!")
    print("Username: admin")
    print("Password: admin") 
    print("Email: admin@admin.ru")
else:
    print("Пользователь 'admin' уже существует")
EOF

echo "Готово!" 