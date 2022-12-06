import pytest


@pytest.mark.colour("Red")
def test_sample_1():
    assert True


@pytest.mark.colour("Red", "Yellow")
def test_sample_2():
    assert True


@pytest.mark.colour("Blue")
def test_sample_3():
    assert True


@pytest.mark.colour("Green", "Yellow")
def test_sample_4():
    assert True
