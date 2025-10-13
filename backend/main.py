# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow your frontend origin
origins = [
    "http://localhost:3000",      # for local Next.js dev
    "http://127.0.0.1:3000",
    # Add your deployed frontend domain here later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # or ["*"] for dev
    allow_credentials=True,
    allow_methods=["*"],          # important — allows OPTIONS, POST, etc.
    allow_headers=["*"],
)

# Then import and include your routers
from backend.routes.analyze import router as analyze_router
app.include_router(analyze_router, prefix="/analyze")
