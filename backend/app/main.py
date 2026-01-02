from fastapi import FastAPI

app = FastAPI(title="Intelligent Financial Behavior Analysis")

@app.get("/")
def health_check():
    return {"status": "OK", "message": "Backend is running"}
