# !user/bin/env python3
# -*- coding: utf-8 -*-
# Author: Artorias
import pickle
import psycopg2

from odoo.http import request
from ..base_session_store_psql.sessionstore import PostgresSessionStore


def metro_save(self, session):
    uid = session.uid or None
    with self.get_cursor() as cr:
        sql_data = {
            'data': psycopg2.Binary(pickle.dumps(dict(session),
                                                 pickle.HIGHEST_PROTOCOL)),
            'id': session.sid,
            'uid': uid,
        }

        if self.is_valid_key(session.sid):
            cr.execute(
                """
                UPDATE sessionstore SET data = %(data)s, uid=%(uid)s WHERE id = %(id)s;
                """, sql_data)
        else:
            cr.execute(
                """
                INSERT INTO sessionstore (id, data, uid)
                VALUES (%(id)s, %(data)s, %(uid)s);
                """, sql_data)
            # request.env['res.users'].trigger_up_to_sso_login(uid)
        # uid不为None的情况删除其他相同uid的session
        if uid is not None:
            cr.execute(
                """
                DELETE FROM sessionstore WHERE uid=%(uid)s AND id != %(id)s
                """, sql_data)

# PostgresSessionStore.save = metro_save