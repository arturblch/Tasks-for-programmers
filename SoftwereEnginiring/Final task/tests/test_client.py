import pytest
from RemoteProcessClient import RemoteProcessClient


@pytest.yield_fixture(scope="module")
def socket():
    remote_process_client = RemoteProcessClient('wgforge-srv.wargaming.net',443)
    yield remote_process_client
    remote_process_client.close()

def test_write_message(socket):
    assert socket.write_message('LOGIN', {"name": "Test_Conway"})[0] == 0
    assert socket.write_message('LOGOUT')[0] == 0

def test_defult_example(socket):
    assert socket.login("Test")[0] == 0
    assert socket.move(1, 1, 0)[0] == 0
    assert socket.map(1)[0] == 0
    assert socket.turn()[0] == 0
    assert socket.logout()[0] == 0
