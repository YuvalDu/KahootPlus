import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


class PlayersORM:
    def __init__(self):
        self.conn = None  # will store the DB connection
        self.cursor = None  # will store the DB connection cursor

    def open_DB(self):
        """
        will open DB file and put value in:
        self.conn (need DB file name)
        and self.cursor
        """
        self.conn = sqlite3.connect('Players.db')
        self.current = self.conn.cursor()

        self.current.execute("""
            CREATE TABLE IF NOT EXISTS PLAYERS(
            username text UNIQUE,
            password text,
            points int);
            """)

    def close_DB(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def add_player(self, user_name, password):
        # Called after getting REG from the client, to add a new player to the db
        self.open_DB()
        psw = generate_password_hash(password, "pbkdf2:sha256", 1)
        sql = "INSERT INTO PLAYERS(username, password, points) "
        sql += "VALUES('" + user_name + "','" + psw + "','" + str(0) + "')"
        self.current.execute(sql)
        self.commit()
        self.close_DB()

    def update_points(self, username, points):
        # Called at the end of a game, adding points by username
        self.open_DB()
        find = "SELECT POINTS FROM PLAYERS WHERE USERNAME = " + "'" + username + "'"
        old_points = self.current.execute(find).fetchone()[0]
        sql = "UPDATE PLAYERS SET POINTS = " + "'" + str(old_points + points) + "'" \
              + "WHERE USERNAME = " + "'" + username + "'"
        self.current.execute(sql)
        self.commit()
        self.close_DB()

    def check_log(self, username, password):
        # returns True / False for LOG information
        self.open_DB()
        sql = "SELECT PASSWORD FROM PLAYERS WHERE USERNAME = " + "'" + username + "'"
        real_pass = self.current.execute(sql).fetchone()
        self.close_DB()
        return check_password_hash(real_pass[0], password)

    def get_points(self, username):
        self.open_DB()
        sql = "SELECT POINTS FROM PLAYERS WHERE USERNAME = " + "'" + username + "'"
        points = self.current.execute(sql).fetchone()
        self.close_DB()
        return str(points[0])

    def get_all_usernames(self):
        # Returns a list of all users
        self.open_DB()
        sql = "SELECT USERNAME FROM PLAYERS"
        data = self.current.execute(sql).fetchall()
        self.close_DB()

        players = []
        for row in data:
            for cul in row:
                players.append(str(cul))
        return players

    def show_all_players(self):
        # Returns all table for debugging
        self.open_DB()
        sql = "SELECT * FROM PLAYERS"
        players = self.current.execute(sql).fetchall()
        self.close_DB()
        for row in players:
            print "---------"
            for cul in row:
                print cul
        print "---------"


def main():
    db = PlayersORM()
    print db.get_points("a")


if __name__ == '__main__':
    main()
