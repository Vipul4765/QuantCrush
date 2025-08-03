from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.pattern_routes import router as pattern_router

app = FastAPI()

# ✅ Allow only specific frontend domain
origins = [
    "http://localhost:8082",  # ✅ Allow local React dev server
    "http://127.0.0.1:8082",
    "http://localhost:8081",  # ✅ Allow local React dev server
    "http://127.0.0.1:8081",
    "http://localhost:8083",  # ✅ Allow local React dev server
    "http://127.0.0.1:8083",
    # "https://your-frontend-domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "error": str(exc)},
    )

# ✅ Register API router
app.include_router(pattern_router)
