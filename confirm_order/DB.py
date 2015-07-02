#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tinyproxy(tinyproxy@gmail.com)'

import threading
from pymongo import MongoClient

debug_client = None
kky_client = None

debug_url = "mongodb://localhost/admin"
kky_url = "mongodb://sa:kuaikuaiyu1219@kuaikuaiyu.com/admin"


client_lock = threading.Lock()

def getDebugClient():
    global debug_client
    if debug_client is None:
        client_lock.acquire()
        if debug_client is None:
            debug_client = MongoClient(host=debug_url)
        client_lock.release()
    return debug_client

def getKKYClient():
    global kky_client
    if kky_client is None:
        client_lock.acquire()
        if kky_client is None:
            kky_client = MongoClient(host=kky_url)
        client_lock.release()
    return kky_client