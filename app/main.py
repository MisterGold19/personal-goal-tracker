# run via uvicorn app.main:app --reload
# --reload - tryb developerski- nie musze ręcznie restartować serwer za każdym razem
from fastapi import FastAPI, APIRouter

# uvicorn potrzebuje instancji FastAPi
# uvicorn - to serwer
app = FastAPI()

placeholder_router = APIRouter(prefix="/api/v1")

# Podpięcie routera do aplikacji
app.include_router(placeholder_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
