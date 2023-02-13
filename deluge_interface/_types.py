from typing import TypedDict

class TorrentStatus(TypedDict):
    active_time: int
    seeding_time: int
    finished_time: int
    all_time_download: int
    storage_mode: str
    distributed_copies: float
    download_payload_rate: int
    file_priorities: list
    hash: str
    auto_managed: bool
    is_auto_managed: bool
    is_finished: bool
    max_connections: int
    max_download_speed: int
    max_upload_slots: int
    max_upload_speed: int
    message: str
    move_on_completed_path: str
    move_on_completed: bool
    move_completed_path: str
    move_completed: bool
    next_announce: int
    num_peers: int
    num_seeds: int
    owner: str
    paused: bool
    prioritize_first_last: bool
    prioritize_first_last_pieces: bool
    sequential_download: bool
    progress: float
    shared: bool
    remove_at_ratio: bool
    save_path: str
    download_location: str
    seeds_peers_ratio: float
    seed_rank: int
    state: str
    stop_at_ratio: bool
    stop_ratio: float
    time_added: int
    total_done: int
    total_payload_download: int
    total_payload_upload: int
    total_peers: int
    total_seeds: int
    total_uploaded: int
    total_wanted: int
    total_remaining: int
    tracker: str
    tracker_host: str
    trackers: list
    tracker_status: str
    upload_payload_rate: int
    comment: str
    creator: str
    num_files: int
    num_pieces: int
    piece_length: int
    private: bool
    total_size: int
    eta: int
    file_progress: list
    files: list
    orig_files: list
    is_seed: bool
    peers: list
    queue: int
    ratio: float
    completed_time: int
    last_seen_complete: int
    name: str
    pieces: list
    seed_mode: bool
    super_seeding: bool
    time_since_download: int
    time_since_upload: int
    time_since_transfer: int