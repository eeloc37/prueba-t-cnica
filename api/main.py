from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from missing_number import NaturalNumbersSet

app = FastAPI(
    title="Missing Number API",
    version="1.0.0"
)

# Estado en memoria (simple y explícito)
numbers_set: NaturalNumbersSet | None = None


class ExtractRequest(BaseModel):
    number: int = Field(..., ge=1, le=100)


@app.post("/extract-number")
def extract_number(payload: ExtractRequest):
    global numbers_set

    try:
        numbers_set = NaturalNumbersSet()
        numbers_set.extract(payload.number)
        return {
            "message": "Número extraído correctamente",
            "extracted": payload.number
        }
    except (ValueError, TypeError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/missing-number")
def get_missing_number():
    if numbers_set is None:
        raise HTTPException(
            status_code=400,
            detail="No se ha extraído ningún número"
        )

    try:
        missing = numbers_set.get_missing_number()
        return {
            "missing_number": missing
        }
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
"""
    Ejecutar:
    uvicorn main:app --reload
"""
