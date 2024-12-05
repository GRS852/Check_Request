import configparser
import psycopg2 


class DbConnect:

    @staticmethod
    def load_config(db_name):
        config = configparser.ConfigParser()
        config.read("data/config.ini")

        if db_name not in config:
            raise ValueError(f"No section: '{db_name}'")

        return{
            "host": config.get(db_name, "host"),
            "port": config.get(db_name, "port"),
            "database": config.get(db_name, "database"),
            "user": config.get(db_name, "user"),
            "password": config.get(db_name, "password")
        }

    @staticmethod
    def connect_db(config, query, fetch_data = False, params = None):
        try:
            conn = psycopg2.connect(
                host = config["host"],
                port = config["port"],
                database = config["database"],
                user = config["user"],
                password = config["password"]
            )

            cur = conn.cursor()

            if params:
                cur.execute(query, params)
            
            else:
                cur.execute(query)
            
            if fetch_data:
                result = cur.fetchall()
            
            else:
                result = None

            if not fetch_data:
                conn.commit()

            cur.close
            conn.close()

            return result
        
        except Exception as e:
            print(f"Erro ao executar a query: {e}")
            return None
    