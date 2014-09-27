# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import pickle
import itertools
import collections

import nose

from python_toolbox import context_management
from python_toolbox import sequence_tools

from python_toolbox import combi
from python_toolbox.combi import *

infinity = float('inf')
infinities = (infinity, -infinity)


def _check_variation_selection(variation_selection):
    assert isinstance(variation_selection, combi.variations.VariationSelection)
    
    kwargs = {}
    
    if variation_selection.is_recurrent:
        #blocktodo obviously remove when done with recurrent
        raise nose.SkipTest


    if variation_selection.is_recurrent and \
                                           not variation_selection.is_rapplied:
        assert not variation_selection.is_allowed
        # Can't even test this illogical clash.
        return 
        
    
    iterable_or_length = (
        'abracab' if variation_selection.is_recurrent else
        tuple(range(60, -10, -10)) if variation_selection.is_rapplied else 7
    )
    kwargs['iterable_or_length'] = iterable_or_length
    sequence = (iterable_or_length if
                isinstance(iterable_or_length, collections.Iterable) else
                sequence_tools.CuteRange(iterable_or_length))
    sequence_set = set(sequence)
    
    if variation_selection.is_dapplied:
        domain = 'isogram'
        kwargs['domain'] = domain
    else:
        domain = sequence_tools.CuteRange(11)
    domain_set = set(domain)
        
    if variation_selection.is_partial:
        kwargs['n_elements'] = 5
        
    if variation_selection.is_combination:
        kwargs['is_combination'] = True
        
    if variation_selection.is_fixed:
        fixed_map = {domain[1]: sequence[1], domain[4]: sequence[3],}
        kwargs['fixed_map'] = fixed_map
    else:
        fixed_map = {}
        
    if variation_selection.is_degreed:
        kwargs['degrees'] = (0, 2, 4, 5)
        

    context_manager = (
        context_management.BlankContextManager() if
        variation_selection.is_allowed else
        cute_testing.RaiseAssertor(combi.UnallowedVariationSelectionException)
    )
    
    with context_manager:
        perm_space = PermSpace(**kwargs)
        if variation_selection.is_sliced:
            if perm_space.length >= 2:
                perm_space = perm_space[2:-2]
            else:
                assert variation_selection.is_combination and \
                                             not variation_selection.is_partial
                perm_space = perm_space[:0]
    
    if not variation_selection.is_allowed:
        return
    
    assert perm_space.variation_selection == variation_selection
    assert perm_space.sequence_length == 7
    for i, perm in enumerate(itertools.islice(perm_space, 100)):
        assert isinstance(perm, combi.PermSpace)
        assert type(perm) == combi.Comb if variation_selection.is_combination \
                                                                else combi.Perm
        if not variation_selection.is_fixed and \
                                            not variation_selection.is_degreed:
            assert perm_space.index(perm) == i
        assert set(perm) == set(sequence)
        for j, ((key, value), key_, (key__, value__)) in enumerate(
                                       zip(perm, perm.as_dictoid, perm.items)):
            assert key == key_ == key__
            assert value == perm.as_dictoid[key] == value__
            assert perm.items[j] == (key, value)
        assert perm.is_rapplied == variation_selection.is_rapplied
        if perm.is_rapplied:
            assert perm.unrapplied == perm_space.unrapplied[i]
        else:
            assert perm.get_rapplied('isogram')
            
            
            
    pass # blocktodo add more
    
    
def test():
    yield from ((_check_variation_selection, variation_selection) for
                variation_selection in combi.variations.variation_selection_space)
    