import psycopg2
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'classic_library',
    'user': 'postgres',
    'password': 'OAhd112'
}

def connect_to_db():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None

def show_menu():
    print("\n" + "=" * 50)
    print("       БИБЛИОТЕКА КЛАССИЧЕСКИХ КНИГ")
    print("=" * 50)
    print("1. Показать все книги")
    print("2. Показать всех авторов")
    print("3. Показать книги на руках")
    print("4. Добавить читателя")
    print("5. Выдать книгу")
    print("6. Вернуть книгу")
    print("7. Книги по странам")
    print("8. Книги по векам")
    print("9. Авторы по направлениям")
    print("10. Статистика по жанрам")
    print("11. Самые популярные книги")
    print("0. Выход")
    print("-" * 50)

def run_query(conn, query, title):
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        print(f"\n{title}")
        print("-" * 60)
        if results:
            if cursor.description:
                print(" | ".join(str(d[0]) for d in cursor.description))
                print("-" * 50)
            for row in results[:20]:
                print(" | ".join(str(v) for v in row))
            if len(results) > 20:
                print(f"... и еще {len(results) - 20} строк")
        else:
            print("Нет данных")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        cursor.close()

def show_all_books(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, title_translated, available_copies FROM books ORDER BY title_translated")
    books = cursor.fetchall()
    print("\nСПИСОК КНИГ:")
    for book in books:
        status = "В наличии" if book[2] > 0 else "Нет в наличии"
        print(f"{book[0]}. {book[1]} - {status}")
    print(f"Всего книг: {len(books)}")
    cursor.close()

def show_all_authors(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name, birth_year FROM authors ORDER BY last_name")
    authors = cursor.fetchall()
    print("\nАВТОРЫ:")
    for a in authors:
        name = f"{a[0] or ''} {a[1]}".strip()
        print(f"{name} (р. {a[2]})")
    cursor.close()

def show_active_loans(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.title_translated, r.first_name, r.last_name, l.due_date
        FROM loans l
        JOIN books b ON l.book_id = b.id
        JOIN readers r ON l.reader_id = r.id
        WHERE l.return_date IS NULL
    """)
    loans = cursor.fetchall()
    print("\nКНИГИ НА РУКАХ:")
    if loans:
        for loan in loans:
            print(f"«{loan[0]}» - {loan[1]} {loan[2]} (вернуть до: {loan[3]})")
    else:
        print("Нет выданных книг")
    cursor.close()

def add_reader(conn):
    print("\nДОБАВЛЕНИЕ НОВОГО ЧИТАТЕЛЯ:")
    name = input("Имя и фамилия: ")
    email = input("Email: ")
    phone = input("Телефон: ")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO readers (first_name, last_name, email, phone)
            VALUES (%s, %s, %s, %s)
        """, (name.split()[0], name.split()[-1], email, phone))
        conn.commit()
        print(f"Читатель {name} успешно добавлен!")
    except Exception as e:
        print(f"Ошибка: {e}")
    cursor.close()

def loan_book(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, title_translated FROM books WHERE available_copies > 0 ORDER BY title_translated")
    books = cursor.fetchall()
    if not books:
        print("Нет доступных книг для выдачи!")
        cursor.close()
        return
    print("\nДоступные книги:")
    for b in books:
        print(f"{b[0]}. {b[1]}")
    book_id = input("Введите ID книги: ")

    cursor.execute("SELECT id, first_name, last_name FROM readers ORDER BY last_name")
    readers = cursor.fetchall()
    print("\nЧитатели:")
    for r in readers:
        print(f"{r[0]}. {r[1]} {r[2]}")
    reader_id = input("Введите ID читателя: ")
    days = input("На сколько дней выдать? (по умолчанию 14): ")
    days = int(days) if days else 14

    try:
        cursor.execute("""
            INSERT INTO loans (book_id, reader_id, loan_date, due_date)
            VALUES (%s, %s, CURRENT_DATE, CURRENT_DATE + %s)
        """, (book_id, reader_id, days))
        conn.commit()
        print(f"Книга выдана на {days} дней!")
    except Exception as e:
        print(f"Ошибка: {e}")
    cursor.close()

def return_book(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT l.id, b.title_translated, r.first_name, r.last_name
        FROM loans l
        JOIN books b ON l.book_id = b.id
        JOIN readers r ON l.reader_id = r.id
        WHERE l.return_date IS NULL
    """)
    loans = cursor.fetchall()
    if not loans:
        print("Нет выданных книг!")
        cursor.close()
        return
    print("\nАктивные выдачи:")
    for l in loans:
        print(f"{l[0]}. «{l[1]}» - {l[2]} {l[3]}")
    loan_id = input("Введите ID выдачи для возврата: ")
    try:
        cursor.execute("UPDATE loans SET return_date = CURRENT_DATE WHERE id = %s", (loan_id,))
        conn.commit()
        print("Книга возвращена в библиотеку!")
    except Exception as e:
        print(f"Ошибка: {e}")
    cursor.close()

def show_books_by_country(conn):
    run_query(conn, """
        SELECT c.name, COUNT(b.id) as books
        FROM books b JOIN countries c ON b.country_origin_id = c.id
        GROUP BY c.name ORDER BY books DESC
    """, "КНИГИ ПО СТРАНАМ")

def show_books_by_century(conn):
    run_query(conn, """
        SELECT century, COUNT(*) FROM books
        GROUP BY century ORDER BY MIN(year_written)
    """, "КНИГИ ПО ВЕКАМ")

def show_authors_by_movement(conn):
    run_query(conn, """
        SELECT a.last_name, lm.name, a.birth_year
        FROM authors a JOIN literary_movements lm ON a.movement_id = lm.id
        ORDER BY lm.name, a.last_name
    """, "АВТОРЫ ПО НАПРАВЛЕНИЯМ")

def show_genre_stats(conn):
    run_query(conn, """
        SELECT g.name, COUNT(b.id) as books, SUM(b.total_copies) as copies
        FROM genres g LEFT JOIN books b ON g.id = b.genre_id
        GROUP BY g.name ORDER BY books DESC
    """, "СТАТИСТИКА ПО ЖАНРАМ")

def show_popular_books(conn):
    run_query(conn, """
        SELECT b.title_translated, a.last_name, COUNT(l.id) as loans
        FROM loans l
        JOIN books b ON l.book_id = b.id
        JOIN authors a ON b.author_id = a.id
        GROUP BY b.id, b.title_translated, a.last_name
        ORDER BY loans DESC LIMIT 5
    """, "ТОП-5 ПОПУЛЯРНЫХ КНИГ")

def main():
    print("=" * 50)
    print("     ЗАГРУЗКА БИБЛИОТЕЧНОГО ПРИЛОЖЕНИЯ")
    print("=" * 50)
    conn = connect_to_db()
    if not conn:
        return
    print("Подключение к базе данных установлено!")
    while True:
        show_menu()
        choice = input("Выберите действие (0-11): ")
        if choice == '1':
            show_all_books(conn)
        elif choice == '2':
            show_all_authors(conn)
        elif choice == '3':
            show_active_loans(conn)
        elif choice == '4':
            add_reader(conn)
        elif choice == '5':
            loan_book(conn)
        elif choice == '6':
            return_book(conn)
        elif choice == '7':
            show_books_by_country(conn)
        elif choice == '8':
            show_books_by_century(conn)
        elif choice == '9':
            show_authors_by_movement(conn)
        elif choice == '10':
            show_genre_stats(conn)
        elif choice == '11':
            show_popular_books(conn)
        elif choice == '0':
            print("До свидания!")
            break
        else:
            print("Неверный выбор! Попробуйте снова.")
        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()