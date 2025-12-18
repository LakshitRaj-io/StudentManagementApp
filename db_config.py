import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": " ",
    "database": "student_result_db",
}


def get_connection():
    """Return a MySQL connection using the config above."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print("Error while connecting to MySQL:", e)
    return None


def init_db():
    """Create database tables if they do not exist."""
    try:
        # Connect without database first to ensure DB exists
        base_conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
        )
        base_conn.autocommit = True
        cur = base_conn.cursor()
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}"
        )
        cur.close()
        base_conn.close()

        conn = get_connection()
        if not conn:
            print("Could not connect to database.")
            return
        cur = conn.cursor()

        # users table for login
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
            """
        )

        # subjects table (teacher can add subjects)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS subjects (
                id INT AUTO_INCREMENT PRIMARY KEY,
                subject_name VARCHAR(100) NOT NULL UNIQUE
            )
            """
        )

        # students table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                roll_no VARCHAR(20) UNIQUE NOT NULL,
                name VARCHAR(100) NOT NULL,
                class_name VARCHAR(50),
                section VARCHAR(10)
            )
            """
        )

        # marks table (many-to-many: students x subjects)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS marks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                subject_id INT NOT NULL,
                marks_obtained FLOAT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id)
                    ON DELETE CASCADE,
                FOREIGN KEY (subject_id) REFERENCES subjects(id)
                    ON DELETE CASCADE
            )
            """
        )

        # create a default teacher user if not exists
        cur.execute(
            """
            INSERT IGNORE INTO users (username, password)
            VALUES ('teacher', 'teacher123')
            """
        )

        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully.")

    except Error as e:
        print("Error during DB initialization:", e)

