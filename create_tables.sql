<<<<<<< HEAD
-- Мировая классическая библиотека
-- 1. СТРАНЫ
CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    continent VARCHAR(50),
    language_official VARCHAR(50),
    code VARCHAR(3)
);

-- 2. ЛИТЕРАТУРНЫЕ НАПРАВЛЕНИЯ
CREATE TABLE literary_movements (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    century_origin VARCHAR(20),
    description TEXT
);

-- 3. ЖАНРЫ
CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    category VARCHAR(30)
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
    notable_works TEXT,
    biography TEXT
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
    year_published_first INT,
    language_original VARCHAR(30),
    country_origin_id INT REFERENCES countries(id),
    is_epic BOOLEAN DEFAULT FALSE,
    word_count INT,
    plot_summary TEXT,
    total_copies INT DEFAULT 2,
    available_copies INT DEFAULT 2
);

-- 6. ИЗДАНИЯ (ISBN теперь UNIQUE, но без дубликатов)
CREATE TABLE editions (
    id SERIAL PRIMARY KEY,
    book_id INT NOT NULL REFERENCES books(id),
    publisher VARCHAR(100),
    translator VARCHAR(100),
    publication_year INT,
    isbn VARCHAR(20) UNIQUE,
    page_count INT,
    cover_type VARCHAR(20),
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
    purpose TEXT
>>>>>>> 48fc7733325149068a85980c584f5015cfef5956
);
