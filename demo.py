#!/usr/bin/env python3

USERNAME = 'anlucia'

import os.path
DB_FILE = os.path.expanduser('~') + '/.scites.json'

import requests
from tinydb import TinyDB, Query
from tinydb.operations import set

from datetime import datetime
from dateutil.parser import parse
from dateutil.tz import gettz

import paper2remarkable.ui as p2r

class ScitesDB:
    def __init__(self, username, dbfile):
        self.db = TinyDB(dbfile)
        self.username = username

    def get_scites(self):
        SCITES_URL = 'https://scirate.com/%s/download_scites' % self.username
        r = requests.get(SCITES_URL)
        return r.json()
    
    def update_db(self):
        Scite = Query()
        for s in self.get_scites():
            self.db.upsert(s, Scite['id'] == s['id'])

    def new_scites(self):
        scite = Query()
        return self.db.search(~ scite.rm_uploaded.exists())

    def mark_uploaded(self, doc_id):
        now = datetime.now(gettz())
        Scite = Query()
        self.db.update(set('rm_uploaded',  str(now)), doc_ids=[doc_id])
    
    def mark_all_uploaded(self, cutoff_time = None):
        if cutoff_time is None:
            cutoff_time = datetime.now(gettz())

        older = lambda ts: parse(ts) < cutoff_time
        Scite = Query()
        self.db.update(set('rm_uploaded',  str(cutoff_time)), Scite.created_at.test(older))

    def upload_new(self):
        for s in scitesdb.new_scites():
            print('Uploading %s: %s' % (s['uid'],s['title']))
            p2r.sys.argv=['p2r', '-r', '-p', '/SciRate/', s['abs_url']]
            p2r.main()
            self.mark_uploaded(s.doc_id)


if __name__ == '__main__':
    scitesdb = ScitesDB(USERNAME,DB_FILE)
    if len(scitesdb.db) == 0:
        # this is the first time we run! We won't upload anything
        scitesdb.update_db()
        scitesdb.mark_all_uploaded()
        print('%d old scites recorder. The new ones will be uploaded.' % len(scitedb.db))
    else:
        scitesdb.update_db()
        scitesdb.upload_new()
  


        
        
