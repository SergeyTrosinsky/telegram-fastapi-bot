from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI(title="Спортивная инфраструктура API")

DB_PATH = "sport.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def row_to_dict(row):
    return {key: row[key] for key in row.keys()}

# Корневой эндпоинт
@app.get("/")
def root():
    return {"message": "API спортивной базы данных работает"}

# Получить всех спортсменов с названием клуба
@app.get("/sportsmen")
def get_sportsmen():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.ID_Sportsmena, s.Ima, s.Familia, s.Data_rojdenia, s.Razryad, k.Nazvanie AS Klub
        FROM Sportsmeny s
        JOIN Kluby k ON s.ID_Kluba = k.ID_Kluba
    """)
    rows = cursor.fetchall()
    conn.close()
    return {"sportsmen": [row_to_dict(r) for r in rows]}

# Получить одного спортсмена по ID
@app.get("/sportsmen/{sportsman_id}")
def get_sportsman(sportsman_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.ID_Sportsmena, s.Ima, s.Familia, s.Data_rojdenia, s.Razryad, k.Nazvanie AS Klub
        FROM Sportsmeny s
        JOIN Kluby k ON s.ID_Kluba = k.ID_Kluba
        WHERE s.ID_Sportsmena = ?
    """, (sportsman_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Спортсмен не найден")
    return row_to_dict(row)

# Получить список всех клубов
@app.get("/clubs")
def get_clubs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID_Kluba, Nazvanie, Adres FROM Kluby")
    rows = cursor.fetchall()
    conn.close()
    return {"clubs": [row_to_dict(r) for r in rows]}

# Получить все соревнования с видом спорта и объектом
@app.get("/competitions")
def get_competitions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT so.ID_Sorevnovaniya, so.Nazvanie, so.Data_nachala, so.Data_okonchania,
               vs.Nazvanie AS Vid_sporta, ob.Nazvanie AS Obekt, so.Gorod
        FROM Sorevnovaniya so
        JOIN Vidy_sporta vs ON so.ID_Vida_sporta = vs.ID_Vida_sporta
        LEFT JOIN Obekty ob ON so.ID_Obekta = ob.ID_Obekta
    """)
    rows = cursor.fetchall()
    conn.close()
    return {"competitions": [row_to_dict(r) for r in rows]}

# Получить призёров конкретного соревнования по названию
@app.get("/prizers/{competition_name}")
def get_prizers(competition_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.Ima, s.Familia, r.Mesto, r.Nagrada
        FROM Rezultaty r
        JOIN Sportsmeny s ON r.ID_Sportsmena = s.ID_Sportsmena
        JOIN Sorevnovaniya so ON r.ID_Sorevnovaniya = so.ID_Sorevnovaniya
        WHERE so.Nazvanie = ? AND r.Mesto <= 3
        ORDER BY r.Mesto
    """, (competition_name,))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="Соревнование не найдено или нет призёров")
    return {"prizers": [row_to_dict(r) for r in rows]}