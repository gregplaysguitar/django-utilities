from django.core.management.base import BaseCommand, CommandError
from django.db import models
from django.core.management import call_command
from django.db import connection, transaction

class Command(BaseCommand):
    def handle(self, *model_labels, **options):
        for label in model_labels:
            m = models.get_model(*label.split('.'))
            temp_name = '_' + m._meta.db_table
            
            try:
                # rename table, then recreate
                cursor = connection.cursor()
                sql = 'ALTER TABLE %s RENAME TO %s' % (m._meta.db_table, temp_name)
                cursor.execute(sql)
                print sql
                call_command('syncdb')
                
                cursor = connection.cursor()
                
                old_fields = [f[0] for f in connection.introspection.get_table_description(cursor, temp_name)]
                new_fields = [f[0] for f in connection.introspection.get_table_description(cursor, m._meta.db_table)]
                
                insert_fields = [f if f in old_fields else '\'\'' for f in new_fields]
                
                # insert data from temp table into new
                sql = 'INSERT INTO %s SELECT %s FROM %s' % (m._meta.db_table, ', '.join(insert_fields), temp_name)
                cursor.execute(sql)
                print sql
                
                # drop temporary table
                sql = 'DROP TABLE %s' % (temp_name)
                cursor.execute(sql)
                print sql
            
            except Exception, e:
                print 'Last SQL statement: ' + sql
                transaction.rollback_unless_managed()
                raise
            else:
                transaction.commit_unless_managed()