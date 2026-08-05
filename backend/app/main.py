from fastapi import FastAPI


app = FastAPI(title="SupportMind API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "service": "SupportMind API",
        "status": "running",
    }
