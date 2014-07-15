import collections
import types
import sys
import math
import numbers

from python_toolbox import misc_tools
from python_toolbox import binary_search
from python_toolbox import dict_tools
from python_toolbox import nifty_collections
from python_toolbox import caching

from layout_rabbit import shy_math_tools
from layout_rabbit import shy_sequence_tools
from layout_rabbit import shy_cute_iter_tools
from layout_rabbit import shy_nifty_collections
from layout_rabbit import shy_misc_tools

from . import misc

infinity = float('inf')


        
class MapSpace(shy_sequence_tools.CuteSequenceMixin, collections.Sequence):
    def __init__(self, function, sequence):
        
        self.function = function
        self.sequence = shy_sequence_tools. \
                                         ensure_iterable_is_immutable_sequence(
            sequence,
            default_type=nifty_collections.LazyTuple
        )
    
    
    length = caching.CachedProperty(
        lambda self: shy_sequence_tools.get_length(self.sequence)
    )
        
    def __repr__(self):
        return '%s(%s, %s)' % (
            type(self).__name__,
            self.function,
            self.sequence
        )
        
    def __getitem__(self, i):
        if isinstance(i, slice):
            return type(self)(self.function, self.sequence[i])
        assert isinstance(i, int)
        return self.function(self.sequence[i]) # Propagating `IndexError`.
        
    
    def __iter__(self):
        for item in self.sequence:
            yield self.function(item)
        
    _reduced = property(
        lambda self: (type(self), self.function, self.sequence)
    )
             
    __eq__ = lambda self, other: (isinstance(other, MapSpace) and
                                  self._reduced == other._reduced)
    
    __bool__ = lambda self: bool(self.sequence)
        

