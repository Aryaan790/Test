from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import math
import os

app = FastAPI(title="Calculator API")

# Serve static files (HTML/CSS/JS)
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def root():
    """Serve the calculator UI."""
    return FileResponse(os.path.join(static_dir, "index.html"))


@app.get("/api/calc")
async def calculate(
    a: float = Query(..., description="First operand"),
    b: float = Query(None, description="Second operand (optional for unary ops)"),
    op: str = Query(..., description="Operator: add, sub, mul, div, mod, pow, sqrt, abs, floor, ceil"),
):
    """Perform a calculation and return the result as JSON."""
    try:
        match op:
            case "add":
                result = a + b
            case "sub":
                result = a - b
            case "mul":
                result = a * b
            case "div":
                if b == 0:
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Division by zero"},
                    )
                result = a / b
            case "mod":
                if b == 0:
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Modulo by zero"},
                    )
                result = a % b
            case "pow":
                result = a ** b
            case "sqrt":
                if a < 0:
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Cannot take square root of negative number"},
                    )
                result = math.sqrt(a)
            case "abs":
                result = abs(a)
            case "floor":
                result = math.floor(a)
            case "ceil":
                result = math.ceil(a)
            case _:
                return JSONResponse(
                    status_code=400,
                    content={"error": f"Unknown operator: {op}"},
                )

        # Clean up float display (e.g. 4.0 -> 4)
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return {"operation": op, "a": a, "b": b, "result": result}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)