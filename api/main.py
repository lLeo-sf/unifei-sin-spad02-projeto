from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller import router as report_router

def create_app() -> FastAPI:
    app = FastAPI()

    origins = [
        "http://localhost:3000",  # porta padrão do React
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,            # quais origens podem acessar
        allow_credentials=True,           # libera credenciais (cookies, auth headers)
        allow_methods=["*"],              # GET, POST, PUT...
        allow_headers=["*"],              # Content-Type, Authorization...
    )

    app.include_router(report_router)

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
