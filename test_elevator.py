import pytest

from elevator import Direction, Elevator


@pytest.mark.parametrize(
    "floor, direction, explicit",
    (
        (1, Direction.UP, False),
        (3, Direction.DOWN, True),
    )
)
def test_init(floor, direction, explicit):
    if explicit:
        elevator = Elevator(floor, direction)
    else:
        elevator = Elevator()

    assert elevator.state() == (floor, direction)


@pytest.mark.parametrize(
    "floor, direction",
    (
        (2, Direction.UP),
        (0, Direction.DOWN),
    )
)
def test_correctly_sets_direction(floor, direction):
    elevator = Elevator()

    elevator.request_floor(floor)
    elevator.process()

    assert elevator.state() == (floor, direction)


@pytest.mark.parametrize(
    "current_floor, requested_floors, expected_floor, direction",
    (
        (2, [3, 1], 3, Direction.UP),
        (2, [3, 1], 1, Direction.DOWN)
    )
)
def test_keeps_direction(current_floor, requested_floors, expected_floor, direction):
    elevator = Elevator(current_floor, direction)

    for floor in requested_floors:
        elevator.request_floor(floor)

    elevator.process()
    assert elevator.state() == (expected_floor, direction)


def test_multiple_request_for_the_same_floor_should_not_add_multiple_requests():
    elevator = Elevator()

    # two consequent requests
    elevator.request_floor(2)
    elevator.request_floor(2)

    elevator.request_floor(3)

    elevator.process()
    assert elevator.state() == (2, Direction.UP)

    elevator.process()
    assert elevator.state() == (3, Direction.UP)


def test_up_down_request_should_be_prioritized_correctly():
    elevator = Elevator(3, Direction.DOWN)

    elevator.request_floor(0)
    elevator.request_floor(1)
    elevator.process()

    assert elevator.state() == (1, Direction.DOWN)


def test_elevator_moves_to_the_higher_floor_and_direction_should_be_up():
    elevator = Elevator(0, Direction.DOWN)

    elevator.request_floor(1)
    elevator.process()

    assert elevator.state() == (1, Direction.UP)


def test_elevator_does_not_move_when_input_is_same():
    elevator = Elevator(1, Direction.UP)

    elevator.request_floor(1)
    elevator.process()

    assert elevator.state() == (1, Direction.UP)


def test_elevator_does_not_change_down_direction_when_input_is_the_same():
    elevator = Elevator(0, Direction.DOWN)

    elevator.request_floor(0)
    elevator.process()

    assert elevator.state() == (0, Direction.DOWN)


def test_elevator_moves_when_tick_is_called():
    elevator = Elevator()

    elevator.request_floor(0)
    assert elevator.state() == (1, Direction.UP)

    elevator.process()
    assert elevator.state() == (0, Direction.DOWN)


def test_out_of_order_request_should_be_prioritize():
    elevator = Elevator()

    elevator.request_floor(5)
    elevator.request_floor(2)
    elevator.process()

    assert elevator.state() == (2, Direction.UP)
