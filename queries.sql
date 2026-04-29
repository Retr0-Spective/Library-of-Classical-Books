-- АНАЛИТИЧЕСКИЕ ЗАПРОСЫ

-- 1. Общая статистика по библиотеке
SELECT 'Стран' as категория, COUNT(*) as количество FROM countries
UNION ALL SELECT 'Литературных направлений', COUNT(*) FROM literary_movements
UNION ALL SELECT 'Жанров', COUNT(*) FROM genres
UNION ALL SELECT 'Авторов', COUNT(*) FROM authors
UNION ALL SELECT 'Книг', COUNT(*) FROM books
UNION ALL SELECT 'Изданий', COUNT(*) FROM editions
UNION ALL SELECT 'Читателей', COUNT(*) FROM readers
UNION ALL SELECT 'Выдач', COUNT(*) FROM loans;

-- 2. Книги по странам происхождения
SELECT c.name as страна, COUNT(b.id) as количество_книг
FROM books b
JOIN countries c ON b.country_origin_id = c.id
GROUP BY c.name
ORDER BY количество_книг DESC;

-- 3. Книги по векам
SELECT century as век, COUNT(*) as количество
FROM books
GROUP BY century
ORDER BY MIN(year_written);

-- 4. Все книги с авторами
SELECT b.title_translated as книга, a.last_name as автор, b.century as век
FROM books b
JOIN authors a ON b.author_id = a.id
ORDER BY a.last_name;

-- 5. Самые популярные книги (по количеству выдач)
SELECT b.title_translated as книга, a.last_name as автор, COUNT(l.id) as выдач
FROM loans l
JOIN books b ON l.book_id = b.id
JOIN authors a ON b.author_id = a.id
GROUP BY b.id, b.title_translated, a.last_name
ORDER BY выдач DESC;

-- 6. Самые активные читатели
SELECT r.first_name || ' ' || r.last_name as читатель, COUNT(l.id) as выдач
FROM readers r
JOIN loans l ON r.id = l.reader_id
GROUP BY r.id, r.first_name, r.last_name
ORDER BY выдач DESC;

-- 7. Книги, которые сейчас на руках
SELECT b.title_translated as книга, r.first_name || ' ' || r.last_name as читатель, 
       l.due_date as срок_возврата, l.purpose as цель
FROM loans l
JOIN books b ON l.book_id = b.id
JOIN readers r ON l.reader_id = r.id
WHERE l.return_date IS NULL
ORDER BY l.due_date;

-- 8. Просроченные книги
SELECT b.title_translated as книга, r.first_name || ' ' || r.last_name as читатель,
       l.due_date as срок, (CURRENT_DATE - l.due_date) as дней_просрочки
FROM loans l
JOIN books b ON l.book_id = b.id
JOIN readers r ON l.reader_id = r.id
WHERE l.return_date IS NULL AND l.due_date < CURRENT_DATE;

-- 9. Доступные книги (есть в наличии)
SELECT title_translated as книга, available_copies as доступно, total_copies as всего
FROM books
WHERE available_copies > 0
ORDER BY available_copies DESC;

-- 10. Книги, которые закончились (нет в наличии)
SELECT title_translated as книга, total_copies as всего
FROM books
WHERE available_copies = 0;

-- 11. Литературные направления по странам
SELECT c.name as страна, lm.name as направление, COUNT(b.id) as произведений
FROM books b
JOIN countries c ON b.country_origin_id = c.id
JOIN literary_movements lm ON b.movement_id = lm.id
GROUP BY c.name, lm.name
ORDER BY c.name, произведений DESC;

-- 12. Авторы по направлениям
SELECT a.last_name as автор, lm.name as направление, a.birth_year as год_рождения
FROM authors a
JOIN literary_movements lm ON a.movement_id = lm.id
ORDER BY lm.name, a.last_name;

-- 13. Статистика по жанрам
SELECT g.name as жанр, COUNT(b.id) as книг, SUM(b.total_copies) as экземпляров
FROM genres g
LEFT JOIN books b ON g.id = b.genre_id
GROUP BY g.name
ORDER BY книг DESC;

-- 14. Читательские предпочтения (любимые жанры и страны)
SELECT r.first_name || ' ' || r.last_name as читатель,
       g.name as любимый_жанр, c.name as любимая_страна
FROM readers r
LEFT JOIN genres g ON r.favorite_genre_id = g.id
LEFT JOIN countries c ON r.favorite_country_id = c.id
ORDER BY r.last_name;

-- 15. Динамика выдач по месяцам
SELECT TO_CHAR(loan_date, 'YYYY-MM') as месяц,
       COUNT(*) as выдач, COUNT(DISTINCT reader_id) as читателей
FROM loans
GROUP BY TO_CHAR(loan_date, 'YYYY-MM')
ORDER BY месяц;

-- 16. Самые короткие книги (по количеству слов)
SELECT title_translated as книга, a.last_name as автор, word_count as количество_слов
FROM books b
JOIN authors a ON b.author_id = a.id
WHERE word_count IS NOT NULL
ORDER BY word_count
LIMIT 5;

-- 17. Самые длинные книги
SELECT title_translated as книга, a.last_name as автор, word_count as количество_слов
FROM books b
JOIN authors a ON b.author_id = a.id
WHERE word_count IS NOT NULL
ORDER BY word_count DESC
LIMIT 5;

-- 18. Полный каталог книг с авторами и странами
SELECT 
    b.title_translated as книга,
    a.last_name as автор,
    c.name as страна_автора,
    b.century as век,
    b.year_written as год_написания,
    b.total_copies as экземпляров
FROM books b
JOIN authors a ON b.author_id = a.id
JOIN countries c ON a.country_id = c.id
ORDER BY a.last_name, b.year_written;

-- 19. Самый продуктивный век
SELECT century as век, COUNT(*) as книг
FROM books
GROUP BY century
ORDER BY книг DESC
LIMIT 1;

-- 20. Книги, которые брали больше 1 раза
SELECT b.title_translated as книга, COUNT(l.id) as выдач
FROM books b
JOIN loans l ON b.id = l.book_id
GROUP BY b.id, b.title_translated
HAVING COUNT(l.id) > 1
ORDER BY выдач DESC;