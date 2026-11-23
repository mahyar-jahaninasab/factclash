import uvicorn


def main() -> None:
    uvicorn.run(
        "factclash.entrypoints.main:app", host="0.0.0.0", port=8010, reload=True
    )
