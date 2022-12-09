import pytest
import sys
from loguru import logger


logger.remove()
logger.add(sys.stderr, level="DEBUG")


@pytest.mark.colour("Red")
def test_sample_1():
    logger.debug("Executing test: test_sample_1")
    logger.debug("Finished test: test_sample_1")


@pytest.mark.colour("Red", "Yellow")
def test_sample_2():
    logger.debug("Executing test: test_sample_2")
    logger.debug("Finished test: test_sample_2")


@pytest.mark.colour("Blue")
def test_sample_3():
    logger.debug("Executing test: test_sample_3")
    logger.debug("Finished test: test_sample_3")


@pytest.mark.colour("Green", "Yellow")
def test_sample_4():
    logger.debug("Executing test: test_sample_4")
    logger.debug("Finished test: test_sample_4")
