import sqlite3

DB_PATH = 'sport.db'

def get_connection():
    """Возвращает соединение с БД с включённой поддержкой внешних ключей."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

#Добавление записей
def add_sportsman(ima, familia, data_rojdenia, razryad, id_kluba):
    """Добавляет нового спортсмена."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Sportsmeny (Ima, Familia, Data_rojdenia, Razryad, ID_Kluba)
        VALUES (?, ?, ?, ?, ?)
    """, (ima, familia, data_rojdenia, razryad, id_kluba))
    conn.commit()
    conn.close()

def add_trener(ima, familia, stazh):
    """Добавляет нового тренера."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Trenery (Ima, Familia, Stazh)
        VALUES (?, ?, ?)
    """, (ima, familia, stazh))
    conn.commit()
    conn.close()

#Выборка с условиями
def get_sportsmen_by_sport(vid_sporta, min_razryad=None):
    """
    Возвращает список спортсменов, занимающихся указанным видом спорта.
    Если указан min_razryad, фильтрует по разряду (сравнение строк).
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT s.Ima, s.Familia, s.Razryad, vs.Nazvanie
        FROM Sportsmeny s
        JOIN Trenirovki t ON s.ID_Sportsmena = t.ID_Sportsmena
        JOIN Vidy_sporta vs ON t.ID_Vida_sporta = vs.ID_Vida_sporta
        WHERE vs.Nazvanie = ?
    """
    params = [vid_sporta]
    if min_razryad:
        query += " AND s.Razryad >= ?"
        params.append(min_razryad)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_sportsmen_by_trener(trener_familia, min_razryad=None):
    """
    Возвращает список спортсменов, тренирующихся у указанного тренера.
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT s.Ima, s.Familia, s.Razryad, tr.Familia
        FROM Sportsmeny s
        JOIN Trenirovki t ON s.ID_Sportsmena = t.ID_Sportsmena
        JOIN Trenery tr ON t.ID_Trenera = tr.ID_Trenera
        WHERE tr.Familia = ?
    """
    params = [trener_familia]
    if min_razryad:
        query += " AND s.Razryad >= ?"
        params.append(min_razryad)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_prizers(sorevnovanie_nazvanie):
    """
    Возвращает призёров (1-3 места) указанного соревнования.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.Ima, s.Familia, r.Mesto, r.Nagrada
        FROM Rezultaty r
        JOIN Sportsmeny s ON r.ID_Sportsmena = s.ID_Sportsmena
        JOIN Sorevnovaniya so ON r.ID_Sorevnovaniya = so.ID_Sorevnovaniya
        WHERE so.Nazvanie = ? AND r.Mesto <= 3
        ORDER BY r.Mesto
    """, (sorevnovanie_nazvanie,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_sportsmen_with_multiple_sports():
    """
    Возвращает спортсменов, занимающихся более чем одним видом спорта,
    и список этих видов.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.Ima, s.Familia, GROUP_CONCAT(vs.Nazvanie, ', ') as Sports
        FROM Sportsmeny s
        JOIN Trenirovki t ON s.ID_Sportsmena = t.ID_Sportsmena
        JOIN Vidy_sporta vs ON t.ID_Vida_sporta = vs.ID_Vida_sporta
        GROUP BY s.ID_Sportsmena
        HAVING COUNT(DISTINCT vs.ID_Vida_sporta) > 1
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_club_stats_by_period(start_date, end_date):
    """
    Возвращает список клубов и количество их спортсменов,
    участвовавших в соревнованиях в указанный период.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT k.Nazvanie, COUNT(DISTINCT s.ID_Sportsmena) as SportsmenCount
        FROM Kluby k
        JOIN Sportsmeny s ON k.ID_Kluba = s.ID_Kluba
        JOIN Rezultaty r ON s.ID_Sportsmena = r.ID_Sportsmena
        JOIN Sorevnovaniya so ON r.ID_Sorevnovaniya = so.ID_Sorevnovaniya
        WHERE so.Data_nachala BETWEEN ? AND ?
        GROUP BY k.ID_Kluba
        ORDER BY SportsmenCount DESC
    """, (start_date, end_date))
    rows = cursor.fetchall()
    conn.close()
    return rows

#Обновление данных
def update_sportsman_rank(sportsman_id, new_razryad):
    """Обновляет разряд спортсмена."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Sportsmeny SET Razryad = ? WHERE ID_Sportsmena = ?
    """, (new_razryad, sportsman_id))
    conn.commit()
    conn.close()

#Удаление данных
def delete_sportsman(sportsman_id):
    """
    Удаляет спортсмена и все связанные записи (результаты, тренировки).
    """
    conn = get_connection()
    cursor = conn.cursor()
    # Удаляем связанные записи (сначала результаты, затем тренировки)
    cursor.execute("DELETE FROM Rezultaty WHERE ID_Sportsmena = ?", (sportsman_id,))
    cursor.execute("DELETE FROM Trenirovki WHERE ID_Sportsmena = ?", (sportsman_id,))
    cursor.execute("DELETE FROM Sportsmeny WHERE ID_Sportsmena = ?", (sportsman_id,))
    conn.commit()
    conn.close()