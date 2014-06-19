'''
@author: wrightm
@copyright: 2014 Michael Wright
@license: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
'''

def test_obj_subclass(obj, *clazz):
    if not issubclass(obj.__class__, clazz):
        raise TypeError('object must be of subclass %s not %s' % (clazz, obj.__class__))
    
def test_obj_instance(obj, *clazz):
    if not isinstance(obj, clazz):
        raise TypeError('object must be of instance %s not %s' % (clazz, obj.__class__))