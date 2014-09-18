# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.combi import *


def test_perms():
    pure_0a = PermSpace(4)
    pure_0b = PermSpace(range(4))
    pure_0c = PermSpace(list(range(4)))
    pure_0d = PermSpace(iter(range(4)))
    assert pure_0a == pure_0b == pure_0c == pure_0d
    assert len(pure_0a) == len(pure_0b) == len(pure_0c) == len(pure_0d)
    assert repr(pure_0a) == repr(pure_0b) == repr(pure_0c) == \
                         repr(pure_0d) == '<PermSpace: range(0, 4)>'
    
    assert cute_iter_tools.are_equal(pure_0a, pure_0b, pure_0c, pure_0d)
    
    assert set(map(bool, (pure_0a, pure_0b, pure_0c, pure_0d))) == {True}
    
    pure_perm_space = pure_0a
    assert pure_0a.is_pure
    assert not pure_0a.is_rapplied
    assert not pure_0a.is_dapplied
    assert not pure_0a.is_fixed
    assert not pure_0a.is_sliced
    
    first_perm = pure_0a[0]
    some_perm = pure_0a[7]
    last_perm = pure_0a[-1]
    
    assert type(first_perm) == type(some_perm) == type(last_perm) == Perm
    assert set(some_perm) == set(range(4))
    assert tuple(first_perm) == (0, 1, 2, 3)
    assert tuple(last_perm) == (3, 2, 1, 0)
    
    assert some_perm.inverse == ~ some_perm
    assert ~ ~ some_perm == some_perm
    
    assert int(first_perm) == 0
    assert int(last_perm) == len(pure_perm_space) - 1
    
    assert first_perm in pure_perm_space
    assert set(first_perm) not in pure_perm_space # No order? Not contained.
    assert some_perm in pure_perm_space
    assert last_perm in pure_perm_space
    assert tuple(first_perm) in pure_perm_space
    assert list(some_perm) in pure_perm_space
    assert iter(last_perm) in pure_perm_space
    assert 'meow' not in pure_perm_space
    assert (0, 1, 2, 3, 3) not in pure_perm_space
    
    assert pure_perm_space.index(first_perm) == 0
    assert pure_perm_space.index(last_perm) == \
                                                len(pure_perm_space) - 1
    assert pure_perm_space.index(some_perm) == 7
    
    assert Perm(7, pure_perm_space) ==  Perm(7, range(4)) == Perm(7, 4) == \
                                                                    some_perm
    
    assert Perm((1, 3, 2, 0)) * 'meow' == 'ewom'
    assert Perm((1, 3, 2, 0)) * Perm('meow', 'meow') == Perm('ewom', 'meow')
    assert Perm((0, 1, 2, 3)) * [0, 1, 2, 3] == (0, 1, 2, 3)
    assert Perm((0, 1, 2, 3)) * Perm((0, 1, 2, 3)) == Perm((0, 1, 2, 3))
    assert Perm((0, 1, 3, 2)) * Perm((2, 0, 1, 3)) == Perm((2, 0, 3, 1))
    
    assert (Perm((0, 1, 2, 3)) ** (- 2)) == (Perm((0, 1, 2, 3)) ** (- 1)) == \
           (Perm((0, 1, 2, 3)) ** (0)) == (Perm((0, 1, 2, 3)) ** (1)) == \
           (Perm((0, 1, 2, 3)) ** 2) == (Perm((0, 1, 2, 3)) ** 3)
    
    assert Perm('woem', 'meow') ** (-1) == Perm('woem', 'meow')
    assert Perm('mowe', 'meow') ** (-1) == Perm('mweo', 'meow')
    
    assert set(map(bool, (pure_0a[4:4], pure_0a[3:2]))) == {False}
    assert pure_0a[2:6][1:-1] == pure_0a[3:5]
    assert tuple(pure_0a[2:6][1:-1]) == tuple(pure_0a[3:5])
    assert pure_0a[2:6][1:-1][1] == pure_0a[3:5][1]
    assert pure_0a[2:5][1:-1] != pure_0a[3:5]
    
    big_perm_space = PermSpace(range(150), fixed_map={1: 5, 70: 3,},
                               degrees=(3, 5))
    
    for i in [10**10, 3*11**9-344, 4*12**8-5, 5*3**20+4]:
        perm = big_perm_space[i]
        perm.number # Just ensuring no exception
        assert big_perm_space.index(perm) == i
    
def test_fixed_perm_space():
    pure_perm_space = PermSpace(5)
    small_fixed_perm_space = PermSpace(5, fixed_map={0: 0, 2: 2, 4: 4,})
    big_fixed_perm_space = PermSpace(5, fixed_map={0: 0, 2: 2,})
    
    assert pure_perm_space != big_fixed_perm_space != small_fixed_perm_space
    assert small_fixed_perm_space.length == \
                                        len(tuple(small_fixed_perm_space)) == 2
    assert big_fixed_perm_space.length == \
                                          len(tuple(big_fixed_perm_space)) == 6
    
    for perm in small_fixed_perm_space:
        assert perm in big_fixed_perm_space
        assert perm in pure_perm_space
        
    for perm in big_fixed_perm_space:
        assert perm in pure_perm_space
        
    assert len([perm for perm in big_fixed_perm_space if perm
                not in small_fixed_perm_space]) == 4
    
    assert small_fixed_perm_space[:] == small_fixed_perm_space
    assert small_fixed_perm_space[1:][0] == small_fixed_perm_space[1]
    
    assert small_fixed_perm_space.index(small_fixed_perm_space[0]) == 0
    assert small_fixed_perm_space.index(small_fixed_perm_space[1]) == 1
    
    assert big_fixed_perm_space.index(big_fixed_perm_space[0]) == 0
    assert big_fixed_perm_space.index(big_fixed_perm_space[1]) == 1
    assert big_fixed_perm_space.index(big_fixed_perm_space[2]) == 2
    assert big_fixed_perm_space.index(big_fixed_perm_space[3]) == 3
    assert big_fixed_perm_space.index(big_fixed_perm_space[4]) == 4
    assert big_fixed_perm_space.index(big_fixed_perm_space[5]) == 5
    
    for perm in small_fixed_perm_space:
        assert (perm[0], perm[2], perm[4]) == (0, 2, 4)
    
    for perm in big_fixed_perm_space:
        assert (perm[0], perm[2]) == (0, 2)
    
    assert big_fixed_perm_space.index(small_fixed_perm_space[1]) != 1
    
    
def test_rapplied_perm_space():
    rapplied_perm_space = PermSpace('meow')
    assert rapplied_perm_space.is_rapplied
    assert not rapplied_perm_space.is_fixed
    assert not rapplied_perm_space.is_sliced
    
    assert 'mowe' in rapplied_perm_space
    assert 'woof' not in rapplied_perm_space
    assert rapplied_perm_space[rapplied_perm_space.index('wome')] == \
                                              Perm('wome', rapplied_perm_space)
    
    rapplied_perm = rapplied_perm_space[3]
    assert isinstance(reversed(rapplied_perm), Perm)
    assert tuple(reversed(rapplied_perm)) == \
                                          tuple(reversed(tuple(rapplied_perm)))
    assert reversed(reversed(rapplied_perm)) == rapplied_perm
    
def test_dapplied_perm_space():
    dapplied_perm_space = PermSpace(5, domain='growl')
    assert dapplied_perm_space.is_dapplied
    assert not dapplied_perm_space.is_rapplied
    assert not dapplied_perm_space.is_fixed
    assert not dapplied_perm_space.is_sliced
    
    assert (0, 4, 2, 3, 1) in dapplied_perm_space
    assert (0, 4, 'ooga booga', 2, 3, 1) not in dapplied_perm_space
    
    dapplied_perm = dapplied_perm_space[-1]
    assert dapplied_perm in dapplied_perm_space
    assert isinstance(reversed(dapplied_perm), Perm)
    assert reversed(dapplied_perm) in dapplied_perm_space
    assert tuple(reversed(dapplied_perm)) == \
                                          tuple(reversed(tuple(dapplied_perm)))
    assert reversed(reversed(dapplied_perm)) == dapplied_perm
    
    assert dapplied_perm['l'] == 0
    assert dapplied_perm['w'] == 1
    assert dapplied_perm['o'] == 2
    assert dapplied_perm['r'] == 3
    assert dapplied_perm['g'] == 4
    
    # `__contains__` works on the values, not the keys:
    for char in 'growl':
        assert char not in dapplied_perm
    for number in range(5):
        assert number in dapplied_perm
    
def test_degreed_perm_space():
    assert PermSpace(3, degrees=0).length == 1
    assert PermSpace(3, degrees=1).length == 3
    assert PermSpace(3, degrees=2).length == 2
    
    for perm in PermSpace(3, degrees=1):
        assert perm.degree == 1
        
        
    for perm in PermSpace(5, degrees=(1, 3)):
        assert perm.degree in (1, 3)
        
    assert cute_iter_tools.is_sorted(
        [perm.number for perm in PermSpace(5, degrees=(1, 3))]
    )
    
    assert PermSpace(
        7, 'travels',
        fixed_map={'l': 5, 'a': 2, 't': 0, 'v': 3, 'r': 1, 'e': 6},
        degrees=(1, 3, 5)
    ).length == 1
    
    assert PermSpace(4, degrees=1, fixed_map={0: 0, 1: 1, 2: 2,}).length == 0
    assert PermSpace(4, degrees=1, fixed_map={0: 0, 1: 1}).length == 1
    assert PermSpace(4, degrees=1, fixed_map={0: 0, }).length == 3
    assert PermSpace(4, degrees=1, fixed_map={0: 1, 1: 0,}).length == 1
    assert PermSpace(4, degrees=1, fixed_map={0: 1, 1: 2,}).length == 0
    assert PermSpace(4, degrees=2, fixed_map={0: 1, 1: 2,}).length == 1
    assert PermSpace(4, degrees=3, fixed_map={0: 1, 1: 2,}).length == 1
    
    assert PermSpace(4, degrees=3, fixed_map={2: 3,}).length == 2
    assert PermSpace(4, degrees=1, fixed_map={2: 3,}).length == 1
    
    funky_perm_space = PermSpace('isogram', domain='travels',
                                 degrees=(1, 3, 5, 9),
                                 fixed_map={'t': 'i', 'v': 'g',})[2:-2]
    
    assert funky_perm_space.is_rapplied
    assert funky_perm_space.is_dapplied
    assert funky_perm_space.is_degreed
    assert funky_perm_space.is_fixed
    assert funky_perm_space.is_sliced
    assert not funky_perm_space.is_pure
    
    assert funky_perm_space.degrees == (1, 3, 5)
    assert funky_perm_space.sequence == 'isogram'
    assert funky_perm_space.domain == 'travels'
    assert funky_perm_space.canonical_slice.start == 2
    
    for i, perm in enumerate(funky_perm_space):
        assert perm.is_dapplied
        assert perm.is_rapplied
        assert perm['t'] == 'i'
        assert perm['v'] == 'g'
        assert perm['s'] in 'isogram'
        assert 1 not in perm
        assert perm.degree in (1, 3, 5, 9)
        assert funky_perm_space.index(perm) == i
        assert perm.undapplied[0] == 'i'
        assert perm.unrapplied['t'] == 0
        assert perm.unrapplied.undapplied[0] == 0
        assert perm.undapplied.is_rapplied
        assert perm.unrapplied.is_dapplied
        
    assert cute_iter_tools.is_sorted(
        [perm.number for perm in funky_perm_space]
    )
    
    assert cute_iter_tools.is_sorted(funky_perm_space)
    
    
    other_perms_chain_space = ChainSpace((funky_perm_space.unsliced[:2],
                                          funky_perm_space.unsliced[-2:]))
    for perm in other_perms_chain_space:
        assert perm.is_dapplied
        assert perm.is_rapplied
        assert perm['t'] == 'i'
        assert perm['v'] == 'g'
        assert perm['s'] in 'isogram'
        assert 1 not in perm
        assert perm.degree in (1, 3, 5, 9)
        assert perm not in funky_perm_space
        assert perm.unrapplied['t'] == 0
        assert perm.unrapplied.undapplied[0] == 0        
        assert perm.undapplied.is_rapplied
        assert perm.unrapplied.is_dapplied
        
    assert other_perms_chain_space.length + funky_perm_space.length == \
                                               funky_perm_space.unsliced.length
    
    assert cute_iter_tools.is_sorted(
        [perm.number for perm in other_perms_chain_space]
    )
    
    
    assert funky_perm_space.unsliced.length + \
           funky_perm_space.unsliced.undegreed.get_degreed(
               i for i in range(funky_perm_space.sequence_length)
               if i not in funky_perm_space.degrees
            ).length == funky_perm_space.unsliced.undegreed.length
    
    
def test_partial_perm_space():
    with cute_testing.RaiseAssertor():
        PermSpace(5, n_elements=6)
        
    perm_space_0 = PermSpace(5, n_elements=5)
    perm_space_1 = PermSpace(5, n_elements=3)
    perm_space_2 = PermSpace(5, n_elements=2)
    perm_space_3 = PermSpace(5, n_elements=1)
    perm_space_4 = PermSpace(5, n_elements=0)
        
    perm_space_5 = PermSpace(5, n_elements=5, is_combination=True)
    perm_space_6 = PermSpace(5, n_elements=3, is_combination=True)
    perm_space_7 = PermSpace(5, n_elements=2, is_combination=True)
    perm_space_8 = PermSpace(5, n_elements=1, is_combination=True)
    perm_space_9 = PermSpace(5, n_elements=0, is_combination=True)
    
    assert not perm_space_0.is_partial and not perm_space_0.is_combination
    assert perm_space_1.is_partial and not perm_space_1.is_combination
    assert perm_space_2.is_partial and not perm_space_2.is_combination
    assert perm_space_3.is_partial and not perm_space_3.is_combination
    assert perm_space_4.is_partial and not perm_space_4.is_combination
    assert set(map(type, (perm_space_0, perm_space_1, perm_space_2,
                          perm_space_3, perm_space_4))) == {PermSpace}
    
    assert not perm_space_5.is_partial and perm_space_5.is_combination
    assert perm_space_6.is_partial and perm_space_6.is_combination
    assert perm_space_7.is_partial and perm_space_7.is_combination
    assert perm_space_8.is_partial and perm_space_8.is_combination
    assert perm_space_9.is_partial and perm_space_9.is_combination
    assert set(map(type, (perm_space_5, perm_space_6, perm_space_7,
                          perm_space_8, perm_space_9))) == {CombSpace}
    
    assert CombSpace(5, n_elements=2) == perm_space_7
    
    assert perm_space_0.length == math.factorial(5)
    assert perm_space_1.length == 5 * 4 * 3
    assert perm_space_2.length == 5 * 4
    assert perm_space_3.length == 5
    assert perm_space_4.length == 1
    
    assert perm_space_5.length == 1
    assert perm_space_6.length == perm_space_7.length == 5 * 4 / 2
    assert perm_space_8.length == 5
    assert perm_space_9.length == 1
    
    assert set(map(tuple, perm_space_1)) > set(map(tuple, perm_space_6))
    
    for i, perm in enumerate(perm_space_2):
        assert len(perm) == 2
        assert not perm.is_dapplied
        assert not perm.is_rapplied
        assert not isinstance(perm, Comb)
        assert perm_space_2.index(perm) == i
        reconstructed_perm = Perm(tuple(perm), perm_space=perm_space_2)
        assert perm == reconstructed_perm
        assert perm.number == reconstructed_perm.number == i
        
    
    for i, perm in enumerate(perm_space_7):
        assert len(perm) == 2
        assert not perm.is_dapplied
        assert not perm.is_rapplied
        assert isinstance(perm, Comb)
        assert perm_space_7.index(perm) == i
        assert perm[0] < perm[1]
        reconstructed_perm = Perm(tuple(perm), perm_space=perm_space_7)
        assert perm == reconstructed_perm
        assert perm.number == reconstructed_perm.number == i
        
    assert cute_iter_tools.is_sorted(
        [perm.number for perm in perm_space_2]
    )
    assert cute_iter_tools.is_sorted(
        [tuple(perm) for perm in perm_space_2]
    )
    assert cute_iter_tools.is_sorted(
        [perm.number for perm in perm_space_7]
    )
    assert cute_iter_tools.is_sorted(
        [tuple(perm) for perm in perm_space_7]
    )
    
    
def test_neighbors():
    perm = Perm('wome', 'meow')
    first_level_neighbors = perm.get_neighbors()
    assert Perm('woem', 'meow') in first_level_neighbors
    assert Perm('meow', 'meow') not in first_level_neighbors
    assert len(first_level_neighbors) == 6
    assert isinstance(first_level_neighbors[0], Perm)
    
    
    
    first_and_second_level_neighbors = perm.get_neighbors((1, 2))
    assert Perm('woem', 'meow') in first_and_second_level_neighbors
    assert Perm('meow', 'meow') not in first_and_second_level_neighbors
    assert Perm('owem', 'meow') in first_and_second_level_neighbors
    assert isinstance(first_and_second_level_neighbors[-1], Perm)
    
    
    assert set(first_level_neighbors) < set(first_and_second_level_neighbors)
    
    assert perm in perm.get_neighbors((0, 1))
    assert set(first_level_neighbors) < set(perm.get_neighbors((0, 1)))
    assert len(first_level_neighbors) + 1 == len(perm.get_neighbors((0, 1)))
    
    

def test_super_structure():
    
    