import psycopg2
import pandas as pd


class pgsql_conn(object):

    def __init__(self, host_name, port_name, database_name, user_name, password_name):
        self.connection = psycopg2.connect(host=host_name,
                                           port=port_name,
                                           database=database_name,
                                           user=user_name,
                                           password=password_name)

    def read_sql(self, sql_string):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(sql_string)
                output = cursor.fetchall()
                col_names = [desc[0] for desc in cursor.description]

        return pd.DataFrame(output, columns=col_names)

    def read_sql_ddl(self, sql_string):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(sql_string)
                self.connection.commit()

    def read_sql_dml(self, sql_string):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(sql_string)
                self.connection.commit()

    def upload_from_file(self, f_path, sql_string):
        with self.connection:
            with self.connection.cursor() as cursor:
                with open(f_path) as f:
                    # cursor.copy_from(f, table_name, columns=column_names, sep=',')
                    cursor.copy_expert(sql_string, f)

                self.connection.commit()
