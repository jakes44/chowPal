import sqlite3
import uuid

class DBManager(object):
    def __init__(self, path):
        self._db = sqlite3.connect(path, check_same_thread=False)
        self._c = self._db.cursor()

    def get_order_history(self, uid):
        query = '''SELECT did, rating FROM choices WHERE uid=?'''

        return self._c.execute(query, (uid,)).fetchall()

    def get_blurb(self, did):
        query = 'SELECT blurb FROM co_data WHERE did=?'
        
        res = self._c.execute(query, (did,)).fetchall()

        if len(res):
            return res
        else:
            return None

    def get_health(self, did):
        query = 'SELECT health_info FROM co_data WHERE did=?'

        res = self._c.execute(query, (did,)).fetchall()

        if len(res):
            return res
        else:
            return {}

    def get_score(self, did):
        query = 'SELECT avg(rating) FROM choices WHERE did=?'

        res = self._c.execute(query, (did,)).fetchall()

        return res[0][0]

    def get_personal_score(self, uid, did):
        query = 'SELECT avg(point) FROM choices WHERE did=? AND uid=?'

        res = self._c.execute(query, (did, uid)).fetchall()

        return res[0][0]

    def get_all_uid(self):
        query = 'SELECT uid FROM user_profile'

        res = self._c.execute(query).fetchall()

        return map(lambda a: a[0], res)

    def create_user_profile(self, dietary_restriction):
        uid = uuid.uuid4().hex
        query = 'INSERT INTO user_profile VALUES (?, ?)'
        
        self._c.execute(query, (uid, dietary_restriction))

        self._db.commit()

        return uid

    def add_user_choice():
        pass

    def close(self):
        self._db.close()

if __name__ == '__main__':
    db_manager = DBManager('DB/chow.db')
    db_manager.get_order_history("1234")
