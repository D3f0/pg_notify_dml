import sqlalchemy
import logging


TRIGGER = """
CREATE TRIGGER {table}_notify_event
AFTER INSERT OR UPDATE OR DELETE ON {table}
    FOR EACH ROW EXECUTE PROCEDURE notify_event();
"""

def get_tables(meta: sqlalchemy.MetaData):
    for name, table in meta.tables.items():
        sql = TRIGGER.format(table=name)
        logging.debug("SQL for %s: %s", table, sql)