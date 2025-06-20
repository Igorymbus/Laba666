from django.db import migrations
from django.db import connection

def migrate_data(apps, schema_editor):
    # Получаем курсор для выполнения SQL-запросов
    with connection.cursor() as cursor:
        # Миграция жанров
        cursor.execute("""
            INSERT INTO genres (name)
            SELECT DISTINCT name FROM public.genres
            ON CONFLICT (id) DO NOTHING;
        """)

        # Миграция лейблов
        cursor.execute("""
            INSERT INTO labels (name, country)
            SELECT DISTINCT name, country FROM public.labels
            ON CONFLICT (id) DO NOTHING;
        """)

        # Миграция исполнителей
        cursor.execute("""
            INSERT INTO artists (name, country)
            SELECT DISTINCT name, country FROM public.artists
            ON CONFLICT (id) DO NOTHING;
        """)

        # Миграция альбомов
        cursor.execute("""
            INSERT INTO albums (id, title, release_date, price, label_id, genre_id)
            SELECT id, title, release_date, price, label_id, genre_id 
            FROM public.albums
            ON CONFLICT (id) DO NOTHING;
        """)

        # Миграция связи альбом-исполнитель
        cursor.execute("""
            INSERT INTO album_artists (album_id, artist_id)
            SELECT album_id, artist_id FROM public.album_artists
            ON CONFLICT (album_id, artist_id) DO NOTHING;
        """)

        # Миграция треков
        cursor.execute("""
            INSERT INTO tracks (album_id, title, duration)
            SELECT album_id, title, duration FROM public.tracks
            ON CONFLICT (id) DO NOTHING;
        """)

        # Миграция клиентов
        cursor.execute("""
            INSERT INTO customers (id, first_name, last_name, email, phone, address, city, country, registered_date)
            SELECT id, first_name, last_name, email, phone, address, city, country, registered_date 
            FROM public.customers
            ON CONFLICT (id) DO NOTHING;
        """)

        # Миграция заказов
        cursor.execute("""
            INSERT INTO orders (id, customer_id, order_date, total_amount)
            SELECT id, customer_id, order_date, total_amount 
            FROM public.orders
            ON CONFLICT (id) DO NOTHING;
        """)

        # Миграция позиций заказа
        cursor.execute("""
            INSERT INTO order_items (order_id, album_id, quantity, price_at_purchase)
            SELECT order_id, album_id, quantity, price_at_purchase 
            FROM public.order_items
            ON CONFLICT (id) DO NOTHING;
        """)

        # Миграция сотрудников
        cursor.execute("""
            INSERT INTO employees (id, first_name, last_name, email, phone, position)
            SELECT id, first_name, last_name, email, phone, position 
            FROM public.employees
            ON CONFLICT (id) DO NOTHING;
        """)

        # Миграция продаж
        cursor.execute("""
            INSERT INTO sales (order_id, employee_id, sale_date)
            SELECT order_id, employee_id, sale_date 
            FROM public.sales
            ON CONFLICT (order_id) DO NOTHING;
        """)

        # Миграция платежей
        cursor.execute("""
            INSERT INTO payments (order_id, payment_date, amount, payment_method)
            SELECT order_id, payment_date, amount, payment_method 
            FROM public.payments
            ON CONFLICT (id) DO NOTHING;
        """)

        # Миграция поставщиков
        cursor.execute("""
            INSERT INTO suppliers (id, name, contact_name, phone, email, country)
            SELECT id, name, contact_name, phone, email, country 
            FROM public.suppliers
            ON CONFLICT (id) DO NOTHING;
        """)

        # Миграция поставок
        cursor.execute("""
            INSERT INTO shipments (supplier_id, album_id, quantity, shipment_date)
            SELECT supplier_id, album_id, quantity, shipment_date 
            FROM public.shipments
            ON CONFLICT (id) DO NOTHING;
        """)

        # Миграция склада
        cursor.execute("""
            INSERT INTO inventory (album_id, stock_quantity, last_updated)
            SELECT album_id, stock_quantity, last_updated 
            FROM public.inventory
            ON CONFLICT (album_id) DO NOTHING;
        """)

def reverse_migrate(apps, schema_editor):
    # В случае отката миграции удаляем все данные
    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE inventory CASCADE;")
        cursor.execute("TRUNCATE TABLE shipments CASCADE;")
        cursor.execute("TRUNCATE TABLE suppliers CASCADE;")
        cursor.execute("TRUNCATE TABLE payments CASCADE;")
        cursor.execute("TRUNCATE TABLE sales CASCADE;")
        cursor.execute("TRUNCATE TABLE employees CASCADE;")
        cursor.execute("TRUNCATE TABLE order_items CASCADE;")
        cursor.execute("TRUNCATE TABLE orders CASCADE;")
        cursor.execute("TRUNCATE TABLE customers CASCADE;")
        cursor.execute("TRUNCATE TABLE tracks CASCADE;")
        cursor.execute("TRUNCATE TABLE album_artists CASCADE;")
        cursor.execute("TRUNCATE TABLE albums CASCADE;")
        cursor.execute("TRUNCATE TABLE artists CASCADE;")
        cursor.execute("TRUNCATE TABLE labels CASCADE;")
        cursor.execute("TRUNCATE TABLE genres CASCADE;")

class Migration(migrations.Migration):
    dependencies = [
        ('qwerty', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migrate_data, reverse_migrate),
    ] 