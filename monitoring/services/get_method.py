from .cardio_db_conn import pgsql_conn
from monitoring_genomic_mutations.settings import REMOTE_DB_HOST, REMOTE_DB_PORT, REMOTE_DB_NAME, REMOTE_DB_USER, \
    REMOTE_DB_PASSWORD


DB_CONN = pgsql_conn(REMOTE_DB_HOST,
                     REMOTE_DB_PORT,
                     REMOTE_DB_NAME,
                     REMOTE_DB_USER,
                     REMOTE_DB_PASSWORD)

def get_data(search_type, gene):
    query = f"""
        SELECT * 
        FROM crd_dmt.data_vcf 
        WHERE CAST(pos AS TEXT) LIKE '{gene}%'
        LIMIT 1000
    """
    df = DB_CONN.read_sql(query)
    return df.to_dict(orient="records")
