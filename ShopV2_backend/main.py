from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    blacklist_router,
    index_router,
    login_router,
    order_router,
    product_router,
    register_router,
    user_router,
)

app = FastAPI(
    title="Online Shop API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(index_router.router)
app.include_router(login_router.router)
app.include_router(register_router.router)
app.include_router(user_router.router)
app.include_router(product_router.router)
app.include_router(order_router.router)
app.include_router(blacklist_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Online Shop API"}
