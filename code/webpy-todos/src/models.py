#coding:utf-8
import web

db = web.database(dbn='sqlite', db="todos.db")

class Todos(object):
    @staticmethod
    def get_by_id(id):
        return db.select('todos', where="id=$id", vars=locals())

    @staticmethod
    def get_all():
        return db.select('todos')

    @staticmethod
    def insert(**kwargs):
        db.insert('todos', title=text)

    @staticmethod
    def delete(id):
        db.delete('todos', where="id=$id", vars=locals())
