from DatabaseConnect import DatabaseConnect
from DatabaseInfo import DatabaseInfo

class DashboardExtras:
    def __init__(self):
        self.db = DatabaseInfo(
            'localhost',
            '5432',
            'postgres_db',
            'postgres_user',
            'admin'
        )

    def cltv_summary(self):
        try:
            table = DatabaseConnect()
            table.connect(self.db)
            table.cur.execute('SELECT * FROM cltv_summary')
            result = table.cur.fetchone()
            print result
            obj = {
                'min': result[0],
                '1q': result[1],
                'median': result[2],
                'mean': result[3],
                '3q': result[4],
                'max': result[5]
            }
            return obj
        except Exception as e:
            print e
            return None

    def arpu(self):
        try:
            table = DatabaseConnect()
            table.connect(self.db)
            table.cur.execute('SELECT * FROM profile_cl')
            results = table.cur.fetchall()
            obj = []
            for result in results:
                obj = {
                    'cluster': result[0],
                    'arpu': result[1]
                }
            return obj
        except Exception as e:
            print e
            return None



obj = DashboardExtras()
obj.cltv_summary()