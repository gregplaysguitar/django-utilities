import logging

class RemovePasswordFilter(logging.Filter):
    '''Remove POSTed passwords from error logs; note this is redundant in Django 1.4+'''
    def filter(self, record):
        
        if record.request.POST:
            post = record.request.POST.copy()
            for key, value in post.iteritems():
                if key.lower().find('password') != -1:
                    post[key] = ''.join(['*' for i in range(0, len(value))])
            
            record.request.POST = post
            
        #import pdb;pdb.set_trace()
        #print record
        
        
        return True
