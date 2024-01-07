import project as pj

import pytest
import random

def test_get_int_percentage():

    # Check numbers 0 through 100
    for i in range(0, 101):
        assert(pj.get_int_percentage(i, 100) == i)
    
    # Check fractions/decimals
    assert(pj.get_int_percentage(2, 3) == 67)
    assert(pj.get_int_percentage(1, 3) == 33)
    assert(pj.get_int_percentage(3, 3) == 100)

    # Check over and under
    assert(pj.get_int_percentage(5, 3) == 100)
    assert(pj.get_int_percentage(-5, 3) == 0)

    # Check div by 0
    assert(pj.get_int_percentage(-5, 0) == 0)
    assert(pj.get_int_percentage(0, 0) == 0)
    assert(pj.get_int_percentage(1, 0) == 100)

    # Check negatie total
    with pytest.raises(ValueError):
        pj.get_int_percentage(1, -1)

def test_is_point_in_square():

    # Normal cases

    square = [0, 0, 2, 6]

    # Test random points within square
    for i in range(100000):
        point = (random.randrange(-square[2]/2, 1 + square[2]/2),
                 random.randrange(-square[3]/2, 1 + square[3]/2))

        assert(pj.is_point_in_square(point, square) == True)
    
    # Test border / corners
    assert(pj.is_point_in_square([1, 0], square) == True)
    assert(pj.is_point_in_square([square[2]/2, -square[3]/2], square) == True)
    assert(pj.is_point_in_square([square[2]/2, square[3]/2], square) == True)
    assert(pj.is_point_in_square([-square[2]/2, -square[3]/2], square) == True)
    assert(pj.is_point_in_square([-square[2]/2, square[3]/2], square) == True)

    # Test exterior points
    assert(pj.is_point_in_square([square[2]/2 + 0.1, 
                                  square[2]/2], square) == False)
    assert(pj.is_point_in_square([square[2]/2 - 0.1, 
                                  square[3]/2 + 0.1], square) == False)

    # point to point case
    assert(pj.is_point_in_square([0, 0], [0, 0, 0, 0]) == True)
    assert(pj.is_point_in_square([0, 0], [1, 1, 0, 0]) == False)

def test_is_square_touching_square():

    s1 = [0, 0, 2, 6]
    s2 = [1, 0, 2, 6]
    s3 = [2, 0, 2, 6]
    s4 = [2.1, 0, 2, 6]

    # Identical
    assert(pj.is_square_touching_square(s1, s1) == True)

    # Overlapping
    assert(pj.is_square_touching_square(s1, s2) == True)
    assert(pj.is_square_touching_square(s2, s1) == True)

    # Edge touching
    assert(pj.is_square_touching_square(s1, s3) == True)
    assert(pj.is_square_touching_square(s3, s1) == True)

    # Not touching
    assert(pj.is_square_touching_square(s1, s4) == False)
    assert(pj.is_square_touching_square(s4, s1) == False)
    

    s1 = [0, 0, 2, 6]
    s2 = [0, 2, 2, 6]
    s3 = [0, 6, 2, 6]
    s4 = [0, 8, 2, 6]

    # Identical
    assert(pj.is_square_touching_square(s1, s1) == True)

    # Overlapping
    assert(pj.is_square_touching_square(s1, s2) == True)

    # Edge touching
    assert(pj.is_square_touching_square(s1, s3) == True)

    # Not touching
    assert(pj.is_square_touching_square(s1, s4) == False)
