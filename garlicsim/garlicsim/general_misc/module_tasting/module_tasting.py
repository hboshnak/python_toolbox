# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

# blocktodo: Will need thread safety for when another thread is importing at
# the same time. probably make context manager for import lock from imp.

from __future__ import with_statement

import imp
import uuid
import sys
import os.path
import encodings.mbcs as _, encodings.utf_8 as _

from garlicsim.general_misc.third_party import mock as mock_module

from garlicsim.general_misc.temp_value_setters import TempImportHookSetter
from garlicsim.general_misc import import_tools


def mock_import(*args, **kwargs):
    return mock_module.Mock(name=repr((args, kwargs)))

def taste_module(path_or_address):
    
    # blocktodo: implement address    
    path = path_or_address
    os.path.isfile(path)
    
    old_sys_modules = sys.modules.copy() # blocktodo: Make context manager for this
    
    name = 'tasted_module_%s' % uuid.uuid4()
    
    with TempImportHookSetter(mock_import):
        
        # Note that `import_by_path` is not affected by the import hook:
        tasted_module = import_tools.import_by_path(path,
                                                    name=name,
                                                    keep_in_sys_modules=False)
        
    assert old_sys_modules == sys.modules
    
    return tasted_module
        