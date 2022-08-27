import importlib.util

from .celery import app as celery_app

mypy_package = importlib.util.find_spec("mypy")
if mypy_package:
    from footballdata.checks.mypy_check import mypy  # noqa


__all__ = ("celery_app",)
