import time
from base64 import b64encode
from datetime import datetime, timedelta
from hashlib import md5
from sqlite3 import connect, Connection, Date, OperationalError
from typing import Union

from ciscoaplookup.spreadsheet_parsing import get_book, platforms, parse_platform_models
from ciscoaplookup.config import Config


def init_db():
    c = _cnx()
    try:
        cur = c.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='file_hashes';""")
        result = cur.fetchone()
        if result is None:
            c.execute("""CREATE TABLE IF NOT EXISTS file_hashes (
                                               file VARCHAR(100) PRIMARY KEY NOT NULL,
                                               hash VARCHAR(200) NOT NULL,
                                               datetime int(4) NOT NULL);""")
            c.execute("""CREATE TABLE IF NOT EXISTS models (
                                                model VARCHAR(15) NOT NULL,
                                                rd VARCHAR(5) NOT NULL,
                                                cn VARCHAR(3) NOT NULL,
                                                PRIMARY KEY (model, rd, cn));
                                                """)
            c.commit()

    finally:
        if c:
            c.close()


def insert_models(models: list[dict[str, str]], prune: bool = False):
    stmt = "INSERT INTO models (model, rd, cn) VALUES (?, ?, ?)"
    row_values = [(row["model"], row["RD"], row["CN"]) for row in models]
    c = _cnx()
    try:
        if prune:
             c.execute("DELETE from models where 1=1;")
        c.executemany(stmt, row_values)
        c.commit()
    finally:
        if c:
            c.close()


def update_file_hash(filename: str, hash: str):
    c = _cnx()
    now = int(time.time())

    try:
        c.execute(f"INSERT INTO file_hashes ('file', 'hash', 'datetime') VALUES(?,?,?)", (filename, hash, now))
        c.commit()
    except Exception as e:
        c.execute(f"UPDATE file_hashes SET hash=?, datetime=? where file = '{filename}';", (hash, now))
        c.commit()
    finally:
        if c:
            c.close()


def get_file_hash(filename: str) -> tuple[str, datetime]:
    c = _cnx()
    try:
        if cur := c.execute(f"SELECT hash, datetime FROM file_hashes where file ='{filename}';"):
            row = next(cur)
            return row[0], row[1]
        raise StopIteration(f"Unable to find hash for {filename}")
    except OperationalError as e:
        raise StopIteration(e.args[0])
    finally:
        if c:
            c.close()


def get_models() -> list[str]:
    c = _cnx()
    try:
        cur = c.execute("""select model, count(*) from models group by model;""")
        return [r[0] for r in cur]
    finally:
        if c:
            c.close()


def get_domain_for(model: str, cn_iso2: str = None) -> list[str]:
    qry = f"SELECT rd, count(cn) FROM (SELECT rd, cn FROM models WHERE model = '{model}')"
    qry += " GROUP BY rd"
    if cn_iso2:
        qry += f",cn having cn = '{cn_iso2}'"
    c = _cnx()
    try:
        cur = c.execute(qry)
        return [r[0] for r in cur]
    finally:
        if c:
            c.close()


def get_models_for(model: str, country: str = None) -> list[str]:
    domains = get_domain_for(model, country)
    if not domains:
        msg = f"Unable to find any valid regulatory domains for {model} in {country}"
        raise ValueError(msg)
    return [f"{model.upper()}{dom}{'-K9' if model.upper().startswith('AIR-') else ''}" for dom in domains]


def get_country_models(model: str) -> list[str]:
    return get_models_for(model)


def _cnx() -> Connection:
    return connect(Config.SQLITE_URI)


def refresh_time_and_hash() -> tuple[datetime, str]:
    hash_ = None
    try:
        hash_, date = get_file_hash(Config.CISCO_XLS_URL)
        if date:
            date = datetime.fromtimestamp(date)
            return date + timedelta(days=Config.REFRESH_DAYS), hash_
    except StopIteration as e:
        pass

    return datetime.now() - timedelta(days=1), hash_  # refresh now


def refresh_required() -> tuple[Union[bool, bytearray], datetime]:
    refresh_date, hash_ = refresh_time_and_hash()
    import requests
    xls_data = requests.get(Config.CISCO_XLS_URL, allow_redirects=True).content
    if hash_ and hash_ == b64encode(md5(xls_data).digest()).decode("utf-8"):
        return False, refresh_date  # no change in file
    return xls_data, refresh_date


def refresh_data(xls_data: bytearray):
    from io import BytesIO
    new_md5 = b64encode(md5(xls_data).digest()).decode("utf-8")
    wb = get_book(BytesIO(xls_data))
    prune = True
    init_db()
    for platform in platforms:
        models = parse_platform_models(wb, platform)
        insert_models(models, prune)
        prune = False
    update_file_hash(Config.CISCO_XLS_URL, new_md5)


__all__ = ["get_models_for",
           "get_country_models",
           "get_domain_for",
           "get_file_hash",
           "update_file_hash",
           "insert_models",
           "init_db",
           "get_models",
           "refresh_time_and_hash",
           "refresh_data",
           "refresh_required"
           ]
