import pytest

from src.slice_view import SliceView


def test_create_slice_view() -> None:
    # All it has to do is not crash
    _ = SliceView([1, 2, 3], 0, 2, 1)
    assert True is True


def test_exception_raised_if_step_equal_to_zero() -> None:
    with pytest.raises(ValueError):
        _ = SliceView([1, 2, 3], 0, 2, 0)


@pytest.mark.parametrize(
    ("view", "expected"),
    [
        (SliceView([1, 2, 3, 4], step=2), [1, 3]),
        # step > 1
        (SliceView([1, 2, 3, 4]), [1, 2, 3, 4]),
        (SliceView([1, 2, 3, 4], start=1), [2, 3, 4]),
        (SliceView([1, 2, 3, 4], stop=3), [1, 2, 3]),
        (SliceView([1, 2, 3, 4], start=-2), [3, 4]),
        (SliceView([1, 2, 3, 4], stop=-1), [1, 2, 3]),
        # step < 1
        (SliceView([1, 2, 3, 4], step=-1), [4, 3, 2, 1]),
        (SliceView([1, 2, 3, 4], start=3, step=-1), [3, 2, 1]),
        (SliceView([1, 2, 3, 4], stop=1, step=-1), [4, 3, 2]),
        (SliceView([1, 2, 3, 4], start=-2, step=-1), [3, 2, 1]),
        (SliceView([1, 2, 3, 4], stop=-4, step=-1), [4, 3, 2]),
        # Multi steps
        (SliceView([1, 2, 3, 4], step=2), [1, 3]),
        (SliceView([1, 2, 3, 4], step=-2), [4, 2]),
        # start beyond boundary
        (SliceView([1, 2, 3, 4], start=6), []),
        (SliceView([1, 2, 3, 4], start=-6, step=-1), []),
        # Stop beyond boundary
        (SliceView([1, 2, 3, 4], step=6), [1, 2, 3, 4]),
        (SliceView([1, 2, 3, 4], stop=-6, step=-1), []),
        # Start after stop
        (SliceView([1, 2, 3, 4], start=3, stop=2), []),
        (SliceView([1, 2, 3, 4], start=2, stop=3, step=-1), []),
    ],
)
def test_slice_view_matches_expected(view: SliceView[int], expected: list[int]) -> None:
    assert expected == list(view)
