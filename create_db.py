import sqlite3

DB_NAME = "sport.db"

def create_tables(cursor):
    """Создание всех таблиц (если их нет)"""
    cursor.executescript("""
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS Vidy_sporta (
            ID_Vida_sporta INTEGER PRIMARY KEY AUTOINCREMENT,
            Nazvanie TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS Kluby (
            ID_Kluba INTEGER PRIMARY KEY AUTOINCREMENT,
            Nazvanie TEXT NOT NULL UNIQUE,
            Adres TEXT
        );

        CREATE TABLE IF NOT EXISTS Obekty (
            ID_Obekta INTEGER PRIMARY KEY AUTOINCREMENT,
            Nazvanie TEXT NOT NULL,
            Tip TEXT,
            Vmestimost INTEGER,
            Poverkhnost TEXT
        );

        CREATE TABLE IF NOT EXISTS Organizatory (
            ID_Organizatora INTEGER PRIMARY KEY AUTOINCREMENT,
            Nazvanie TEXT NOT NULL UNIQUE,
            Telefon TEXT
        );

        CREATE TABLE IF NOT EXISTS Sorevnovaniya (
            ID_Sorevnovaniya INTEGER PRIMARY KEY AUTOINCREMENT,
            Nazvanie TEXT NOT NULL,
            Data_nachala TEXT NOT NULL,
            Data_okonchania TEXT,
            ID_Vida_sporta INTEGER NOT NULL,
            ID_Obekta INTEGER,
            Gorod TEXT,
            FOREIGN KEY (ID_Vida_sporta) REFERENCES Vidy_sporta(ID_Vida_sporta) ON DELETE RESTRICT,
            FOREIGN KEY (ID_Obekta) REFERENCES Obekty(ID_Obekta) ON DELETE RESTRICT
        );

        CREATE TABLE IF NOT EXISTS Sportsmeny (
            ID_Sportsmena INTEGER PRIMARY KEY AUTOINCREMENT,
            Ima TEXT NOT NULL,
            Familia TEXT NOT NULL,
            Data_rojdenia TEXT,
            Razryad TEXT,
            ID_Kluba INTEGER NOT NULL,
            FOREIGN KEY (ID_Kluba) REFERENCES Kluby(ID_Kluba) ON DELETE RESTRICT
        );

        CREATE TABLE IF NOT EXISTS Trenery (
            ID_Trenera INTEGER PRIMARY KEY AUTOINCREMENT,
            Ima TEXT NOT NULL,
            Familia TEXT NOT NULL,
            Stazh INTEGER
        );

        CREATE TABLE IF NOT EXISTS Rezultaty (
            ID_Rezultata INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Sorevnovaniya INTEGER NOT NULL,
            ID_Sportsmena INTEGER NOT NULL,
            Mesto INTEGER,
            Nagrada TEXT,
            Luchshiy_rezultat TEXT,
            UNIQUE (ID_Sorevnovaniya, ID_Sportsmena),
            FOREIGN KEY (ID_Sorevnovaniya) REFERENCES Sorevnovaniya(ID_Sorevnovaniya) ON DELETE RESTRICT,
            FOREIGN KEY (ID_Sportsmena) REFERENCES Sportsmeny(ID_Sportsmena) ON DELETE RESTRICT
        );

        CREATE TABLE IF NOT EXISTS Sorevnovaniya_Organizatory (
            ID_Sorevnovaniya INTEGER NOT NULL,
            ID_Organizatora INTEGER NOT NULL,
            PRIMARY KEY (ID_Sorevnovaniya, ID_Organizatora),
            FOREIGN KEY (ID_Sorevnovaniya) REFERENCES Sorevnovaniya(ID_Sorevnovaniya) ON DELETE RESTRICT,
            FOREIGN KEY (ID_Organizatora) REFERENCES Organizatory(ID_Organizatora) ON DELETE RESTRICT
        );

        CREATE TABLE IF NOT EXISTS Trenirovki (
            ID_Trenirovki INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Sportsmena INTEGER NOT NULL,
            ID_Trenera INTEGER NOT NULL,
            ID_Vida_sporta INTEGER NOT NULL,
            Data_trenirovki TEXT,
            Dlitelnost_minuty INTEGER,
            UNIQUE (ID_Sportsmena, ID_Trenera, ID_Vida_sporta, Data_trenirovki),
            FOREIGN KEY (ID_Sportsmena) REFERENCES Sportsmeny(ID_Sportsmena) ON DELETE RESTRICT,
            FOREIGN KEY (ID_Trenera) REFERENCES Trenery(ID_Trenera) ON DELETE RESTRICT,
            FOREIGN KEY (ID_Vida_sporta) REFERENCES Vidy_sporta(ID_Vida_sporta) ON DELETE RESTRICT
        );
    """)

def is_table_empty(cursor, table_name):
    """Проверяет, пуста ли таблица"""
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    return cursor.fetchone()[0] == 0

def fill_database(cursor):
    """Заполнение таблиц данными, если они пусты"""

    # Vidy_sporta
    if is_table_empty(cursor, "Vidy_sporta"):
        cursor.executemany(
            "INSERT INTO Vidy_sporta (ID_Vida_sporta, Nazvanie) VALUES (?, ?)",
            [(1, 'Футбол'), (2, 'Баскетбол'), (3, 'Хоккей'), (4, 'Теннис'), (5, 'Плавание')]
        )
        print("✓ Vidy_sporta")

    # Kluby
    if is_table_empty(cursor, "Kluby"):
        clubs = [
            (1, 'Спартак', 'г. Москва, ул. Спортивная, д. 1'),
            (2, 'ЦСКА', 'г. Москва, Ленинградский проспект, д. 39'),
            (3, 'Динамо', 'г. Москва, ул. Петровка, д. 26'),
            (4, 'Локомотив', 'г. Москва, ул. Болотная, д. 7'),
            (5, 'Крылья Советов', 'г. Москва, Волгоградский проспект, д. 46'),
        ]
        cursor.executemany("INSERT INTO Kluby (ID_Kluba, Nazvanie, Adres) VALUES (?, ?, ?)", clubs)
        print("✓ Kluby")

    # Obekty
    if is_table_empty(cursor, "Obekty"):
        objects = [
            (1, 'Лужники', 'Стадион', 81000, 'Искусственный газон'),
            (2, 'ЦСКА Арена', 'Стадион', 30000, 'Натуральный газон'),
            (3, 'ВТБ Арена', 'Дворец спорта', 15000, 'Паркет'),
            (4, 'Олимпийский', 'Бассейн', 5000, 'Вода'),
            (5, 'Сокольники', 'Теннисный центр', 8000, 'Хард'),
        ]
        cursor.executemany("INSERT INTO Obekty (ID_Obekta, Nazvanie, Tip, Vmestimost, Poverkhnost) VALUES (?, ?, ?, ?, ?)", objects)
        print("✓ Obekty")

    # Organizatory
    if is_table_empty(cursor, "Organizatory"):
        organizers = [
            (1, 'Московская федерация футбола', 'тел: +7-495-111-11-11'),
            (2, 'Российский олимпийский комитет', 'тел: +7-495-222-22-22'),
            (3, 'Департамент спорта Москвы', 'тел: +7-495-333-33-33'),
            (4, 'Спортивный клуб "Столица"', 'тел: +7-495-444-44-44'),
            (5, 'Ассоциация студенческого спорта', 'тел: +7-495-555-55-55'),
        ]
        cursor.executemany("INSERT INTO Organizatory (ID_Organizatora, Nazvanie, Telefon) VALUES (?, ?, ?)", organizers)
        print("✓ Organizatory")

    # Sorevnovaniya
    if is_table_empty(cursor, "Sorevnovaniya"):
        competitions = [
            (1, 'Кубок Москвы по футболу', '2024-05-01', '2024-05-10', 1, 1, 'Москва'),
            (2, 'Чемпионат Москвы по баскетболу', '2024-06-15', '2024-06-25', 2, 3, 'Москва'),
            (3, 'Зимний турнир по хоккею', '2024-12-01', '2024-12-05', 3, 3, 'Москва'),
            (4, 'Открытый теннисный чемпионат', '2024-07-10', '2024-07-20', 4, 5, 'Москва'),
            (5, 'Соревнования по плаванию "Волна"', '2024-08-05', '2024-08-07', 5, 4, 'Москва'),
        ]
        cursor.executemany("INSERT INTO Sorevnovaniya (ID_Sorevnovaniya, Nazvanie, Data_nachala, Data_okonchania, ID_Vida_sporta, ID_Obekta, Gorod) VALUES (?, ?, ?, ?, ?, ?, ?)", competitions)
        print("✓ Sorevnovaniya")

    # Sportsmeny
    if is_table_empty(cursor, "Sportsmeny"):
        sportsmen = [
            (1, 'Александр', 'Смирнов', '1998-05-15', 'КМС', 1),
            (2, 'Денис', 'Васильев', '2000-03-22', '1 разряд', 2),
            (3, 'Павел', 'Морозов', '1999-11-08', 'КМС', 3),
            (4, 'Артем', 'Никитин', '2001-07-30', '2 разряд', 4),
            (5, 'Игорь', 'Федоров', '1997-12-14', 'МС', 5),
        ]
        cursor.executemany("INSERT INTO Sportsmeny (ID_Sportsmena, Ima, Familia, Data_rojdenia, Razryad, ID_Kluba) VALUES (?, ?, ?, ?, ?, ?)", sportsmen)
        print("✓ Sportsmeny")

    # Trenery
    if is_table_empty(cursor, "Trenery"):
        trainers = [
            (1, 'Иван', 'Петров', 10),
            (2, 'Сергей', 'Иванов', 8),
            (3, 'Алексей', 'Сидоров', 12),
            (4, 'Дмитрий', 'Кузнецов', 6),
            (5, 'Михаил', 'Попов', 15),
        ]
        cursor.executemany("INSERT INTO Trenery (ID_Trenera, Ima, Familia, Stazh) VALUES (?, ?, ?, ?)", trainers)
        print("✓ Trenery")

    # Rezultaty
    if is_table_empty(cursor, "Rezultaty"):
        results = [
            (1, 1, 1, 1, 'Золотая медаль', '3 гола'),
            (2, 1, 2, 2, 'Серебряная медаль', '2 гола'),
            (3, 2, 3, 1, 'Золотая медаль', '25 очков'),
            (4, 3, 4, 3, 'Бронзовая медаль', '2 шайбы'),
            (5, 4, 5, 2, 'Серебряная медаль', '6:4, 6:3'),
        ]
        cursor.executemany("INSERT INTO Rezultaty (ID_Rezultata, ID_Sorevnovaniya, ID_Sportsmena, Mesto, Nagrada, Luchshiy_rezultat) VALUES (?, ?, ?, ?, ?, ?)", results)
        print("✓ Rezultaty")

    # Sorevnovaniya_Organizatory
    if is_table_empty(cursor, "Sorevnovaniya_Organizatory"):
        comp_org = [
            (1, 1),
            (2, 2),
            (1, 3),
            (3, 4),
            (4, 5),
        ]
        cursor.executemany("INSERT INTO Sorevnovaniya_Organizatory (ID_Sorevnovaniya, ID_Organizatora) VALUES (?, ?)", comp_org)
        print("✓ Sorevnovaniya_Organizatory")

    # Trenirovki
    if is_table_empty(cursor, "Trenirovki"):
        trainings = [
            (1, 1, 1, 1, '2024-04-20', 120),
            (2, 2, 2, 2, '2024-04-21', 90),
            (3, 3, 3, 3, '2024-04-22', 150),
            (4, 4, 4, 4, '2024-04-23', 120),
            (5, 5, 5, 5, '2024-04-24', 100),
        ]
        cursor.executemany("INSERT INTO Trenirovki (ID_Trenirovki, ID_Sportsmena, ID_Trenera, ID_Vida_sporta, Data_trenirovki, Dlitelnost_minuty) VALUES (?, ?, ?, ?, ?, ?)", trainings)
        print("✓ Trenirovki")

def main():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # Создаём таблицы
        create_tables(cursor)
        print("Таблицы созданы (или уже существуют).")

        # Заполняем данными
        fill_database(cursor)
        conn.commit()
        print("\nБаза данных успешно создана и заполнена!")

    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()