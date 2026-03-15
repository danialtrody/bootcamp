import sys

import uvicorn

from src.app import app

PORT = 8000
KEEP_ALIVE_TIMEOUT = 65

port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT

uvicorn.run(
    app,
    host="127.0.0.1",
    port=port,
    log_level="info",
    timeout_keep_alive=KEEP_ALIVE_TIMEOUT,
    access_log=True,
    proxy_headers=True,
)
