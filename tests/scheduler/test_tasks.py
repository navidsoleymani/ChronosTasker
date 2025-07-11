import pytest
from scheduler.tasks import add

@pytest.mark.celery(result_backend='rpc://')
def test_add_task():
    """
    Test the add task returns the correct result.
    """
    result = add.delay(4, 6)
    # Wait for the task to finish and get the result
    assert result.get(timeout=10) == 10
