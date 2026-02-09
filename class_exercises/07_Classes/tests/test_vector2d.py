from solutions.vector2d import Vector2D


def test__str__():
    vector = Vector2D(3.0,4.0)
    assert str(vector) == "Vector2D(3.0,4.0)"

def test__repr__():
    vector = Vector2D(3.0,4.0)
    assert repr(vector) == "Vector2D(3.0,4.0)"

def test__eq__():
    vector = Vector2D(3.0,4.0)
    equal =  Vector2D(3.0,4.0)
    not_equal =  Vector2D(4.0,3.0)
    not_isinstance = (4.0,3.0)

    assert (vector == equal) == True
    assert (vector == not_equal) == False
    assert (vector == not_isinstance) == False

    
def test__add__():
    vector1 = Vector2D(3.0,4.0)
    vector2 =  Vector2D(3.0,4.0)
    vector3 = Vector2D(0.0,0.0)
    vector4 = Vector2D(-1.0,-1.0)

    
    assert (vector1 + vector2) == Vector2D(6.0,8.0)
    assert (vector1 + vector3) == Vector2D(3.0,4.0)
    assert (vector1 + vector4) == Vector2D(2.0,3.0)



def test__sub__():
    vector1 = Vector2D(3.0,4.0)
    vector2 =  Vector2D(3.0,4.0)
    vector3 = Vector2D(0.0,0.0)
    vector4 = Vector2D(-1.0,-1.0)

    assert (vector1 - vector2) == Vector2D(0.0,0.0)
    assert (vector1 - vector3) == Vector2D(3.0,4.0)
    assert (vector1 - vector4) == Vector2D(4.0,5.0)
   
def test__mul__():
    vector = Vector2D(3.0,4.0)

    assert (vector*0) == Vector2D(0.0,0.0)
    assert (vector*-1) == Vector2D(-3.0,-4.0)
    assert (vector*5) == Vector2D(15.0,20.0)



def test__abs__():
    vector1 = Vector2D(3.0,4.0)
    vector2 = Vector2D(0.0,0.0)
    vector3 = Vector2D(-3.0,-4.0)

    assert abs(vector1) == 5.0
    assert abs(vector2) == 0.0
    assert abs(vector3) == 5.0


def test_magnitude():
    vector1 = Vector2D(3.0,4.0)
    vector2 = Vector2D(0.0,0.0)
    vector3 = Vector2D(-3.0,-4.0)


    assert vector1.magnitude() == 5.0
    assert vector2.magnitude() == 0.0
    assert vector3.magnitude() == 5.0


def test_dot():
    vector1 = Vector2D(3.0,4.0)
    vector2 = Vector2D(2.0,2.0)
    vector3 = Vector2D(0.0,0.0)
    vector4 = Vector2D(-1.0,-2.0)

    
    assert vector1.dot(vector2) == 14.0
    assert vector1.dot(vector3) == 0.0
    assert vector1.dot(vector4) == -11.0


