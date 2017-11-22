import pytest
from Runner import Runner


@pytest.yield_fixture(scope="module")
def runner():
    runner = Runner()
    yield runner
    runner.remote_process_client.close()


def test_defult_example(runner):
    runner.login("Test")
    assert runner.remote_process_client.read_response()[0] == 0
    runner.move(1, 1, 0)
    assert runner.remote_process_client.read_response()[0] == 0
    runner.turn()
    assert runner.remote_process_client.read_response()[0] == 0
    runner.logout()