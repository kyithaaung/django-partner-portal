"""Project package initialization."""

import importlib.util

if importlib.util.find_spec("pymysql"):
    import pymysql

    pymysql.install_as_MySQLdb()
