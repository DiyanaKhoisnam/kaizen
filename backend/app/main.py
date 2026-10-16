from fastapi import FastAPI

app = FastAPI(title="kaizen")

@app.get("/health")
def health():
    return {"status":"ok"}
