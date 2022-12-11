import sqlite3
QUIZZES_FOLDER = r"E:\\FinalProj\\Quizzes\\"
QUIZ_DB = "Quizzes.db"


class QuizzesORM:
    def __init__(self, name):
        self.conn = None  # will store the DB connection
        self.cursor = None  # will store the DB connection cursor
        self.name = "_".join(name.split())  # reformat the name of the quiz and make all spaces into : '_'

    def open_DB(self):
        """
        will open DB file and put value in:
        self.conn (need DB file name)
        and self.cursor
        """

        self.conn = sqlite3.connect(QUIZZES_FOLDER + QUIZ_DB)
        self.current = self.conn.cursor()

        create = """CREATE TABLE IF NOT EXISTS %s(question text, RAnswer text, WAnswer1 text, WAnswer2 text,
         WAnswer3 text);""" % self.name
        self.current.execute(create)

    def add_question(self, question, RAnswer, WAnswer1, WAnswer2, WAnswer3):
        # Called after getting REG from the client, to add a new player to the db
        self.open_DB()
        sql = "INSERT INTO %s(question, RAnswer, WAnswer1, WAnswer2, WAnswer3) " % self.name
        sql += "VALUES('" + question + "','" + RAnswer + "','" + WAnswer1 + "','" + WAnswer2 + "','" + WAnswer3 + "')"
        self.current.execute(sql)
        self.commit()
        self.close_DB()

    def close_DB(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def get_quiz(self):
        # Returns all table for showing in the quiz
        self.open_DB()
        sql = "SELECT * FROM %s" % self.name
        data = self.current.execute(sql).fetchall()
        self.close_DB()
        quiz = {}
        for a in data:
            quiz[str(a[0])] = [str(a[1])]
            for wa in a[2:]:
                quiz[str(a[0])].append(str(wa))
        return quiz

    def get_quizzes(self):
        self.conn = sqlite3.connect(QUIZZES_FOLDER + QUIZ_DB)
        self.current = self.conn.cursor()
        sql = "SELECT name FROM sqlite_master WHERE type='table'"
        data = self.current.execute(sql).fetchall()
        self.close_DB()
        quizzes = []
        for q in data:
            quizzes.append(str(q[0]))
        return quizzes


def main():
    db = QuizzesORM("Capital_Cities")
    print db.get_quizzes()


if __name__ == '__main__':
    main()
