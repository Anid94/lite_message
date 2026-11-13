from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse

from exceptions import AppError
from routes import users

app = FastAPI()

app.include_router(users.router)

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/health", status_code=200)
def check_health():
    return {"status":"OK"}