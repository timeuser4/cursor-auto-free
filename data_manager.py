import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="accounts.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        if not self._table_exists():
            self._create_table()
    
    def _table_exists(self):
        self.cursor.execute('''
            SELECT name FROM sqlite_master WHERE type='table' AND name='accounts'
        ''')
        return self.cursor.fetchone() is not None
    
    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL, 
                email TEXT NOT NULL,
                account TEXT NOT NULL,
                password TEXT NOT NULL,
                date TIMESTAMP NOT NULL
            )
        ''')
        self.conn.commit()
    
    def push(self, firstname, lastname, email, account, password):
        current_time = datetime.now()
        self.cursor.execute('''
            INSERT INTO accounts (firstname, lastname, email, account, password, date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (firstname, lastname, email, account, password, current_time))
        self.conn.commit()
    
    def peek(self):
        self.cursor.execute('''
            SELECT firstname, lastname, email, account, password, date 
            FROM accounts 
            ORDER BY date ASC LIMIT 1
        ''')
        return self.cursor.fetchone()
    
    def pop(self):
        self.cursor.execute('''
            SELECT firstname, lastname, email, account, password, date 
            FROM accounts 
            ORDER BY date ASC LIMIT 1
        ''')
        result = self.cursor.fetchone()
        
        if result:
            self.cursor.execute('DELETE FROM accounts WHERE date = ?', (result[5],))
            self.conn.commit()
            return {
                'firstname': result[0],
                'lastname': result[1],
                'email': result[2],
                'account': result[3],
                'password': result[4],
                'date': result[5]
            }
        return None
    
    def size(self):
        self.cursor.execute('SELECT COUNT(*) FROM accounts')
        return self.cursor.fetchone()[0]
    
    def delete(self, id):
        self.cursor.execute('DELETE FROM accounts WHERE id = ?', (id,))
        self.conn.commit()
    
    def search(self, firstname=None, lastname=None, email=None, account=None, password=None):
        # FIXME: search结果总是None
        query = 'SELECT * FROM accounts WHERE'
        params = []
        if firstname:
            query += ' firstname = ? AND'
            params.append(firstname)
        if lastname:
            query += ' lastname = ? AND'
            params.append(lastname)
        if email:
            query += ' email = ? AND'
            params.append(email)
        if account:
            query += ' account = ? AND'
            params.append(account)
        if password:
            query += ' password = ? AND'
            params.append(password)
        if query.endswith('AND'):
            query = query[:-4]
        if not query.endswith('WHERE'):
            query += ' LIMIT 1'
        print(query)
        print(params)
        query = 'SELECT * FROM accounts WHERE firstname = ? LIMIT 1'
        params = ['John']
        return self.cursor.fetchone()
    
    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    db = DatabaseManager()
    db.push("John", "Doe", "john.doe@example.com", "johndoe", "password123")
    print(db.peek())
    print(db.pop())
    print(db.size())
    print(db.search(firstname="John"))
    db.delete(1)
