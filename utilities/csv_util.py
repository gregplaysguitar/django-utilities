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


def export_csv(output, qs, fields):
    '''Creates a csv export from a queryset.
       
       output - a file-like output object 
       qs - queryset or compatible iterable to export
       fields - iterable of `(name, getter)` pairs, where `getter` is a 
                callable, an attibute, or a dot-separated set of attributes.
    '''
    
    csvfile = csv.writer(output)
    
    # header row
    csvfile.writerow([f[0] for f in fields])
    
    # data rows
    for obj in qs:
        row = []
        for name, getter in fields:                       
            row.append(getval(obj, getter))

        csvfile.writerow(row)


class CSVExportCommand(BaseCommand):
    '''A generic command to create a csv export. Extend this class and add the 
       following:
       
       - A `get_queryset` method, which takes an options argument and returns 
         the queryset to process.
       - A `self.FIELDS` tuple, which should consist of `(name, getter)` pairs,
         where `getter` is a callable, an att
ibute, or a dot-separated set of
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
        fields = getattr(self, 'FIELDS', None)
        if not fields:
            raise NotImplementedError('`FIELDS` is not defined')
        
        if os.path.exists(destination) and not options['overwrite']:
            raise CommandError('Destination file already exists')
        
        qs = self.get_queryset(options)
        if not len(qs):
            raise CommandError('No objects found')
        
        
        output_file = open(destination, 'w')
        export_csv(output_file, qs, fields)
        output_file.close()


