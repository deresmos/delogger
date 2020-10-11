import pytest

from delogger import DecoratorBase
from delogger import Delogger
from tests.lib.base import DeloggerTestBase


class _CanNotRun(DecoratorBase):
    decorator_name = "can_not_run"

    def can_run(self) -> bool:
        return False

    def wrapper(self, f, *args, **kwargs):
        self.logger.debug("not run")

        return False


class TestDecoratorBase(DeloggerTestBase):
    def test_not_can_run(self):
        delogger = Delogger("can_not_run")
        delogger.load_decorator(_CanNotRun())
        logger = delogger.get_logger()

        @logger.can_not_run
        def test_func():
            return 1

        ret = test_func()

        assert ret == 1

    def test_assert_already_defined_decorator(self):
        delogger = Delogger("already_defined")
        delogger.load_decorator(_CanNotRun())

        with pytest.raises(AttributeError):
            delogger.load_decorator(_CanNotRun())
