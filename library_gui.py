import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'classic_library',
    'user': 'postgres',
    'password': 'OAhd112'
}


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Мировая классическая библиотека")
        self.root.geometry("900x600")
        self.root.resizable(True, True)

        # Подключение к БД
        self.conn = None
        self.connect_to_db()

        # Создание интерфейса
        self.create_menu()
        self.create_main_frame()

    def connect_to_db(self):
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.conn.set_client_encoding('UTF8')
            print("Подключено к базе данных")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось подключиться к БД:\n{e}")
            self.root.destroy()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Меню "Книги"
        books_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Книги", menu=books_menu)
        books_menu.add_command(label="Показать все книги", command=self.show_books)
        books_menu.add_command(label="Добавить книгу", command=self.add_book)
        books_menu.add_command(label="Редактировать книгу", command=self.edit_book)
        books_menu.add_command(label="Удалить книгу", command=self.delete_book)
        books_menu.add_separator()
        books_menu.add_command(label="Поиск книг", command=self.search_books)

        # Меню "Авторы"
        authors_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Авторы", menu=authors_menu)
        authors_menu.add_command(label="Показать всех авторов", command=self.show_authors)
        authors_menu.add_command(label="Добавить автора", command=self.add_author)
        authors_menu.add_command(label="Редактировать автора", command=self.edit_author)
        authors_menu.add_command(label="Удалить автора", command=self.delete_author)

        # Меню "Читатели"
        readers_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Читатели", menu=readers_menu)
        readers_menu.add_command(label="Показать всех читателей", command=self.show_readers)
        readers_menu.add_command(label="Добавить читателя", command=self.add_reader)
        readers_menu.add_command(label="Редактировать читателя", command=self.edit_reader)
        readers_menu.add_command(label="Удалить читателя", command=self.delete_reader)

        # Меню "Выдача"
        loans_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Выдача книг", menu=loans_menu)
        loans_menu.add_command(label="Все выдачи", command=self.show_loans)
        loans_menu.add_command(label="Выдать книгу", command=self.loan_book)
        loans_menu.add_command(label="Вернуть книгу", command=self.return_book)
        loans_menu.add_command(label="Активные выдачи", command=self.show_active_loans)

        # Меню "Отчёты"
        reports_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Отчёты", menu=reports_menu)
        reports_menu.add_command(label="Книги на руках", command=self.report_books_on_hands)
        reports_menu.add_command(label="Статистика по авторам", command=self.report_author_stats)
        reports_menu.add_command(label="Книги по странам", command=self.report_books_by_country)
        reports_menu.add_command(label="Популярность по жанрам", command=self.report_genre_popularity)

        # Меню "Помощь"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Помощь", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        title_label = ttk.Label(self.main_frame, text="МИРОВАЯ КЛАССИЧЕСКАЯ БИБЛИОТЕКА",
                                font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Таблица для отображения данных
        self.tree = ttk.Treeview(self.main_frame, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Скроллбар для таблицы
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Кнопки управления
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="Обновить", command=self.refresh_view).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Выдать книгу", command=self.loan_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Вернуть книгу", command=self.return_book).pack(side=tk.LEFT, padx=5)

        # Статусная строка
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Загружаем начальные данные
        self.show_books()

    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def refresh_view(self):
        self.show_books()

    def show_books(self):
        self.clear_table()
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT b.id, b.title_translated, a.last_name, b.century, b.available_copies
            FROM books b JOIN authors a ON b.author_id = a.id
            ORDER BY b.title_translated
        """)
        rows = cursor.fetchall()
        cursor.close()

        columns = ["ID", "Название", "Автор", "Век", "В наличии"]
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        self.status_var.set(f"Загружено книг: {len(rows)}")

    def show_authors(self):
        self.clear_table()
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, first_name, last_name, birth_year FROM authors ORDER BY last_name")
        rows = cursor.fetchall()
        cursor.close()

        columns = ["ID", "Имя", "Фамилия", "Год рождения"]
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        self.status_var.set(f"Загружено авторов: {len(rows)}")

    def show_readers(self):
        self.clear_table()
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, first_name, last_name, email, phone FROM readers ORDER BY last_name")
        rows = cursor.fetchall()
        cursor.close()

        columns = ["ID", "Имя", "Фамилия", "Email", "Телефон"]
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        self.status_var.set(f"Загружено читателей: {len(rows)}")

    def show_loans(self):
        self.clear_table()
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT l.id, b.title_translated, r.first_name, r.last_name, l.loan_date, l.due_date, l.return_date
            FROM loans l
            JOIN books b ON l.book_id = b.id
            JOIN readers r ON l.reader_id = r.id
            ORDER BY l.loan_date DESC
        """)
        rows = cursor.fetchall()
        cursor.close()

        columns = ["ID", "Книга", "Читатель", "Фамилия", "Дата выдачи", "Срок", "Дата возврата"]
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        self.status_var.set(f"Загружено выдач: {len(rows)}")

    def show_active_loans(self):
        self.clear_table()
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT b.title_translated, r.first_name, r.last_name, l.due_date
            FROM loans l
            JOIN books b ON l.book_id = b.id
            JOIN readers r ON l.reader_id = r.id
            WHERE l.return_date IS NULL
        """)
        rows = cursor.fetchall()
        cursor.close()

        columns = ["Книга", "Имя читателя", "Фамилия", "Срок возврата"]
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        self.status_var.set(f"Активных выдач: {len(rows)}")

    def add_book(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить книгу")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Название:").pack(pady=5)
        title_entry = ttk.Entry(dialog, width=40)
        title_entry.pack(pady=5)

        # Выбор автора
        ttk.Label(dialog, text="Автор:").pack(pady=5)
        author_combo = ttk.Combobox(dialog, width=37)
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, last_name FROM authors ORDER BY last_name")
        authors = cursor.fetchall()
        author_combo['values'] = [f"{a[0]}. {a[1]}" for a in authors]
        author_combo.pack(pady=5)
        cursor.close()

        ttk.Label(dialog, text="Век:").pack(pady=5)
        century_entry = ttk.Entry(dialog, width=40)
        century_entry.pack(pady=5)

        ttk.Label(dialog, text="Год написания:").pack(pady=5)
        year_entry = ttk.Entry(dialog, width=40)
        year_entry.pack(pady=5)

        ttk.Label(dialog, text="Количество экземпляров:").pack(pady=5)
        copies_entry = ttk.Entry(dialog, width=40)
        copies_entry.pack(pady=5)

        def save():
            if not author_combo.get():
                messagebox.showerror("Ошибка", "Выберите автора")
                return
            author_id = author_combo.get().split(".")[0]
            cursor = self.conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO books (title_translated, author_id, century, year_written, total_copies, available_copies)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (title_entry.get(), author_id, century_entry.get(), year_entry.get(),
                      copies_entry.get(), copies_entry.get()))
                self.conn.commit()
                messagebox.showinfo("Успех", "Книга добавлена!")
                dialog.destroy()
                self.show_books()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
            cursor.close()

        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=20)

    def add_author(self):
        name = simpledialog.askstring("Добавить автора", "Введите имя и фамилию автора:")
        if name:
            cursor = self.conn.cursor()
            try:
                parts = name.split()
                if len(parts) >= 2:
                    cursor.execute("INSERT INTO authors (first_name, last_name) VALUES (%s, %s)",
                                   (parts[0], ' '.join(parts[1:])))
                else:
                    cursor.execute("INSERT INTO authors (last_name) VALUES (%s)", (name,))
                self.conn.commit()
                messagebox.showinfo("Успех", "Автор добавлен!")
                self.show_authors()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
            cursor.close()

    def add_reader(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить читателя")
        dialog.geometry("300x250")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Имя:").pack(pady=5)
        first_entry = ttk.Entry(dialog, width=30)
        first_entry.pack(pady=5)

        ttk.Label(dialog, text="Фамилия:").pack(pady=5)
        last_entry = ttk.Entry(dialog, width=30)
        last_entry.pack(pady=5)

        ttk.Label(dialog, text="Email:").pack(pady=5)
        email_entry = ttk.Entry(dialog, width=30)
        email_entry.pack(pady=5)

        ttk.Label(dialog, text="Телефон:").pack(pady=5)
        phone_entry = ttk.Entry(dialog, width=30)
        phone_entry.pack(pady=5)

        def save():
            cursor = self.conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO readers (first_name, last_name, email, phone)
                    VALUES (%s, %s, %s, %s)
                """, (first_entry.get(), last_entry.get(), email_entry.get(), phone_entry.get()))
                self.conn.commit()
                messagebox.showinfo("Успех", "Читатель добавлен!")
                dialog.destroy()
                self.show_readers()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
            cursor.close()

        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=20)

    def loan_book(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Выдать книгу")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Книга:").pack(pady=5)
        book_combo = ttk.Combobox(dialog, width=37)
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, title_translated FROM books WHERE available_copies > 0 ORDER BY title_translated")
        books = cursor.fetchall()
        book_combo['values'] = [f"{b[0]}. {b[1]}" for b in books]
        book_combo.pack(pady=5)

        ttk.Label(dialog, text="Читатель:").pack(pady=5)
        reader_combo = ttk.Combobox(dialog, width=37)
        cursor.execute("SELECT id, first_name, last_name FROM readers ORDER BY last_name")
        readers = cursor.fetchall()
        reader_combo['values'] = [f"{r[0]}. {r[1]} {r[2]}" for r in readers]
        reader_combo.pack(pady=5)
        cursor.close()

        ttk.Label(dialog, text="На сколько дней:").pack(pady=5)
        days_entry = ttk.Entry(dialog, width=30)
        days_entry.insert(0, "14")
        days_entry.pack(pady=5)

        def save():
            if not book_combo.get() or not reader_combo.get():
                messagebox.showerror("Ошибка", "Выберите книгу и читателя")
                return
            book_id = book_combo.get().split(".")[0]
            reader_id = reader_combo.get().split(".")[0]
            days = days_entry.get() or "14"

            cursor = self.conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO loans (book_id, reader_id, loan_date, due_date)
                    VALUES (%s, %s, CURRENT_DATE, CURRENT_DATE + %s)
                """, (book_id, reader_id, days))
                self.conn.commit()
                messagebox.showinfo("Успех", "Книга выдана!")
                dialog.destroy()
                self.show_books()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
            cursor.close()

        ttk.Button(dialog, text="Выдать", command=save).pack(pady=20)

    def return_book(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Вернуть книгу")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Выберите выдачу для возврата:").pack(pady=10)

        listbox = tk.Listbox(dialog, width=50, height=10)
        listbox.pack(pady=10)

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT l.id, b.title_translated, r.first_name, r.last_name, l.due_date
            FROM loans l
            JOIN books b ON l.book_id = b.id
            JOIN readers r ON l.reader_id = r.id
            WHERE l.return_date IS NULL
        """)
        loans = cursor.fetchall()
        for loan in loans:
            listbox.insert(tk.END, f"{loan[0]}. {loan[1]} - {loan[2]} {loan[3]} (до {loan[4]})")
        cursor.close()

        def save():
            selection = listbox.curselection()
            if not selection:
                messagebox.showerror("Ошибка", "Выберите выдачу")
                return
            loan_text = listbox.get(selection[0])
            loan_id = loan_text.split(".")[0]

            cursor = self.conn.cursor()
            try:
                cursor.execute("UPDATE loans SET return_date = CURRENT_DATE WHERE id = %s", (loan_id,))
                self.conn.commit()
                messagebox.showinfo("Успех", "Книга возвращена!")
                dialog.destroy()
                self.show_books()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
            cursor.close()

        ttk.Button(dialog, text="Вернуть", command=save).pack(pady=20)

    def edit_book(self):
        book_id = simpledialog.askstring("Редактировать книгу", "Введите ID книги для редактирования:")
        if book_id:
            new_title = simpledialog.askstring("Редактировать книгу", "Введите новое название:")
            if new_title:
                cursor = self.conn.cursor()
                try:
                    cursor.execute("UPDATE books SET title_translated = %s WHERE id = %s", (new_title, book_id))
                    self.conn.commit()
                    messagebox.showinfo("Успех", "Книга обновлена!")
                    self.show_books()
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))
                cursor.close()

    def edit_author(self):
        author_id = simpledialog.askstring("Редактировать автора", "Введите ID автора:")
        if author_id:
            new_name = simpledialog.askstring("Редактировать автора", "Введите новое имя автора:")
            if new_name:
                cursor = self.conn.cursor()
                try:
                    parts = new_name.split()
                    if len(parts) >= 2:
                        cursor.execute("UPDATE authors SET first_name = %s, last_name = %s WHERE id = %s",
                                       (parts[0], ' '.join(parts[1:]), author_id))
                    else:
                        cursor.execute("UPDATE authors SET last_name = %s WHERE id = %s", (new_name, author_id))
                    self.conn.commit()
                    messagebox.showinfo("Успех", "Автор обновлён!")
                    self.show_authors()
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))
                cursor.close()

    def edit_reader(self):
        reader_id = simpledialog.askstring("Редактировать читателя", "Введите ID читателя:")
        if reader_id:
            new_phone = simpledialog.askstring("Редактировать читателя", "Введите новый телефон:")
            if new_phone:
                cursor = self.conn.cursor()
                try:
                    cursor.execute("UPDATE readers SET phone = %s WHERE id = %s", (new_phone, reader_id))
                    self.conn.commit()
                    messagebox.showinfo("Успех", "Читатель обновлён!")
                    self.show_readers()
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))
                cursor.close()

    def delete_book(self):
        book_id = simpledialog.askstring("Удалить книгу", "Введите ID книги для удаления:")
        if book_id:
            if messagebox.askyesno("Подтверждение", f"Удалить книгу с ID {book_id}?"):
                cursor = self.conn.cursor()
                try:
                    cursor.execute("DELETE FROM loans WHERE book_id = %s", (book_id,))
                    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
                    self.conn.commit()
                    messagebox.showinfo("Успех", "Книга удалена!")
                    self.show_books()
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))
                cursor.close()

    def delete_author(self):
        author_id = simpledialog.askstring("Удалить автора", "Введите ID автора:")
        if author_id:
            if messagebox.askyesno("Подтверждение", f"Удалить автора с ID {author_id}?"):
                cursor = self.conn.cursor()
                try:
                    cursor.execute("UPDATE books SET author_id = NULL WHERE author_id = %s", (author_id,))
                    cursor.execute("DELETE FROM authors WHERE id = %s", (author_id,))
                    self.conn.commit()
                    messagebox.showinfo("Успех", "Автор удалён!")
                    self.show_authors()
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))
                cursor.close()

    def delete_reader(self):
        reader_id = simpledialog.askstring("Удалить читателя", "Введите ID читателя:")
        if reader_id:
            if messagebox.askyesno("Подтверждение", f"Удалить читателя с ID {reader_id}?"):
                cursor = self.conn.cursor()
                try:
                    cursor.execute("UPDATE loans SET reader_id = NULL WHERE reader_id = %s", (reader_id,))
                    cursor.execute("DELETE FROM readers WHERE id = %s", (reader_id,))
                    self.conn.commit()
                    messagebox.showinfo("Успех", "Читатель удалён!")
                    self.show_readers()
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))
                cursor.close()

    def search_books(self):
        search = simpledialog.askstring("Поиск книг", "Введите название или автора:")
        if search:
            self.clear_table()
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT b.id, b.title_translated, a.last_name, b.century, b.available_copies
                FROM books b JOIN authors a ON b.author_id = a.id
                WHERE b.title_translated ILIKE %s OR a.last_name ILIKE %s
                ORDER BY b.title_translated
            """, (f"%{search}%", f"%{search}%"))
            rows = cursor.fetchall()
            cursor.close()

            columns = ["ID", "Название", "Автор", "Век", "В наличии"]
            self.tree["columns"] = columns
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=150)

            for row in rows:
                self.tree.insert("", tk.END, values=row)

            self.status_var.set(f"Найдено книг: {len(rows)}")

    def report_books_on_hands(self):
        self.clear_table()
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT r.first_name || ' ' || r.last_name as reader, COUNT(l.id) as books, 
                   SUM(CASE WHEN l.due_date < CURRENT_DATE THEN 1 ELSE 0 END) as overdue
            FROM readers r
            LEFT JOIN loans l ON r.id = l.reader_id AND l.return_date IS NULL
            GROUP BY r.id
            HAVING COUNT(l.id) > 0
            ORDER BY books DESC
        """)
        rows = cursor.fetchall()
        cursor.close()

        columns = ["Читатель", "Книг на руках", "Просрочено"]
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        self.status_var.set(f"Отчёт: книги на руках у читателей")

    def report_author_stats(self):
        self.clear_table()
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT a.last_name, COUNT(b.id) as books, SUM(b.total_copies) as copies, 
                   ROUND(AVG(b.word_count)) as avg_words
            FROM authors a LEFT JOIN books b ON a.id = b.author_id
            GROUP BY a.id ORDER BY books DESC
        """)
        rows = cursor.fetchall()
        cursor.close()

        columns = ["Автор", "Книг", "Экземпляров", "Ср. слов"]
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        self.status_var.set(f"Отчёт: статистика по авторам")

    def report_books_by_country(self):
        self.clear_table()
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT c.name, COUNT(b.id) as books, SUM(b.total_copies) as copies
            FROM books b JOIN countries c ON b.country_origin_id = c.id
            GROUP BY c.name ORDER BY books DESC
        """)
        rows = cursor.fetchall()
        cursor.close()

        columns = ["Страна", "Книг", "Экземпляров"]
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        self.status_var.set(f"Отчёт: книги по странам")

    def report_genre_popularity(self):
        self.clear_table()
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT g.name, COUNT(b.id) as books, COUNT(l.id) as loans,
                   ROUND(COUNT(l.id)::numeric / NULLIF(COUNT(b.id), 0), 2) as ratio
            FROM genres g
            LEFT JOIN books b ON g.id = b.genre_id
            LEFT JOIN loans l ON b.id = l.book_id
            GROUP BY g.id ORDER BY loans DESC
        """)
        rows = cursor.fetchall()
        cursor.close()

        columns = ["Жанр", "Книг", "Выдач", "Популярность"]
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        self.status_var.set(f"Отчёт: популярность по жанрам")

    def show_about(self):
        messagebox.showinfo("О программе",
                            "Мировая классическая библиотека\n\n"
                            "Версия: 2.0 (Графический интерфейс)\n"
                            "Разработчик: Чухланцев Данил Алексеевич\n\n"
                            "Технологии:\n"
                            "- PostgreSQL\n"
                            "- Python + Tkinter\n"
                            "- psycopg2")


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()