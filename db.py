import sqlite3

def check_db():
    databaseFile = ("data.db")
    db = sqlite3.connect(databaseFile, check_same_thread=False)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM users")
        print("БД (1/2) знайдено")
    except sqlite3.OperationalError:
        print("БД (1/2) не знайдено")
        cursor.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INT)")
        print("БД (1/2) створено...")
    try:
        cursor.execute("SELECT * FROM files")
        print("БД (2/2) знайдено")
    except sqlite3.OperationalError:
        print("БД (2/2) не знайдено")
        cursor.execute("CREATE TABLE files(user_id INT, type TEXT, code TEXT, file_id TEXT, viwes INT DEFAULT (0), password TEXT)")
        print("БД (2/2) створено...")

def get_users_exist(user_id):
    db = sqlite3.connect("data.db", check_same_thread=False)
    cursor = db.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id, ))
    if cursor.fetchone() is None:
        return False
    else:
        return True

def add_user_to_db(user_id):
    db = sqlite3.connect('data.db', check_same_thread=False)
    cursor = db.cursor()
    user = [user_id]
    cursor.execute(f'''INSERT INTO users(user_id) VALUES(?)''', user)
    db.commit()

def add_new_file(user_id, type, code, file_id):
    db = sqlite3.connect('data.db', check_same_thread=False)
    cursor = db.cursor()
    data = [user_id, type, code, file_id]
    cursor.execute(f'''INSERT INTO files(user_id, type, code, file_id) VALUES(?,? ,? ,?)''', data)
    db.commit()
def add_new_file_with_password(user_id, type, code, file_id, password):
    db = sqlite3.connect('data.db', check_same_thread=False)
    cursor = db.cursor()
    data = [user_id, type, code, file_id, password]
    cursor.execute(f'''INSERT INTO files(user_id, type, code, file_id, password) VALUES(?,?,?,?,?)''', data)
    db.commit()
def get_file(code):
    db = sqlite3.connect('data.db', check_same_thread=False)
    cursor = db.cursor()
    cursor.execute("SELECT file_id FROM files WHERE code=?", (code, ))
    fileID = cursor.fetchone()
    cursor.execute("SELECT type FROM files WHERE code=?", (code, ))
    type_file = cursor.fetchone()
    cursor.execute("SELECT viwes FROM files WHERE code=?", (code, ))
    viwes = cursor.fetchone()
    cursor.execute("SELECT password FROM files WHERE code=?", (code, ))
    password = cursor.fetchone()
    return type_file, fileID, viwes, password

def get_files_user(user_id):
    db = sqlite3.connect('data.db', check_same_thread=False)
    cursor = db.cursor()
    cursor.execute("SELECT code FROM files WHERE user_id=?", (user_id, ))
    fileIDs = cursor.fetchall()
    cursor.execute("SELECT type FROM files WHERE user_id=?", (user_id, ))
    types_my_file = cursor.fetchall()
    cursor.execute("SELECT viwes FROM files WHERE user_id=?", (user_id, ))
    viwes = cursor.fetchall()
    cursor.execute("SELECT password FROM files WHERE user_id=?", (user_id, ))
    passwords = cursor.fetchall()
    return types_my_file, fileIDs, viwes, passwords
def update_viwes(code):
    db = sqlite3.connect('data.db', check_same_thread=False)
    cursor = db.cursor()
    cursor.execute("SELECT viwes FROM files WHERE code=?", (code, ))
    viwes = cursor.fetchone()
    cursor.execute("""UPDATE files SET viwes = ? WHERE code = ?""", (int(viwes[0])+1, code))
    db.commit()
def delete_file(code):
    db = sqlite3.connect('data.db', check_same_thread=False)
    cursor = db.cursor()
    cursor.execute("DELETE FROM files WHERE code = ?", (code, ))
    db.commit()