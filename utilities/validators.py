import csv, re

from django.core.exceptions import ValidationError



class CSVValidator(object):
    
    def __init__(self, num_columns=None):
        self.num_columns = num_columns

    def __call__(self, value):
        """Validates that the input file is a csv, and has the correct 
           number of rows and columns if specified."""
        
        if str(value)[-4:].lower() != '.csv':
            raise ValidationError('That is not a csv file.')
        else:
            sample = value.read(1024)
            value.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample)
            except csv.Error:
                raise ValidationError('That file could not be parsed as CSV.')
            else:
                if self.num_columns:
                    file = csv.reader(value, dialect=dialect)
                    value.seek(0)
                    for row in file:
                        columns = len(row)
                        break
                    
                    if columns != self.num_columns:
                        raise ValidationError('Incorrect number of columns - %s columns required.' % self.num_columns)



COORDS_RE = re.compile('^\s*\-?\d+\.\d+\s*,\s*-?\d+\.\d+\s*$')
def map_coords(value):
    if not COORDS_RE.match(value):
        raise ValidationError(u'Example format: -43.526954, 172.63508')

