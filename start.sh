#!/bin/bash
cd rezistorka # Your app working directory
export PORT=8080
export PYTHONNOUSERSITE=1  # Отключает user site-packages
export PIP_USER=false
# Очищаем старую проблемную venv если есть
if [ -d "venv" ]; then
    echo "Removing old venv with system packages conflict..."
    rm -rf venv
fi

# Создаем ЧИСТОЕ виртуальное окружение (без --system-site-packages)
echo "Creating fresh virtual environment..."
python3 -m venv venv

# Активируем
source venv/bin/activate

# Обновляем pip, setuptools, wheel
echo "Upgrading pip tools..."
pip install --no-cache-dir --upgrade pip setuptools wheel

# Устанавливаем зависимости
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install --no-cache-dir -r requirements.txt
fi

echo "Starting application..."
python3 main.py