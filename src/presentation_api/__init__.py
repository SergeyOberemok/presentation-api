import os
import uvicorn


def main() -> None:
    uvicorn.run(
        "presentation_api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("ENV", "dev") == "dev",
    )
