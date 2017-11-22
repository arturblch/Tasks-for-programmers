import pytest
from RemoteProcessClient import RemoteProcessClient


@pytest.yield_fixture(scope="module")
def socket():
    remote_process_client = RemoteProcessClient('wgforge-srv.wargaming.net',
                                                443)
    yield remote_process_client
    remote_process_client.close()


def test_write_message(socket):
    socket.write_message('LOGIN', {"name": "Test_Conway"})
    assert socket.read_response()[0] == 0


