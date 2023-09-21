from flask import Flask, render_template, request
import psycopg2
from decouple import config

# Чтение значений из .env файла
DB_NAME = config('DB_NAME')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
DB_HOST = config('DB_HOST')

app = Flask(__name__)

# Настройки подключения к базе данных PostgreSQL
db_settings = {
    'dbname': DB_NAME,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
}


def create_properties_table():
    conn = psycopg2.connect(**db_settings)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS properties (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                address VARCHAR(255),
                floor INTEGER,
                area FLOAT,
                type VARCHAR(255),
                metro_stations VARCHAR(255)
            )
        """)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = psycopg2.connect(**db_settings)
    cursor = conn.cursor()

    if request.method == 'POST':
        # Получаем значения из формы фильтрации
        min_area = request.form.get('min_area')
        max_floor = request.form.get('max_floor')
        metro_station = request.form.get('metro_station')

        # Пишем SQL-запрос с учетом фильтров
        query = 'SELECT * FROM properties WHERE 1=1'
        params = []

        if min_area:
            query += ' AND area >= %s'
            params.append(float(min_area))

        if max_floor:
            query += ' AND floor <= %s'
            params.append(int(max_floor))

        if metro_station:
            # Приводим введенное значение к нижнему регистру перед сравнением
            # А также приводим значение в базе данных к нижнему регистру
            query += ' AND LOWER(metro_stations) LIKE LOWER(%s)'
            params.append(f'%{metro_station}%')

        cursor.execute(query, params)
    else:
        # Если форма не отправлена, просто получаем все объекты
        cursor.execute('SELECT * FROM properties')

    properties = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', properties=properties)


@app.route('/property/<int:property_id>')
def property_detail(property_id):
    conn = psycopg2.connect(**db_settings)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM properties WHERE id = %s', (property_id,))
    property_data = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('property_detail.html', property=property_data)


if __name__ == '__main__':
    create_properties_table()
    app.run(debug=True)
