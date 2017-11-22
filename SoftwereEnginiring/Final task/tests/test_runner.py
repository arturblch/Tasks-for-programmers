import pytest
from Runner import Runner


@pytest.yield_fixture(scope="module")
def runner():
    runner = Runner()
    yield runner
    runner.remote_process_client.close()


def test_defult_example(runner):
    assert runner.login("Test")[0] == 0
    assert runner.move(1, 1, 0)[0] == 0
    assert runner.turn()[0] == 0
    assert runner.logout()[0] == 0
