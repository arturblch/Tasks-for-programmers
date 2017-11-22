import pygame
from RemoteProcessClient import RemoteProcessClient

@pytest.yield_fixture
def socket():
    remote_process_client = RemoteProcessClient('wgforge-srv.wargaming.net', 443)
    yield _socket
    remote_process_client.close()

def test_write_message(socket)
    remote_process_client.write_message('LOGIN', {'name' : "Test_Conway"})

def test_write_message(socket)
    remote_process_client.write_message('LOGIN', {'name' : "Test_Conway"})
