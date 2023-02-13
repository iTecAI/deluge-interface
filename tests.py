from deluge_interface import Deluge
from dotenv import load_dotenv
import os

load_dotenv()


def test_magnet(deluge: Deluge):
    result = deluge.add_magnet(
        "magnet:?xt=urn:btih:375ae3280cd80a8e9d7212e11dfaf7c45069dd35&dn=archlinux-2023.02.01-x86_64.iso",
        add_paused=True,
        name="test-magnet",
    )
    print(result.id)
    print(result.status())


deluge = Deluge(os.getenv("HOST"), os.getenv("PASSWORD"))
print(deluge.session_id)
print(deluge.methods)

test_magnet(deluge)

# deluge.add_magnet("magnet:?xt=urn:btih:375ae3280cd80a8e9d7212e11dfaf7c45069dd35&dn=archlinux-2023.02.01-x86_64.iso", add_paused=True, name="test-magnet")
# deluge.add_torrent_from_url("https://archlinux.org/releng/releases/2023.02.01/torrent/", add_paused=True, name="test-url")
# deluge.add_torrent_from_file("test-files", "archlinux-2023.02.01-x86_64.iso.torrent", add_paused=True, name="test-torrent")
