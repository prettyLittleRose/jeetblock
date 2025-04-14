import json
import sqlite3

class Settings:
    def __init__(self, db_path: str = 'settings.db'):
        self.db_path = db_path
        self.__init_db__()

    def __init_db__(self) -> None:
        conn = sqlite3.connect(self.db_path)
        curs = conn.cursor()

        curs.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                countries TEXT DEFAULT '[]',
                delete_chat INTEGER DEFAULT 0,
                block_user INTEGER DEFAULT 0,
                log_user_info INTEGER DEFAULT 0,
                log_block INTEGER DEFAULT 1,
                log_delete INTEGER DEFAULT 1,
                log_errors INTEGER DEFAULT 0
            )
        ''')

        curs.execute('SELECT COUNT(*) FROM settings')
        if curs.fetchone()[0] == 0:
            curs.execute('INSERT INTO settings DEFAULT VALUES')

        conn.commit()
        conn.close()

    def add_countries(self, countries: list = []) -> None:
        conn = sqlite3.connect(self.db_path)
        curs = conn.cursor()

        current = self.get_countries()
        updated = list(set(current + countries))
        curs.execute('UPDATE settings SET countries = ?', (json.dumps(updated),))

        conn.commit()
        conn.close()

    def remove_countries(self, countries: list = []) -> None:
        conn = sqlite3.connect(self.db_path)
        curs = conn.cursor()

        current = self.get_countries()
        updated = current
        for country in countries:
            if country in updated:
                updated.remove(country)

        curs.execute('UPDATE settings SET countries = ?', (json.dumps(updated),))

        conn.commit()
        conn.close()

    def configure_delete_chat(self, enable: bool) -> None:
        conn = sqlite3.connect(self.db_path)
        curs = conn.cursor()

        curs.execute('UPDATE settings SET delete_chat = ?', (1 if enable else 0,))

        conn.commit()
        conn.close()

    def configure_block_user(self, enable: bool) -> None:
        conn = sqlite3.connect(self.db_path)
        curs = conn.cursor()

        curs.execute('UPDATE settings SET block_user = ?', (1 if enable else 0,))

        conn.commit()
        conn.close()

    def configure_log_user_info(self, enable: bool) -> None:
        conn = sqlite3.connect(self.db_path)
        curs = conn.cursor()

        curs.execute('UPDATE settings SET log_user_info = ?', (1 if enable else 0,))

        conn.commit()
        conn.close()

    def configure_log_block(self, enable: bool) -> None:
        conn = sqlite3.connect(self.db_path)
        curs = conn.cursor()

        curs.execute('UPDATE settings SET log_block = ?', (1 if enable else 0,))

        conn.commit()
        conn.close()

    def configure_log_delete(self, enable: bool) -> None:
        conn = sqlite3.connect(self.db_path)
        curs = conn.cursor()

        curs.execute('UPDATE settings SET log_delete = ?', (1 if enable else 0,))

        conn.commit()
        conn.close()

    def configure_log_errors(self, enable: bool) -> None:
        conn = sqlite3.connect(self.db_path)
        curs = conn.cursor()

        curs.execute('UPDATE settings SET log_errors = ?', (1 if enable else 0,))

        conn.commit()
        conn.close()

    def get_delete_chat(self) -> bool:
        conn = sqlite3.connect(self.db_path)
        curs = conn.cursor()

        curs.execute('SELECT delete_chat FROM settings')
        result = curs.fetchone()[0]
        conn.close()

        return bool(result)

    def get_block_user(self) -> bool:
        conn = sqlite3.connect(self.db_path)
        curs = conn.cursor()

        curs.execute('SELECT block_user FROM settings')
        result = curs.fetchone()[0]
        conn.close()

        return bool(result)

    def get_log_user_info(self) -> bool:
        conn = sqlite3.connect(self.db_path)
        curs = conn.cursor()
        
        curs.execute('SELECT log_user_info FROM settings')
        result = curs.fetchone()[0]
        conn.close()

        return bool(result)

    def get_log_block(self) -> bool:
        conn = sqlite3.connect(self.db_path)
        curs = conn.cursor()

        curs.execute('SELECT log_block FROM settings')
        result = curs.fetchone()[0]
        conn.close()

        return bool(result)

    def get_log_delete(self) -> bool:
        conn = sqlite3.connect(self.db_path)
        curs = conn.cursor()

        curs.execute('SELECT log_delete FROM settings')
        result = curs.fetchone()[0]
        conn.close()

        return bool(result)

    def get_log_errors(self) -> bool:
        conn = sqlite3.connect(self.db_path)
        curs = conn.cursor()

        curs.execute('SELECT log_errors FROM settings')
        result = curs.fetchone()[0]
        conn.close()

        return bool(result)

    def get_countries(self) -> list:
        conn = sqlite3.connect(self.db_path)
        curs = conn.cursor()

        curs.execute('SELECT countries FROM settings')
        result = json.loads(curs.fetchone()[0])
        conn.close()
        
        return result
