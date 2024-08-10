# testing
* `pytest tests -v`
* `PYTHONDONTWRITEBYTECODE=1 pytest tests -v`
* `PYTHONDONTWRITEBYTECODE=1 pytest tests/test_log.py -v -p no:cacheprovider`
* for test_log use `PYTHONPATH=$(pwd) python tests/test_log.py`
* `PYTHONDONTWRITEBYTECODE=1 python inbund/test.py`