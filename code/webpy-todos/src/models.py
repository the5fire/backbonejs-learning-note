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
    def create(**kwargs):
        db.insert('todos', **kwargs)

    @staticmethod
    def update(**kwargs):
        db.update('todos', where="id=$id", vars={"id": kwargs.pop('id')}, **kwargs)

    @staticmethod
    def delete(id):
        db.delete('todos', where="id=$id", vars=locals())
