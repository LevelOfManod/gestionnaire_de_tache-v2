import sqlite3


def cross_out(text):
    return ''.join([u'\u0336{}'.format(c) for c in text])

class Task:
    def __init__(self):
        self.db_nom = 'tasks.db'
        self.db_connect()
        self.curseur.execute("""CREATE TABLE IF NOT EXISTS Tasks
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             task TEXTE, state INTEGER)""")
        self.db_close()

    def db_connect(self):
        self.connection = sqlite3.connect(self.db_nom)
        self.curseur = self.connection.cursor()

    def db_close(self):
        self.connection.close()

    def exist(self, task):
        request = f"SELECT * FROM Tasks WHERE task = '{task}'"
        result = self.curseur.execute(request).fetchall
        return True if result else False

    def add(self, task, state=False):
        request = f"INSERT INTO Tasks (task, state) VALUES ('{task}',{int(state)})"
        self.curseur.execute(request)
        self.connection.commit()
    
    def display(self):
        request = "SELECT * FROM Tasks"
        tasks = self.curseur.execute(request).fetchall()
        print("--------------")
        for t in tasks:
            if t[2]: #si tache = True on barre
                print(f"{t[0]} - {cross_out(t[1])}, {t[2]}")
            else:
                print(f"{t[0]} - {t[1]}, {t[2]}")

    def finish(self, task):
        if self.exist(task):
            request = f"UPDATE Tasks SET state = 1 WHERE task = '{task}'"
            self.curseur.execute(request)
            self.connection.commit()
            print(f"{task} completed")
        else:
            print("The task doesn't exist")

    
    def delete(self, task):
        request = f"DELETE FROM Tasks WHERE task = '{task}'"
        self.curseur.execute(request)
        self.connection.commit()

tasks = Task()

try:
    tasks.db_connect()
    tasks.display()


except Exception as e:
    print("Erreur", e)

finally:
    tasks.db_close()


