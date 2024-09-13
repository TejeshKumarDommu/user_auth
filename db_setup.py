import sqlite3

def init_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS roles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        created_by INTEGER,
        FOREIGN KEY (created_by) REFERENCES roles(id)
    )''')
    
    # Create a default Superadmin if not exists
    cursor.execute("SELECT * FROM roles WHERE role='Superadmin'")
    if cursor.fetchone() is None:
        cursor.execute('''INSERT INTO roles (username, password, role, created_by) 
                          VALUES ('superadmin', 'superadmin', 'Superadmin', NULL)''')
        print("Default Superadmin created.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
