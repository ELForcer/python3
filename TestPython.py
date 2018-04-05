import sqlite3
import uuid
import datetime
import time
import pymssql #работа с MS SQL
from flask import request


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def gen_dict(cur):
    names = [x[0].upper() for x in cur.description]
    for row in cur:
        yield dict(zip(names, row))
       
