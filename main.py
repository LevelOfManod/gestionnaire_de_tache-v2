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

    def exist(self, task_id):
        request = f"SELECT * FROM Tasks WHERE id = ?"
        result = self.curseur.execute(request, (task_id)).fetchall
        return True if result else False

    def add(self, task, state=False):
        request = f"INSERT INTO Tasks (task, state) VALUES (?, ?)"
        self.curseur.execute(request ,(task, int(state)))
        self.connection.commit()
        task_id = self.curseur.lastrowid
        return task_id
    

    def display(self):
        ask = "SELECT COUNT(*) FROM Tasks"
        request_asked = self.curseur.execute(ask).fetchone()
        if request_asked[0] == 0:
            print("Your task list is empty")

        else:
            request = "SELECT * FROM Tasks"
            tasks = self.curseur.execute(request).fetchall()
            for t in tasks:
                if t[2]:
                    print(f"{t[0]} - {cross_out(t[1])}, {t[2]}")
                else:
                    print(f"{t[0]} - {t[1]}, {t[2]}")
    

    def finish(self, task_id):
        if self.exist(task_id):
            request = f"UPDATE Tasks SET state = 1 WHERE id = ?"
            self.curseur.execute(request, (task_id))
            self.connection.commit()
            print(f"{task_id} completed")
        else:
            print("The task doesn't exist")

    
    def delete(self, task_id):
        request = f"DELETE FROM Tasks WHERE id = ?"
        self.curseur.execute(request, (task_id))
        self.connection.commit()

    def delete_all(self):
        request = f"DELETE FROM Tasks"
        self.curseur.execute(request)

        request_update = "UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'Tasks'"
        self.curseur.execute(request_update)
        self.connection.commit()

        
    

tasks = Task()

try:
    tasks.db_connect()

    while True:
        cmd = print("\n\n")
        cmd = print("----------------------------------------------------------------------")
        cmd = input("Enter a command (+: Add, -: End, d: Delete, v: View, o: Option q: Quit)\n----------------------------------------------------------------------\ncmd: ")

        if cmd == "+":
            task = input("Enter the name: ")
            tasks.add(task)


        elif cmd == "-":
            idx = input("Enter the task id: ")
            tasks.finish(idx)
        
        elif cmd == "d":
            idx = input("Enter the task id: ")
            tasks.delete(idx)

        elif cmd == "v":
            tasks.display()
        
        elif cmd == "o":
            cmd = input("Delete all tasks y/n ?")
            if cmd == "y":
                tasks.delete_all()
                print(" ! ! ! All tasks have been deleted ! ! ! ")
                break

            elif cmd == "n":
                continue

        elif cmd == "q":
            break
        
        else:
            print("Invalid order")


except Exception as e:
    print("Erreur", e)

finally:
    tasks.db_close()