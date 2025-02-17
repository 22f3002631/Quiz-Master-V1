import sqlite3 as sql

connection=sql.connect("quiz_database.db")
curobj=connection.cursor()

curobj.execute('PRAGMA foreign_keys=ON;')

curobj.execute("""
CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    qualification TEXT NOT NULL,
    dob TEXT NOT NULL
    )""")

curobj.execute("""
CREATE TABLE IF NOT EXISTS subject(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT NOT NULL
    )""")

curobj.execute("""
CREATE TABLE IF NOT EXISTS chapter(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    FOREIGN KEY(subject_id) REFERENCES subject(id) ON DELETE CASCADE
    )""")

curobj.execute("""
CREATE TABLE IF NOT EXISTS quiz(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter_id INTEGER NOT NULL,
    date_of_quiz TEXT NOT NULL,
    time_duration TEXT NOT NULL,
    FOREIGN KEY(chapter_id) REFERENCES chapter(id) ON DELETE CASCADE
    )""")

curobj.execute("""
CREATE TABLE IF NOT EXISTS question(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER NOT NULL,
    question_title TEXT NOT NULL,
    question_statement TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    option4 TEXT NOT NULL,
    correct_option INTEGER NOT NULL,
    FOREIGN KEY(quiz_id) REFERENCES quiz(id) ON DELETE CASCADE
    )""")

curobj.execute("""
CREATE TABLE IF NOT EXISTS scores(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    time_stamp_of_attempt DATETIME NOT NULL,
    FOREIGN KEY(quiz_id) REFERENCES quiz(id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
    )""")

curobj.execute("""
INSERT INTO user(id,username,password,full_name,qualification,dob) 
    VALUES (1,'admin','quizmaster$23','Quiz Master','N/A','N/A')
""")
connection.commit()
connection.close()
print("Database with all tables created successfully!")