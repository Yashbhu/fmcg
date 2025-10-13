from fastapi import FastAPI
from backend.routes import tenders, analyze

app = FastAPI(title="Tender Intelligence API 🚀")

# Attach routers
app.include_router(tenders.router, prefix="/tenders", tags=["Tenders"])
app.include_router(analyze.router, prefix="/analyze", tags=["Analyze"])

@app.get("/")
def root():
    return {"message": "✅ Tender Intelligence Backend is running!"}
