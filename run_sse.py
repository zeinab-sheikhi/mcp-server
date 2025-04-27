import logging 

import uvicorn
from starlette.applications import Starlette

from sse import SseHandler
from server import create_server

logger = logging.getLogger(__name__)

def create_app():
    server, init_options = create_server()
    sse_handler = SseHandler(server, init_options)
    app = Starlette(routes=sse_handler.get_routes())
    return app


def main():
    app = create_app()
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=3001,
        log_level="debug",
        log_config=None,
    )
    server = uvicorn.Server(config)
    logger.info("Starting server...")
    try:
        server.run()
    except Exception as e:
        logger.error(f"Failed to start server: {e}", exc_info=True)
        raise e


if __name__ == "__main__":
    main()
