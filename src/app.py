from fastapi import APIRouter, FastAPI

from factclash.contradictions import router as contradictions



app = FastAPI()

api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(contradictions.router)
app.include_router(api_v1)

@app.get("/")
async def root():
    return {"message": "Hello I am confused, these facts don't make sense"}


