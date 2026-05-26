from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.embed import router as embed_router

app = FastAPI(
    title="Power BI Embedded PoC Backend",
    description="Backend minimal per PoC Power BI Embedded (FastAPI)",
    version="0.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_origin_regex="https://.*\\.ngrok-free\\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(embed_router, prefix="/api")

@app.get("/")
def healthcheck():
    return {"status": "ok", "message": "Backend PoC Power BI Embedded"}
