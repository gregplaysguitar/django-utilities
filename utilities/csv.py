import csv, os
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError


def getval(obj, getter):
    """Gets a value from an object, using a getter which 
       can be a callable, an attribute, or a dot-separated
       list of attributes"""
    if callable(getter):
        val = getter(obj)
    else:
        val = obj
        for attr in getter.split('.'):
            val = getattr(val, attr)
            if callable(val):
                val = val()
    if val == True:
        val = 'yes'
    elif val == False:
        val = ''
    return (unicode(val or '')).encode('utf-8')


class CSVExportCommand(BaseCommand):
    '''A generic command to create a csv export. Extend this class and add the 
       following:
       
       - A `get_queryset` method, which takes an options argument and returns 
         the queryset to process.
       - A `self.FIELDS` tuple, which should consist of `(name, getter)` pairs,
         where `getter` is a callable, an attribute, or a dot-separated set of
         attributes.
       
    '''
    
    args = 'Destination filename'
    can_import_settings = True

    option_list = BaseCommand.option_list + (
        make_option(
            '--overwrite',
            action='store_true',
            dest='overwrite',
            default=False,
            help='Overwrite existing file'
        ),
    )
    
    def get_queryset(self, options):
        raise NotImplementedError
    
    def handle(self, destination, *args, **options):
        if os.path.exists(destination) and not options['overwrite']:
            raise CommandError('Destination file already exists')
        else:
            file = open(destination, 'w')
            csvfile = csv.writer(file)

            qs = self.get_queryset(options)

            if not len(qs):
                raise CommandError('No objects found')                
            else:
                csvfile.writerow([f[0] for f in self.FIELDS])

                for obj in qs:
                    row = []
                    for name, getter in self.FIELDS:                       
                        row.append(getval(obj, getter))

                    csvfile.writerow(row)

                file.close()






