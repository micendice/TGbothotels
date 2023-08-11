import peewee as pw

from datetime import datetime


db = pw.SqliteDatabase('querylog2.db')


class ModelBase(pw.Model):
    created_at = pw.DateField(default=datetime.now())

    class Meta():
        database = db


class History(ModelBase):
    user_id = pw.TextField()
    command = pw.TextField()
    pl_sort = pw.TextField()

    city = pw.TextField()
    hotels_num = pw.IntegerField()
    num_photo = pw.TextField()
    adults_num = pw.TextField()
    kids_num = pw.TextField()
    check_in_date = pw.DateField()
    check_out_date = pw.DateField()

    full_result = pw.TextField()
    result_descr = pw.TextField()

