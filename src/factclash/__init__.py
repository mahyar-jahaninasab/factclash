from factclash.app.main import app
import uvicorn

def main() -> None:
    uvicorn.run("factclash.app.main:app", host="0.0.0.0", port=8010, reload=True)
