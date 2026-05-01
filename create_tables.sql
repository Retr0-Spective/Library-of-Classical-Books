-- СОЗДАНИЕ ТАБЛИЦ
-- 1. СТРАНЫ
CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    continent VARCHAR(50)
);

-- 2. ЛИТЕРАТУРНЫЕ НАПРАВЛЕНИЯ
CREATE TABLE literary_movements (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    century_origin VARCHAR(20)
);

-- 3. ЖАНРЫ
CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- 4. АВТОРЫ
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,
    birth_year INT,
    death_year INT,
    country_id INT REFERENCES countries(id),
    movement_id INT REFERENCES literary_movements(id),
    notable_works TEXT
);

-- 5. КНИГИ
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title_original VARCHAR(200),
    title_translated VARCHAR(200) NOT NULL,
    author_id INT REFERENCES authors(id),
    genre_id INT REFERENCES genres(id),
    movement_id INT REFERENCES literary_movements(id),
    century VARCHAR(20) NOT NULL,
    year_written INT,
    language_original VARCHAR(30),
    country_origin_id INT REFERENCES countries(id),
    is_epic BOOLEAN DEFAULT FALSE,
    word_count INT,
    total_copies INT DEFAULT 2,
    available_copies INT DEFAULT 2,
    
    CHECK (year_written > -3000),
    CHECK (total_copies >= 0),
    CHECK (available_copies BETWEEN 0 AND total_copies)
);

-- 6. ИЗДАНИЯ
CREATE TABLE editions (
    id SERIAL PRIMARY KEY,
    book_id INT NOT NULL REFERENCES books(id),
    publisher VARCHAR(100),
    translator VARCHAR(100),
    publication_year INT,
    isbn VARCHAR(20) UNIQUE,
    page_count INT,
    price DECIMAL(10, 2)
);

-- 7. ЧИТАТЕЛИ
CREATE TABLE readers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    birth_year INT,
    favorite_genre_id INT REFERENCES genres(id),
    favorite_country_id INT REFERENCES countries(id),
    registration_date DATE DEFAULT CURRENT_DATE
);

-- 8. ВЫДАЧА КНИГ
CREATE TABLE loans (
    id SERIAL PRIMARY KEY,
    book_id INT NOT NULL REFERENCES books(id),
    edition_id INT REFERENCES editions(id),
    reader_id INT NOT NULL REFERENCES readers(id),
    loan_date DATE NOT NULL DEFAULT CURRENT_DATE,
    due_date DATE NOT NULL,
    return_date DATE,
    purpose TEXT,
    
    CHECK (due_date >= loan_date),
    CHECK (return_date IS NULL OR return_date >= loan_date)
);


-- ИНДЕКСЫ
CREATE INDEX idx_books_author ON books(author_id);
CREATE INDEX idx_books_title ON books(title_translated);
CREATE INDEX idx_loans_dates ON loans(loan_date, due_date);


-- ПРОЕКЦИИ (VIEW)
-- 1. По одной таблице (доступные книги)
CREATE VIEW available_books AS
SELECT id, title_translated, author_id, available_copies
FROM books
WHERE available_copies > 0;

-- 2. По нескольким таблицам (информация о книгах)
CREATE VIEW books_info AS
SELECT 
    b.title_translated AS book_title,
    a.last_name AS author,
    c.name AS country,
    b.century,
    b.available_copies
FROM books b
JOIN authors a ON b.author_id = a.id
JOIN countries c ON b.country_origin_id = c.id;

-- 3. С GROUP BY и HAVING (статистика по странам)
CREATE VIEW country_statistics AS
SELECT 
    c.name AS country,
    COUNT(b.id) AS total_books,
    SUM(b.total_copies) AS total_copies
FROM countries c
LEFT JOIN books b ON c.id = b.country_origin_id
GROUP BY c.name
HAVING COUNT(b.id) >= 2;


-- ТРИГГЕР
CREATE OR REPLACE FUNCTION update_book_copies()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE books 
        SET available_copies = available_copies - 1 
        WHERE id = NEW.book_id;
    ELSIF TG_OP = 'UPDATE' AND NEW.return_date IS NOT NULL 
          AND OLD.return_date IS NULL THEN
        UPDATE books 
        SET available_copies = available_copies + 1 
        WHERE id = NEW.book_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER on_loan_change
AFTER INSERT OR UPDATE ON loans
FOR EACH ROW
EXECUTE FUNCTION update_book_copies();