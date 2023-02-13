# Likely Required Headers

# RPC Commands
- `auth.login`
    - Params: [password]
    - Result: boolean
    - Notes: Sets the set-cookie header to `_session_id=<id>`
- `system.listMethods`
    - Params: []
    - Result: `[method: str...]`