-- ПРОВЕРОЧНЫЕ ЗАПРОСЫ
-- 1. Общая статистика
SELECT 'Страны' as Сущность, COUNT(*) as Количество FROM countries
UNION ALL SELECT 'Направления', COUNT(*) FROM literary_movements
UNION ALL SELECT 'Жанры', COUNT(*) FROM genres
UNION ALL SELECT 'Авторы', COUNT(*) FROM authors
UNION ALL SELECT 'Книги', COUNT(*) FROM books
UNION ALL SELECT 'Издания', COUNT(*) FROM editions
UNION ALL SELECT 'Читатели', COUNT(*) FROM readers
UNION ALL SELECT 'Выдачи', COUNT(*) FROM loans;

-- 2. Все книги с авторами
SELECT b.title_translated as Книга, a.last_name as Автор, b.century as Век
FROM books b
JOIN authors a ON b.author_id = a.id
ORDER BY a.last_name;

-- 3. Книги по странам
SELECT c.name as Страна, COUNT(b.id) as Количество_книг
FROM books b
JOIN countries c ON b.country_origin_id = c.id
GROUP BY c.name
ORDER BY Количество_книг DESC;

-- 4. Книги на руках у читателей
SELECT b.title_translated as Книга, r.first_name || ' ' || r.last_name as Читатель, l.due_date as Срок_возврата
FROM loans l
JOIN books b ON l.book_id = b.id
JOIN readers r ON l.reader_id = r.id
WHERE l.return_date IS NULL;

-- 5. Просроченные книги
SELECT b.title_translated as Книга, r.first_name || ' ' || r.last_name as Читатель, 
       l.due_date as Срок, (CURRENT_DATE - l.due_date) as Дней_просрочки
FROM loans l
JOIN books b ON l.book_id = b.id
JOIN readers r ON l.reader_id = r.id
WHERE l.return_date IS NULL AND l.due_date < CURRENT_DATE;

-- 6. Самые популярные книги
SELECT b.title_translated as Книга, a.last_name as Автор, COUNT(l.id) as Выдач
FROM loans l
JOIN books b ON l.book_id = b.id
JOIN authors a ON b.author_id = a.id
GROUP BY b.id, b.title_translated, a.last_name
ORDER BY Выдач DESC;

-- 7. Доступные книги (представление available_books)
SELECT * FROM available_books;

-- 8. Информация о книгах (представление books_info)
SELECT * FROM books_info LIMIT 10;

-- 9. Статистика по странам (представление country_statistics)
SELECT * FROM country_statistics;

-- 10. Авторы по направлениям
SELECT a.last_name as Автор, lm.name as Направление
FROM authors a
JOIN literary_movements lm ON a.movement_id = lm.id
ORDER BY lm.name, a.last_name;