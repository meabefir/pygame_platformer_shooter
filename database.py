import sqlite3

conn = sqlite3.connect('user_database.db')

# Create a cursor object to execute SQL commands
c = conn.cursor()

class USER:
    ID = 0
    USERNAME = 1
    PASSWORD = 2
    POINTS1 = 3
    LEFT = 9
    RIGHT = 10
    JUMP = 11
    SWITCH = 12
    USE = 13

# c.execute('''DROP TABLE users''')
# c.execute('''CREATE TABLE users
#              (id INTEGER PRIMARY KEY,
#               username TEXT UNIQUE,
#               password TEXT,
#               points1 INTEGER default 0,
#               points2 INTEGER default 0,
#               points3 INTEGER default 0,
#               points4 INTEGER default 0,
#               points5 INTEGER default 0,
#               points6 INTEGER default 0,
#               left INTEGER default 97,
#               right INTEGER default 100,
#               jump INTEGER default 32,
#               switch INTEGER default 113,
#               use INTEGER default 120
#               )''')

# c.execute("INSERT INTO users (username, password) VALUES ('user2', 'password2')")
# c.execute("INSERT INTO users (username, password) VALUES ('user4', 'password4')")
# c.execute("INSERT INTO users (username, password) VALUES ('user6', 'password6')")
# conn.commit()

c.execute("SELECT * FROM users")
# Fetch all the results
results = c.fetchall()
# Print the results
for row in results:
    print(row)

def get_users():
    c.execute("SELECT * FROM users")
    return c.fetchall()

def create_user(username, password):
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except:
        print("user already exists")
        return False

def login_user(username, password):
    c.execute(f"SELECT * FROM users where username=? and password=?", (username, password))
    user_data = c.fetchone()
    if user_data:
        print(f'logged in {user_data[USER.USERNAME]}')
        return {
            "username": user_data[USER.USERNAME],
            "points1": user_data[USER.POINTS1],
            "points2": user_data[USER.POINTS1+1],
            "points3": user_data[USER.POINTS1+2],
            "points4": user_data[USER.POINTS1+3],
            "points5": user_data[USER.POINTS1+4],
            "points6": user_data[USER.POINTS1+5],
            "left": user_data[USER.LEFT],
            "right": user_data[USER.RIGHT],
            "jump": user_data[USER.JUMP],
            "switch": user_data[USER.SWITCH],
            "use": user_data[USER.USE],
        }
    print("login failed")
    return None

def update_points(user, points_string, points):
    c.execute(f"update users set {points_string}=? where username=?", (points, user))
    conn.commit()

def udpate_binding(user, binding_name, value):
    c.execute(f"update users set {binding_name}=? where username=?", (value, user))
    conn.commit()

def close():
    conn.close()

login_user("user2", "password2")
# update_points("user2", "points1", 2)
# login_user("user2", "password2")

