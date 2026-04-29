-- ЗАПОЛНЕНИЕ БАЗЫ ДАННЫХ

-- 1. СТРАНЫ
INSERT INTO countries (name, continent, language_official, code) VALUES
    ('Россия', 'Европа', 'Русский', 'RUS'),
    ('Англия', 'Европа', 'Английский', 'GBR'),
    ('Франция', 'Европа', 'Французский', 'FRA'),
    ('Германия', 'Европа', 'Немецкий', 'DEU'),
    ('США', 'Северная Америка', 'Английский', 'USA'),
    ('Япония', 'Азия', 'Японский', 'JPN'),
    ('Италия', 'Европа', 'Итальянский', 'ITA'),
    ('Греция', 'Европа', 'Греческий', 'GRC'),
    ('Колумбия', 'Южная Америка', 'Испанский', 'COL');

-- 2. ЛИТЕРАТУРНЫЕ НАПРАВЛЕНИЯ
INSERT INTO literary_movements (name, century_origin, description) VALUES
    ('Античность', 'V до н.э.', 'Греко-римская литература, мифология, эпос'),
    ('Средневековье', 'V-XV', 'Рыцарские романы, религиозная литература'),
    ('Ренессанс', 'XIV-XVI', 'Возрождение античных идеалов, гуманизм'),
    ('Романтизм', 'XIX', 'Чувства, природа, индивидуализм'),
    ('Реализм', 'XIX', 'Правдивое отображение действительности'),
    ('Модернизм', 'XX', 'Эксперименты, поток сознания'),
    ('Постмодернизм', 'XX-XXI', 'Ирония, метапроза, магический реализм');

-- 3. ЖАНРЫ
INSERT INTO genres (name, category) VALUES
    ('Роман', 'проза'),
    ('Трагедия', 'драма'),
    ('Поэма', 'поэзия'),
    ('Новелла', 'проза'),
    ('Эпопея', 'проза'),
    ('Антиутопия', 'проза');

-- 4. АВТОРЫ
INSERT INTO authors (first_name, last_name, birth_year, death_year, country_id, movement_id, notable_works) VALUES
    ('Федор', 'Достоевский', 1821, 1881, (SELECT id FROM countries WHERE name = 'Россия'), (SELECT id FROM literary_movements WHERE name = 'Реализм'), 'Преступление и наказание, Братья Карамазовы, Идиот'),
    ('Лев', 'Толстой', 1828, 1910, (SELECT id FROM countries WHERE name = 'Россия'), (SELECT id FROM literary_movements WHERE name = 'Реализм'), 'Война и мир, Анна Каренина, Воскресение'),
    ('Александр', 'Пушкин', 1799, 1837, (SELECT id FROM countries WHERE name = 'Россия'), (SELECT id FROM literary_movements WHERE name = 'Романтизм'), 'Евгений Онегин, Руслан и Людмила, Капитанская дочка'),
    ('Чарльз', 'Диккенс', 1812, 1870, (SELECT id FROM countries WHERE name = 'Англия'), (SELECT id FROM literary_movements WHERE name = 'Реализм'), 'Большие надежды, Оливер Твист, Дэвид Копперфильд'),
    ('Джейн', 'Остин', 1775, 1817, (SELECT id FROM countries WHERE name = 'Англия'), (SELECT id FROM literary_movements WHERE name = 'Романтизм'), 'Гордость и предубеждение, Эмма, Чувство и чувствительность'),
    ('Джордж', 'Оруэлл', 1903, 1950, (SELECT id FROM countries WHERE name = 'Англия'), (SELECT id FROM literary_movements WHERE name = 'Постмодернизм'), '1984, Скотный двор, Дочь священника'),
    ('Уильям', 'Шекспир', 1564, 1616, (SELECT id FROM countries WHERE name = 'Англия'), (SELECT id FROM literary_movements WHERE name = 'Ренессанс'), 'Гамлет, Ромео и Джульетта, Макбет'),
    ('Виктор', 'Гюго', 1802, 1885, (SELECT id FROM countries WHERE name = 'Франция'), (SELECT id FROM literary_movements WHERE name = 'Романтизм'), 'Отверженные, Собор Парижской Богоматери, Человек, который смеется'),
    ('Гюстав', 'Флобер', 1821, 1880, (SELECT id FROM countries WHERE name = 'Франция'), (SELECT id FROM literary_movements WHERE name = 'Реализм'), 'Госпожа Бовари, Саламбо, Воспитание чувств'),
    ('Франц', 'Кафка', 1883, 1924, (SELECT id FROM countries WHERE name = 'Германия'), (SELECT id FROM literary_movements WHERE name = 'Модернизм'), 'Превращение, Процесс, Замок'),
    ('Иоганн', 'Гете', 1749, 1832, (SELECT id FROM countries WHERE name = 'Германия'), (SELECT id FROM literary_movements WHERE name = 'Романтизм'), 'Фауст, Страдания юного Вертера'),
    ('Эрнест', 'Хемингуэй', 1899, 1961, (SELECT id FROM countries WHERE name = 'США'), (SELECT id FROM literary_movements WHERE name = 'Модернизм'), 'Старик и море, По ком звонит колокол, Прощай, оружие'),
    ('Мурасаки', 'Сикибу', 978, 1014, (SELECT id FROM countries WHERE name = 'Япония'), (SELECT id FROM literary_movements WHERE name = 'Средневековье'), 'Повесть о Гэндзи'),
    ('Данте', 'Алигьери', 1265, 1321, (SELECT id FROM countries WHERE name = 'Италия'), (SELECT id FROM literary_movements WHERE name = 'Ренессанс'), 'Божественная комедия'),
    (NULL, 'Гомер', -800, -750, (SELECT id FROM countries WHERE name = 'Греция'), (SELECT id FROM literary_movements WHERE name = 'Античность'), 'Илиада, Одиссея'),
    ('Габриэль', 'Гарсиа Маркес', 1927, 2014, (SELECT id FROM countries WHERE name = 'Колумбия'), (SELECT id FROM literary_movements WHERE name = 'Постмодернизм'), 'Сто лет одиночества, Любовь во время холеры');

-- 5. КНИГИ
INSERT INTO books (title_original, title_translated, author_id, genre_id, movement_id, century, year_written, year_published_first, language_original, country_origin_id, is_epic, word_count, total_copies, available_copies) VALUES
    ('Crime and Punishment', 'Преступление и наказание', (SELECT id FROM authors WHERE last_name = 'Достоевский'), (SELECT id FROM genres WHERE name = 'Роман'), (SELECT id FROM literary_movements WHERE name = 'Реализм'), 'XIX', 1866, 1866, 'Русский', (SELECT id FROM countries WHERE name = 'Россия'), FALSE, 210000, 3, 3),
    ('War and Peace', 'Война и мир', (SELECT id FROM authors WHERE last_name = 'Толстой'), (SELECT id FROM genres WHERE name = 'Эпопея'), (SELECT id FROM literary_movements WHERE name = 'Реализм'), 'XIX', 1869, 1869, 'Русский', (SELECT id FROM countries WHERE name = 'Россия'), TRUE, 580000, 2, 2),
    ('Eugene Onegin', 'Евгений Онегин', (SELECT id FROM authors WHERE last_name = 'Пушкин'), (SELECT id FROM genres WHERE name = 'Роман'), (SELECT id FROM literary_movements WHERE name = 'Романтизм'), 'XIX', 1833, 1833, 'Русский', (SELECT id FROM countries WHERE name = 'Россия'), FALSE, 35000, 2, 2),
    ('Great Expectations', 'Большие надежды', (SELECT id FROM authors WHERE last_name = 'Диккенс'), (SELECT id FROM genres WHERE name = 'Роман'), (SELECT id FROM literary_movements WHERE name = 'Реализм'), 'XIX', 1861, 1861, 'Английский', (SELECT id FROM countries WHERE name = 'Англия'), FALSE, 183000, 3, 3),
    ('Pride and Prejudice', 'Гордость и предубеждение', (SELECT id FROM authors WHERE last_name = 'Остин'), (SELECT id FROM genres WHERE name = 'Роман'), (SELECT id FROM literary_movements WHERE name = 'Романтизм'), 'XIX', 1813, 1813, 'Английский', (SELECT id FROM countries WHERE name = 'Англия'), FALSE, 120000, 4, 4),
    ('Nineteen Eighty-Four', '1984', (SELECT id FROM authors WHERE last_name = 'Оруэлл'), (SELECT id FROM genres WHERE name = 'Антиутопия'), (SELECT id FROM literary_movements WHERE name = 'Постмодернизм'), 'XX', 1949, 1949, 'Английский', (SELECT id FROM countries WHERE name = 'Англия'), FALSE, 89000, 3, 3),
    ('Hamlet', 'Гамлет', (SELECT id FROM authors WHERE last_name = 'Шекспир'), (SELECT id FROM genres WHERE name = 'Трагедия'), (SELECT id FROM literary_movements WHERE name = 'Ренессанс'), 'XVII', 1601, 1603, 'Английский', (SELECT id FROM countries WHERE name = 'Англия'), FALSE, 30000, 2, 2),
    ('Les Misérables', 'Отверженные', (SELECT id FROM authors WHERE last_name = 'Гюго'), (SELECT id FROM genres WHERE name = 'Роман'), (SELECT id FROM literary_movements WHERE name = 'Романтизм'), 'XIX', 1862, 1862, 'Французский', (SELECT id FROM countries WHERE name = 'Франция'), TRUE, 530000, 2, 2),
    ('Madame Bovary', 'Госпожа Бовари', (SELECT id FROM authors WHERE last_name = 'Флобер'), (SELECT id FROM genres WHERE name = 'Роман'), (SELECT id FROM literary_movements WHERE name = 'Реализм'), 'XIX', 1856, 1857, 'Французский', (SELECT id FROM countries WHERE name = 'Франция'), FALSE, 140000, 2, 2),
    ('The Metamorphosis', 'Превращение', (SELECT id FROM authors WHERE last_name = 'Кафка'), (SELECT id FROM genres WHERE name = 'Новелла'), (SELECT id FROM literary_movements WHERE name = 'Модернизм'), 'XX', 1915, 1915, 'Немецкий', (SELECT id FROM countries WHERE name = 'Германия'), FALSE, 21000, 2, 2),
    ('Faust', 'Фауст', (SELECT id FROM authors WHERE last_name = 'Гете'), (SELECT id FROM genres WHERE name = 'Трагедия'), (SELECT id FROM literary_movements WHERE name = 'Романтизм'), 'XIX', 1832, 1808, 'Немецкий', (SELECT id FROM countries WHERE name = 'Германия'), FALSE, 100000, 1, 1),
    ('The Old Man and the Sea', 'Старик и море', (SELECT id FROM authors WHERE last_name = 'Хемингуэй'), (SELECT id FROM genres WHERE name = 'Роман'), (SELECT id FROM literary_movements WHERE name = 'Модернизм'), 'XX', 1952, 1952, 'Английский', (SELECT id FROM countries WHERE name = 'США'), FALSE, 27000, 3, 3),
    ('The Tale of Genji', 'Повесть о Гэндзи', (SELECT id FROM authors WHERE last_name = 'Сикибу'), (SELECT id FROM genres WHERE name = 'Роман'), (SELECT id FROM literary_movements WHERE name = 'Средневековье'), 'XI', 1010, 1021, 'Японский', (SELECT id FROM countries WHERE name = 'Япония'), TRUE, 400000, 1, 1),
    ('The Divine Comedy', 'Божественная комедия', (SELECT id FROM authors WHERE last_name = 'Алигьери'), (SELECT id FROM genres WHERE name = 'Поэма'), (SELECT id FROM literary_movements WHERE name = 'Ренессанс'), 'XIV', 1320, 1472, 'Итальянский', (SELECT id FROM countries WHERE name = 'Италия'), FALSE, 100000, 2, 2),
    ('Iliad', 'Илиада', (SELECT id FROM authors WHERE last_name = 'Гомер'), (SELECT id FROM genres WHERE name = 'Эпопея'), (SELECT id FROM literary_movements WHERE name = 'Античность'), 'VIII до н.э.', -750, -750, 'Греческий', (SELECT id FROM countries WHERE name = 'Греция'), TRUE, 150000, 2, 2),
    ('One Hundred Years of Solitude', 'Сто лет одиночества', (SELECT id FROM authors WHERE last_name = 'Гарсиа Маркес'), (SELECT id FROM genres WHERE name = 'Роман'), (SELECT id FROM literary_movements WHERE name = 'Постмодернизм'), 'XX', 1967, 1967, 'Испанский', (SELECT id FROM countries WHERE name = 'Колумбия'), FALSE, 150000, 3, 3);

-- 6. ИЗДАНИЯ (ИСПРАВЛЕНО: УДАЛЁН ДУБЛИКАТ ISBN)
INSERT INTO editions (book_id, publisher, translator, publication_year, isbn, page_count, cover_type, price) VALUES
    ((SELECT id FROM books WHERE title_translated = 'Преступление и наказание'), 'Азбука', 'Раиса Гальперина', 2020, '978-5-389-12345-6', 672, 'твёрдая', 450.00),
    ((SELECT id FROM books WHERE title_translated = 'Преступление и наказание'), 'Эксмо', 'Нина Вольпин', 2018, '978-5-04-098765-4', 640, 'мягкая', 350.00),
    ((SELECT id FROM books WHERE title_translated = 'Война и мир'), 'Эксмо', 'Александра Чечина', 2022, '978-5-04-150123-4', 1344, 'твёрдая', 890.00),
    ((SELECT id FROM books WHERE title_translated = 'Отверженные'), 'АСТ', 'Наталья Рыкова', 2019, '978-5-17-145678-9', 1344, 'твёрдая', 890.00),
    ((SELECT id FROM books WHERE title_translated = 'Повесть о Гэндзи'), 'Гиперион', 'Татьяна Соколова-Делюсина', 2018, '978-5-89332-345-6', 1216, 'твёрдая', 1200.00),
    ((SELECT id FROM books WHERE title_translated = 'Божественная комедия'), 'АСТ', 'Михаил Лозинский', 2021, '978-5-17-145678-8', 720, 'твёрдая', 680.00),
    ((SELECT id FROM books WHERE title_translated = 'Илиада'), 'Наука', 'Николай Гнедич', 2008, '978-5-02-025678-9', 528, 'мягкая', 350.00),
    ((SELECT id FROM books WHERE title_translated = 'Сто лет одиночества'), 'АСТ', 'Маргарита Былинкина', 2020, '978-5-17-118765-2', 416, 'твёрдая', 550.00);

-- 7. ЧИТАТЕЛИ
INSERT INTO readers (first_name, last_name, email, phone, birth_year, favorite_genre_id, favorite_country_id, registration_date) VALUES
    ('Анна', 'Каренина', 'anna.karenina@library.ru', '+7-900-111-22-33', 1985, (SELECT id FROM genres WHERE name = 'Роман'), (SELECT id FROM countries WHERE name = 'Россия'), '2025-01-10'),
    ('Евгений', 'Онегин', 'eugene.onegin@library.ru', '+7-900-222-33-44', 1990, (SELECT id FROM genres WHERE name = 'Поэма'), (SELECT id FROM countries WHERE name = 'Англия'), '2025-01-15'),
    ('Наташа', 'Ростова', 'natasha.rostova@library.ru', '+7-900-333-44-55', 2000, (SELECT id FROM genres WHERE name = 'Эпопея'), (SELECT id FROM countries WHERE name = 'Франция'), '2025-02-01'),
    ('Родион', 'Раскольников', 'rodion.raskolnikov@library.ru', '+7-900-444-55-66', 1988, (SELECT id FROM genres WHERE name = 'Философский роман'), (SELECT id FROM countries WHERE name = 'Германия'), '2025-02-20'),
    ('Пьер', 'Безухов', 'pierre.bezukhov@library.ru', '+7-900-555-66-77', 1975, (SELECT id FROM genres WHERE name = 'Роман'), (SELECT id FROM countries WHERE name = 'Италия'), '2025-03-01');

-- 8. ВЫДАЧА КНИГ
INSERT INTO loans (book_id, edition_id, reader_id, loan_date, due_date, return_date, purpose) VALUES
    ((SELECT id FROM books WHERE title_translated = 'Война и мир'), NULL, (SELECT id FROM readers WHERE email = 'anna.karenina@library.ru'), '2025-03-01', '2025-03-15', NULL, 'Исследование эпохи'),
    ((SELECT id FROM books WHERE title_translated = 'Отверженные'), (SELECT id FROM editions WHERE isbn = '978-5-17-145678-9'), (SELECT id FROM readers WHERE email = 'eugene.onegin@library.ru'), '2025-02-20', '2025-03-06', '2025-03-14', 'Досуг'),
    ((SELECT id FROM books WHERE title_translated = 'Повесть о Гэндзи'), (SELECT id FROM editions WHERE isbn = '978-5-89332-345-6'), (SELECT id FROM readers WHERE email = 'natasha.rostova@library.ru'), '2025-03-05', '2025-03-19', NULL, 'Изучение культуры'),
    ((SELECT id FROM books WHERE title_translated = 'Сто лет одиночества'), (SELECT id FROM editions WHERE isbn = '978-5-17-118765-2'), (SELECT id FROM readers WHERE email = 'pierre.bezukhov@library.ru'), '2025-03-07', '2025-03-21', NULL, 'Магический реализм'),
    ((SELECT id FROM books WHERE title_translated = 'Гамлет'), NULL, (SELECT id FROM readers WHERE email = 'rodion.raskolnikov@library.ru'), '2025-03-10', '2025-03-24', NULL, 'Изучение трагедии'),
    ((SELECT id FROM books WHERE title_translated = 'Илиада'), (SELECT id FROM editions WHERE isbn = '978-5-02-025678-9'), (SELECT id FROM readers WHERE email = 'anna.karenina@library.ru'), '2025-02-10', '2025-02-24', '2025-02-20', 'Античность'),
    ((SELECT id FROM books WHERE title_translated = 'Преступление и наказание'), (SELECT id FROM editions WHERE isbn = '978-5-389-12345-6'), (SELECT id FROM readers WHERE email = 'rodion.raskolnikov@library.ru'), '2025-03-12', '2025-03-26', NULL, 'Любимый автор');