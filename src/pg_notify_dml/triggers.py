import logging
from typing import Dict

import sqlalchemy

TRIGGER = """
CREATE TRIGGER {table}_notify_event
AFTER INSERT OR UPDATE OR DELETE ON {table}
    FOR EACH ROW EXECUTE PROCEDURE notify_event();
"""



def get_tables(meta: sqlalchemy.MetaData) -> Dict[str, str]:
    for name, table in meta.tables.items():
        sql = TRIGGER.format(table=name)
        logging.debug("SQL for %s: %s", table, sql)

# def ensure_event_function(engine: sqlalchemy.Engine):
#     """Ensures the event function is present in the engine"""
#     ...
