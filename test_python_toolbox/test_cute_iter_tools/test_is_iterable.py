# Copyright 2009-2012 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `python_toolbox.cute_iter_tools.is_iterable`.'''

import nose.tools

from python_toolbox.infinity import infinity
from python_toolbox import cute_iter_tools
from python_toolbox.cute_iter_tools import is_iterable


def test():
    '''Test basic workings of `is_iterable`.'''
    
    iterables = [
        [1, 2, 3],
        (1, 2),
        {},
        (),
        [[1]],
        'asdfasdf',
        ''
    ]
    
    non_iterables = [
        dict,
        list,
        type,
        None,
        True,
        False,
        Exception,
        lambda x: x
    ]
    
    for iterable in iterables:
        assert is_iterable(iterable)
        
    for non_iterable in non_iterables:
        assert not is_iterable(non_iterable)