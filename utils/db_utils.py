#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2020/5/13 下午3:44
# @Author : Zh
# @Project : zh
# @File   : db_utils.py
# @Software: PyCharm

import pymysql
import logging

from app import settings

logger = logging.getLogger()


class DBReader(object):
    """数据库连接类
    """

    def __init__(self, DB_USER=settings.DB_USER_READER, DB_PASSWD=settings.DB_PASSWD_READER, DB_HOST=settings.DB_HOST,
                 DB_PORT=settings.DB_PORT, DB_CHARSET=settings.DB_CHARSET):
        self._conn = None
        try:
            self.DB_HOST = DB_HOST
            self.DB_PORT = DB_PORT
            self.DB_USER = DB_USER
            self.DB_PASSWD = DB_PASSWD
            self.DB_CHARSET = DB_CHARSET
            self.reconnect()
        except pymysql.Error as e:
            logger.error("Cannot connect to MySQL on %s")

    def reconnect(self):
        self.close()
        self._conn = pymysql.connect(
            host=self.DB_HOST,
            user=self.DB_USER,
            passwd=self.DB_PASSWD,
            port=self.DB_PORT,
            charset=self.DB_CHARSET,
        )
        self._conn.autocommit(True)

    def getConn(self):
        """ 获取数据库连接 """
        if self._conn is None: self.reconnect()
        try:
            self._conn.ping()
        except:
            self.reconnect()

        return self._conn

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

    def close(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def begin(self):
        if self._conn is not None:
            try:
                self.execute("BEGIN")
            except Exception as e:
                logger.error("Can not begin transaction")

    def commit(self):
        if self._conn is not None:
            try:
                self._conn.ping()
            except:
                self.reconnect()
            try:
                self._conn.commit()
            except Exception as e:
                self._conn.rollback()
                logger.exception("Can not commit", e)

    def rollback(self):
        if self._conn is not None:
            try:
                self._conn.rollback()
            except Exception as e:
                logger.error("Can not rollback")

    def execute(self, sql, parameters=None):
        cursor = self._cursor()
        try:
            rowcount = self._execute(cursor, sql, parameters)
            return rowcount
        finally:
            cursor.close()

    def executeAndGetId(self, sql, parameters=None):
        cursor = self._cursor()
        try:
            self._execute(cursor, sql, parameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    def readOne(self, sql, parameters=None):
        cursor = self._cursor()
        try:
            rowcount = self._execute(cursor, sql, parameters)
            if rowcount > 0:
                res = cursor.fetchone()
            else:
                res = None
            return res
        finally:
            cursor.close()

    def readList(self, sql, parameters=None):
        cursor = self._cursor()
        try:
            rowcount = self._execute(cursor, sql, parameters)
            if rowcount > 0:
                res = cursor.fetchall()
            else:
                res = None
            return res
        finally:
            cursor.close()

    def _cursor(self):
        if self._conn is None: self.reconnect()
        try:
            self._conn.ping()
        except:
            self.reconnect()
        return self._conn.cursor()

    def _execute(self, cursor, sql, parameters=None):
        try:
            if parameters is None:
                res = cursor.execute(sql)
            else:
                res = cursor.execute(sql, parameters)
            return res
        except pymysql.Error as e:
            logger.error('Mysql Error:%s\nSQL:%s' % (e, sql))
            self.close()
            raise

    def batch_execute(self, sql_list):
        cursor = self._cursor()
        try:
            for sql in sql_list:
                cursor.execute(sql)
            cursor.close()
            self.commit()
        except Exception as e:
            cursor.close()
            self.rollback()
            raise e


if __name__ == "__main__":
    sql = """
            SELECT
                cu.user_name,
                cu.user_password,
                cu.status user_status,
                cua.attr_id,
                cua.attr_value,
                cua.status attr_status
            FROM
                {radius}.rd_cpe_user cu
                LEFT JOIN {radius}.rd_cpe_user_attrs cua ON cua.user_id = cu.id 
            WHERE
                cu.user_name ="{username}"
                {limit}
            """.format(radius=settings.DB_RADIUS_NAME, username="4241000254", limit="limit 1, 100")

    result = DBReader().readList(sql)
    print(result)

    print(sql)
