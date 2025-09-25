Modernization of the "Hyperion" system at a ceramic tile production enterprise.
python manage.py makemigrations
python manage.py migrate --database=default  # Для .exe бази (але з managed=False нічого не зміниться)
python manage.py migrate --database=zip_db  # Для ЗІП бази