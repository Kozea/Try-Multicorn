# -*- coding: utf-8 -*-
"""
Flask application default configuration module

"""

CONFIG = {
    "DB_URL": "pgfdw://multicorn@localhost:5432/multicorn",
    "DB_URL_ADMIN": "pgfdw://multicorn_admin@localhost:5432/multicorn",
    "DB_FDW_SERVER": "multicorn_srv"
}

