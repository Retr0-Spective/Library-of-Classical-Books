import psycopg2
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'classic_library',
    'user': 'postgres',
    'password': 'OAhd112'
}

def connect():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_client_encoding('UTF8')
        return conn
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None

def menu(title, items):
    print(f"\n{title}")
    print("-" * 40)
    for k, v in items.items():
        print(f"{k}. {v}")
    print("0. Назад")
    print("-" * 40)

def show_all(conn, table, fields, join="", order=""):
    cur = conn.cursor()
    query = f"SELECT {fields} FROM {table} {join} ORDER BY {order}"
    cur.execute(query)
    rows = cur.fetchall()
    print(f"\nСПИСОК:")
    for row in rows:
        print(" | ".join(str(r) for r in row))
    print(f"Всего: {len(rows)}")
    cur.close()

def insert_row(conn, table, columns, values):
    cur = conn.cursor()
    try:
        placeholders = ','.join(['%s'] * len(values))
        cur.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values)
        conn.commit()
        print("Запись добавлена!")
    except Exception as e:
        print(f"Ошибка: {e}")
    cur.close()

def update_row(conn, table, set_col, set_val, id_col, id_val):
    cur = conn.cursor()
    try:
        cur.execute(f"UPDATE {table} SET {set_col} = %s WHERE {id_col} = %s", (set_val, id_val))
        conn.commit()
        print("Запись обновлена!")
    except Exception as e:
        print(f"Ошибка: {e}")
    cur.close()

def delete_row(conn, table, id_col, id_val, cascade_table=None):
    cur = conn.cursor()
    try:
        if cascade_table:
            cur.execute(f"DELETE FROM {cascade_table} WHERE {id_col} = %s", (id_val,))
        cur.execute(f"DELETE FROM {table} WHERE {id_col} = %s", (id_val,))
        conn.commit()
        print("Запись удалена!")
    except Exception as e:
        print(f"Ошибка: {e}")
    cur.close()

def run_query(conn, query, title):
    cur = conn.cursor()
    try:
        cur.execute(query)
        rows = cur.fetchall()
        print(f"\n{title}")
        print("-" * 60)
        if rows:
            if cur.description:
                print(" | ".join(d[0] for d in cur.description))
                print("-" * 50)
            for row in rows[:20]:
                print(" | ".join(str(v) for v in row))
            if len(rows) > 20:
                print(f"... еще {len(rows)-20} строк")
        else:
            print("Нет данных")
    except Exception as e:
        print(f"Ошибка: {e}")
    cur.close()

def books_menu(conn):
    while True:
        menu("РАБОТА С КНИГАМИ", {'1': 'Показать все', '2': 'Добавить', '3': 'Редактировать',
                                   '4': 'Удалить', '5': 'Поиск', '6': 'Фильтр', '7': 'Сортировка'})
        ch = input("Выберите действие: ")
        if ch == '1':
            show_all(conn, "books b JOIN authors a ON b.author_id = a.id",
                     "b.id, b.title_translated, a.last_name, b.century, b.available_copies",
                     "", "b.title_translated")
        elif ch == '2':
            cur = conn.cursor()
            cur.execute("SELECT id, last_name FROM authors ORDER BY last_name")
            for a in cur.fetchall():
                print(f"{a[0]}. {a[1]}")
            title = input("Название: ")
            author_id = input("ID автора: ")
            century = input("Век: ")
            year = input("Год: ")
            copies = input("Кол-во: ")
            insert_row(conn, "books", "title_translated, author_id, century, year_written, total_copies, available_copies",
                       (title, author_id, century, year, copies, copies))
            cur.close()
        elif ch == '3':
            show_all(conn, "books", "id, title_translated", "", "title_translated")
            book_id = input("ID книги: ")
            new_title = input("Новое название: ")
            update_row(conn, "books", "title_translated", new_title, "id", book_id)
        elif ch == '4':
            show_all(conn, "books", "id, title_translated", "", "title_translated")
            book_id = input("ID книги: ")
            delete_row(conn, "books", "id", book_id, "loans")
        elif ch == '5':
            s = input("Поиск: ")
            cur = conn.cursor()
            cur.execute("""
                SELECT b.id, b.title_translated, a.last_name 
                FROM books b 
                JOIN authors a ON b.author_id = a.id 
                WHERE b.title_translated ILIKE %s OR a.last_name ILIKE %s
            """, (f"%{s}%", f"%{s}%"))
            for r in cur.fetchall():
                print(f"{r[0]}. {r[1]} - {r[2]}")
            cur.close()
        elif ch == '6':
            print("1. По веку\n2. В наличии\n3. По стране")
            fch = input("Выберите: ")
            if fch == '1':
                cond = f"b.century = '{input('Век: ')}'"
                show_all(conn, "books b JOIN authors a ON b.author_id = a.id",
                         "b.id, b.title_translated, a.last_name, b.century, b.available_copies",
                         f"WHERE {cond}", "b.title_translated")
            elif fch == '2':
                show_all(conn, "books b JOIN authors a ON b.author_id = a.id",
                         "b.id, b.title_translated, a.last_name, b.century, b.available_copies",
                         "WHERE b.available_copies > 0", "b.title_translated")
            elif fch == '3':
                cur = conn.cursor()
                cur.execute("SELECT id, name FROM countries")
                for c in cur.fetchall():
                    print(f"{c[0]}. {c[1]}")
                country_id = input("ID страны: ")
                show_all(conn, "books b JOIN authors a ON b.author_id = a.id",
                         "b.id, b.title_translated, a.last_name, b.century, b.available_copies",
                         f"WHERE b.country_origin_id = {country_id}", "b.title_translated")
                cur.close()
        elif ch == '7':
            print("1. По названию\n2. По автору\n3. По году")
            och = input("Выберите: ")
            order = {'1': 'b.title_translated', '2': 'a.last_name', '3': 'b.year_written'}.get(och, 'b.title_translated')
            show_all(conn, "books b JOIN authors a ON b.author_id = a.id",
                     "b.id, b.title_translated, a.last_name, b.century, b.available_copies",
                     "", order)
        elif ch == '0':
            break
        input("\nНажмите Enter...")

def authors_menu(conn):
    while True:
        menu("РАБОТА С АВТОРАМИ", {'1': 'Показать всех', '2': 'Добавить', '3': 'Редактировать', '4': 'Удалить', '5': 'Поиск'})
        ch = input("Выберите действие: ")
        if ch == '1':
            show_all(conn, "authors", "id, first_name, last_name, birth_year", "", "last_name")
        elif ch == '2':
            first_name = input("Имя (Enter - пропустить): ") or None
            last_name = input("Фамилия: ")
            birth_year = input("Год рождения: ")
            insert_row(conn, "authors", "first_name, last_name, birth_year", (first_name, last_name, birth_year))
        elif ch == '3':
            show_all(conn, "authors", "id, last_name", "", "last_name")
            author_id = input("ID автора: ")
            new_last_name = input("Новая фамилия: ")
            update_row(conn, "authors", "last_name", new_last_name, "id", author_id)
        elif ch == '4':
            show_all(conn, "authors", "id, last_name", "", "last_name")
            author_id = input("ID автора: ")
            delete_row(conn, "authors", "id", author_id, "books")
        elif ch == '5':
            s = input("Фамилия: ")
            cur = conn.cursor()
            cur.execute("SELECT id, first_name, last_name, birth_year FROM authors WHERE last_name ILIKE %s", (f"%{s}%",))
            for r in cur.fetchall():
                print(f"{r[0]}. {r[1] or ''} {r[2]} (р. {r[3]})")
            cur.close()
        elif ch == '0':
            break
        input("\nНажмите Enter...")

def readers_menu(conn):
    while True:
        menu("РАБОТА С ЧИТАТЕЛЯМИ", {'1': 'Показать всех', '2': 'Добавить', '3': 'Редактировать', '4': 'Удалить', '5': 'Поиск'})
        ch = input("Выберите действие: ")
        if ch == '1':
            show_all(conn, "readers", "id, first_name, last_name, email, phone", "", "last_name")
        elif ch == '2':
            first_name = input("Имя: ")
            last_name = input("Фамилия: ")
            email = input("Email: ")
            phone = input("Телефон: ")
            insert_row(conn, "readers", "first_name, last_name, email, phone", (first_name, last_name, email, phone))
        elif ch == '3':
            show_all(conn, "readers", "id, first_name, last_name", "", "last_name")
            reader_id = input("ID читателя: ")
            new_phone = input("Новый телефон: ")
            update_row(conn, "readers", "phone", new_phone, "id", reader_id)
        elif ch == '4':
            show_all(conn, "readers", "id, first_name, last_name", "", "last_name")
            reader_id = input("ID читателя: ")
            delete_row(conn, "readers", "id", reader_id, "loans")
        elif ch == '5':
            s = input("Фамилия: ")
            cur = conn.cursor()
            cur.execute("SELECT id, first_name, last_name, email, phone FROM readers WHERE last_name ILIKE %s OR first_name ILIKE %s", (f"%{s}%", f"%{s}%"))
            for r in cur.fetchall():
                print(f"{r[0]}. {r[1]} {r[2]} | {r[3]} | {r[4] or '-'}")
            cur.close()
        elif ch == '0':
            break
        input("\nНажмите Enter...")

def loans_menu(conn):
    while True:
        menu("ВЫДАЧА КНИГ", {'1': 'Все выдачи', '2': 'Выдать книгу', '3': 'Вернуть книгу', '4': 'Активные', '5': 'Просроченные'})
        ch = input("Выберите действие: ")
        if ch == '1':
            show_all(conn, "loans l JOIN books b ON l.book_id=b.id JOIN readers r ON l.reader_id=r.id",
                     "l.id, b.title_translated, r.first_name, r.last_name, l.loan_date, l.due_date, l.return_date",
                     "", "l.loan_date DESC")
        elif ch == '2':
            cur = conn.cursor()
            cur.execute("SELECT id, title_translated FROM books WHERE available_copies > 0")
            print("\nДоступные книги:")
            for b in cur.fetchall():
                print(f"{b[0]}. {b[1]}")
            book_id = input("ID книги: ")
            cur.execute("SELECT id, first_name, last_name FROM readers")
            print("\nЧитатели:")
            for r in cur.fetchall():
                print(f"{r[0]}. {r[1]} {r[2]}")
            reader_id = input("ID читателя: ")
            days = input("Дней (14): ")
            days = int(days) if days else 14
            cur.execute("""
                INSERT INTO loans (book_id, reader_id, loan_date, due_date)
                VALUES (%s, %s, CURRENT_DATE, CURRENT_DATE + %s)
            """, (book_id, reader_id, days))
            conn.commit()
            print("Книга выдана!")
            cur.close()
        elif ch == '3':
            cur = conn.cursor()
            cur.execute("""
                SELECT l.id, b.title_translated, r.first_name, r.last_name 
                FROM loans l 
                JOIN books b ON l.book_id=b.id 
                JOIN readers r ON l.reader_id=r.id 
                WHERE l.return_date IS NULL
            """)
            print("\nАктивные выдачи:")
            for l in cur.fetchall():
                print(f"{l[0]}. {l[1]} - {l[2]} {l[3]}")
            loan_id = input("ID выдачи для возврата: ")
            cur.execute("UPDATE loans SET return_date = CURRENT_DATE WHERE id = %s", (loan_id,))
            conn.commit()
            print("Книга возвращена!")
            cur.close()
        elif ch == '4':
            cur = conn.cursor()
            cur.execute("""
                SELECT b.title_translated, r.first_name, r.last_name, l.due_date 
                FROM loans l 
                JOIN books b ON l.book_id=b.id 
                JOIN readers r ON l.reader_id=r.id 
                WHERE l.return_date IS NULL
            """)
            print("\nАКТИВНЫЕ ВЫДАЧИ:")
            for l in cur.fetchall():
                print(f"{l[0]} - {l[1]} {l[2]} (до {l[3]})")
            print(f"Всего: {cur.rowcount}")
            cur.close()
        elif ch == '5':
            cur = conn.cursor()
            cur.execute("""
                SELECT b.title_translated, r.first_name, r.last_name, l.due_date, 
                       (CURRENT_DATE - l.due_date) as days_overdue
                FROM loans l 
                JOIN books b ON l.book_id=b.id 
                JOIN readers r ON l.reader_id=r.id 
                WHERE l.return_date IS NULL AND l.due_date < CURRENT_DATE
            """)
            print("\nПРОСРОЧЕННЫЕ ВЫДАЧИ:")
            for l in cur.fetchall():
                print(f"{l[0]} - {l[1]} {l[2]} | просрочено на {l[4]} дней")
            cur.close()
        elif ch == '0':
            break
        input("\nНажмите Enter...")

def author_books_form(conn):
    while True:
        menu("АВТОР И ЕГО КНИГИ", {'1': 'Выбрать автора', '2': 'Показать книги', '3': 'Добавить книгу', '4': 'Новый автор с книгой'})
        ch = input("Выберите действие: ")
        if ch == '1':
            show_all(conn, "authors", "id, first_name, last_name", "", "last_name")
            aid = input("ID автора: ")
            cur = conn.cursor()
            cur.execute("SELECT first_name, last_name FROM authors WHERE id=%s", (aid,))
            a = cur.fetchone()
            if a:
                print(f"Выбран: {a[0] or ''} {a[1]}")
            cur.close()
        elif ch == '2':
            aid = input("ID автора: ")
            cur = conn.cursor()
            cur.execute("SELECT id, title_translated, century, year_written FROM books WHERE author_id=%s", (aid,))
            for b in cur.fetchall():
                print(f"{b[0]}. {b[1]} ({b[2]} век, {b[3]} г.)")
            cur.close()
        elif ch == '3':
            aid = input("ID автора: ")
            title = input("Название книги: ")
            century = input("Век: ")
            year = input("Год: ")
            insert_row(conn, "books", "title_translated, author_id, century, year_written, total_copies, available_copies",
                       (title, aid, century, year, 1, 1))
        elif ch == '4':
            last_name = input("Фамилия автора: ")
            cur = conn.cursor()
            cur.execute("INSERT INTO authors (last_name) VALUES (%s) RETURNING id", (last_name,))
            aid = cur.fetchone()[0]
            conn.commit()
            title = input("Название книги: ")
            century = input("Век: ")
            year = input("Год: ")
            insert_row(conn, "books", "title_translated, author_id, century, year_written, total_copies, available_copies",
                       (title, aid, century, year, 1, 1))
            cur.close()
        elif ch == '0':
            break
        input("\nНажмите Enter...")

def reports_menu(conn):
    reports = [
        ("КНИГИ НА РУКАХ", """
            SELECT r.first_name||' '||r.last_name as читатель, 
                   COUNT(l.id) as книг,
                   SUM(CASE WHEN l.due_date<CURRENT_DATE THEN 1 ELSE 0 END) as просрочено
            FROM readers r 
            LEFT JOIN loans l ON r.id=l.reader_id AND l.return_date IS NULL 
            GROUP BY r.id 
            HAVING COUNT(l.id)>0 
            ORDER BY книг DESC
        """),
        ("СТАТИСТИКА ПО АВТОРАМ", """
            SELECT a.last_name, COUNT(b.id), SUM(b.total_copies), ROUND(AVG(b.word_count)) 
            FROM authors a 
            LEFT JOIN books b ON a.id=b.author_id 
            GROUP BY a.id 
            ORDER BY COUNT(b.id) DESC
        """),
        ("ПОПУЛЯРНОСТЬ ПО ЖАНРАМ", """
            SELECT g.name, COUNT(b.id), COUNT(l.id), 
                   ROUND(COUNT(l.id)::numeric/NULLIF(COUNT(b.id),0),2) 
            FROM genres g 
            LEFT JOIN books b ON g.id=b.genre_id 
            LEFT JOIN loans l ON b.id=l.book_id 
            GROUP BY g.id 
            ORDER BY COUNT(l.id) DESC
        """),
        ("КНИГИ ПО СТРАНАМ", """
            SELECT c.name, COUNT(b.id), SUM(b.total_copies) 
            FROM books b 
            JOIN countries c ON b.country_origin_id=c.id 
            GROUP BY c.name 
            ORDER BY COUNT(b.id) DESC
        """),
        ("АВТОРЫ ПО НАПРАВЛЕНИЯМ", """
            SELECT lm.name, COUNT(a.id), COUNT(b.id) 
            FROM literary_movements lm 
            LEFT JOIN authors a ON lm.id=a.movement_id 
            LEFT JOIN books b ON a.id=b.author_id 
            GROUP BY lm.id 
            ORDER BY COUNT(a.id) DESC
        """),
        ("ДЕТАЛЬНАЯ СТАТИСТИКА ПО ЖАНРАМ", """
            SELECT g.name, COUNT(b.id), SUM(b.total_copies), SUM(b.word_count), ROUND(AVG(b.word_count)) 
            FROM genres g 
            LEFT JOIN books b ON g.id=b.genre_id 
            GROUP BY g.id 
            ORDER BY COUNT(b.id) DESC
        """)
    ]
    while True:
        menu("ОТЧЁТЫ", {str(i+1): r[0] for i, r in enumerate(reports)})
        ch = input("Выберите отчёт (0-6): ")
        if ch == '0':
            break
        try:
            idx = int(ch) - 1
            if 0 <= idx < len(reports):
                run_query(conn, reports[idx][1], reports[idx][0])
        except:
            print("Неверный выбор")
        input("\nНажмите Enter...")

def main():
    conn = connect()
    if not conn:
        return
    print("Подключено к базе данных!")
    while True:
        menu("ГЛАВНОЕ МЕНЮ", {'1': 'Книги', '2': 'Авторы', '3': 'Читатели', '4': 'Выдача книг', '5': 'Форма (Автор+Книги)', '6': 'Отчёты'})
        ch = input("Выберите действие (0-6): ")
        if ch == '1':
            books_menu(conn)
        elif ch == '2':
            authors_menu(conn)
        elif ch == '3':
            readers_menu(conn)
        elif ch == '4':
            loans_menu(conn)
        elif ch == '5':
            author_books_form(conn)
        elif ch == '6':
            reports_menu(conn)
        elif ch == '0':
            print("До свидания!")
            break
        input("\nНажмите Enter...")

if __name__ == "__main__":
    main()