from deluge_interface import Deluge
from dotenv import load_dotenv
import os
import time

load_dotenv()


def test_magnet(deluge: Deluge):
    print("\nTesting magnet file")
    result = deluge.add_magnet(
        "magnet:?xt=urn:btih:375ae3280cd80a8e9d7212e11dfaf7c45069dd35&dn=archlinux-2023.02.01-x86_64.iso",
        name="test-magnet",
    )
    print(result.id)
    
    for i in range(5):
        time.sleep(1)
        print(result.get_status()["progress"])
    
    deluge.remove_torrent(result.id, remove_data=True)

def test_url(deluge: Deluge):
    print("\nTesting torrent URL")
    result = deluge.add_torrent_from_url("https://archlinux.org/releng/releases/2023.02.01/torrent/", name="test-url")
    print(result.id)
    
    for i in range(5):
        time.sleep(1)
        print(result.get_status()["progress"])
    
    deluge.remove_torrent(result.id, remove_data=True)

def test_file(deluge: Deluge):
    print("\nTesting torrent file")
    result = deluge.add_torrent_from_file("test-files", "archlinux-2023.02.01-x86_64.iso.torrent", name="test-torrent")
    print(result.id)
    
    for i in range(5):
        time.sleep(1)
        print(result.get_status()["progress"])
    
    deluge.remove_torrent(result.id, remove_data=True)


deluge = Deluge(os.getenv("HOST"), os.getenv("PASSWORD"))
print(deluge.session_id)
print(deluge.methods)

test_magnet(deluge)
test_url(deluge)
test_file(deluge)

# deluge.add_magnet("magnet:?xt=urn:btih:375ae3280cd80a8e9d7212e11dfaf7c45069dd35&dn=archlinux-2023.02.01-x86_64.iso", add_paused=True, name="test-magnet")
# deluge.add_torrent_from_url("https://archlinux.org/releng/releases/2023.02.01/torrent/", add_paused=True, name="test-url")
# deluge.add_torrent_from_file("test-files", "archlinux-2023.02.01-x86_64.iso.torrent", add_paused=True, name="test-torrent")
