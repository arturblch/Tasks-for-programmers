import pytest
from Runner import Runner


@pytest.yield_fixture(scope="module")
def runner():
    runner = Runner()
    yield runner
    runner.remote_process_client.close()


def test_run_example(runner):
    runner.remote_process_client.login("Test_Conway")
    runner.remote_process_client.move(1, 1, 0)
    for i in range(10):
        response = runner.remote_process_client.map(1)
        print("Position - ", response[1]["train"][0]["position"])
        runner.remote_process_client.turn()
    assert response[1]["train"][0]["position"] == 10
    for i in range(10):
        response = runner.remote_process_client.map(1)
        print("Position - ", response[1]["train"][0]["position"])
        runner.remote_process_client.turn()
    runner.remote_process_client.logout()
