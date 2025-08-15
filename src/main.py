from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.shared.database.psql import engine
from src.shared.database.psql import Base
from src.modules.auth.http.rest.controller.auth_controller import router as auth_router
from src.modules.user.http.rest.controller.user_controller import router as user_router
from src.modules.products.http.rest.controller.product_controller import router as product_router
from src.modules.carts.http.rest.controller.carts_controller import router as carts_router
app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(carts_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
