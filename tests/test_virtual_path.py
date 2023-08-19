from giford.util import Point, Movement, VirtualPath


def test_point():
    p = Point(-1, 1)
    assert p.x == -1 and p.y == 1


def test_movement():
    p1 = Point(0, -1)
    p2 = Point(1, -1)
    m = Movement(p1, p2)
    assert m.origin.x == 0 and m.origin.y == -1
    assert m.target.x == 1 and m.target.y == -1


def test_movement_formula():
    # these are WELL beyond what is reasonable, but want to test distance formula
    p1 = Point(-3, 2)
    p2 = Point(0, -2)
    m = Movement(p1, p2)

    assert m.x_distance == 3
    assert m.y_distance == -4
    assert m.distance() == 5


def test_virtual_path_empty():
    vp = VirtualPath()

    assert len(vp.points) == 0

    try:
        vp.calculate_movements()
    except Exception as e:
        assert str(e) == "no points to produce movements"
        pass


def test_virtual_path_one_point():
    vp = VirtualPath(origin_point=Point.get_true_origin())
    assert len(vp.points) == 1
    origin_point = vp.points[0]

    movements: list[Movement] = vp.calculate_movements()
    assert len(movements) == 1

    mov = movements[0]
    assert mov.origin == origin_point and mov.target == origin_point


def test_virtual_path_multi_point_no_origin():
    p0 = Point(-1, 1)
    vp = VirtualPath(origin_point=p0)

    p1 = Point(0, 0)
    vp.add_point(p1)

    vp.add_point_from_coords(1, -1)

    movements: list[Movement] = vp.calculate_movements(is_from_true_origin=False)

    assert len(movements) == 2

    assert movements[0].origin == p0 and movements[0].target == p1
    assert (
        movements[1].origin == p1
        and movements[1].target.x == 1
        and movements[1].target.y == -1
    )


def test_virtual_path_multi_point_from_true_origin():
    # this test uses calculate movements in the way that is useful
    p0 = Point(-1, 1)
    p1 = Point(0, 0)
    p2 = Point(1, -1)
    vp = VirtualPath().add_point(p0).add_point(p1).add_point(p2)

    movements: list[Movement] = vp.calculate_movements()

    assert len(movements) == 3

    assert movements[0].origin == Point(0, 0) and movements[0].target == p0
    assert movements[1].origin == Point(0, 0) and movements[1].target == p1
    assert movements[2].origin == Point(0, 0) and movements[2].target == p2
