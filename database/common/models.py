from datetime import datetime

import peewee as pw

db = pw.SqliteDatabase('querylog13.db')


class ModelBase(pw.Model):
    created_at = pw.DateField(default=datetime.now())

    class Meta():
        database = db


class History(ModelBase):
    command = pw.TextField()
    sorting_by = pw.TextField
    city = pw.TextField()
    hotels_num = pw.TextField()
    num_photo = pw.TextField()
    check_in_date = pw.DateField()
    check_out_date = pw.DateField()

    full_result = pw.TextField()
    result_descr = pw.TextField()




    #username = pw.TextField()