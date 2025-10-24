from scalar_fastapi import get_scalar_api_reference
from fastapi import FastAPI


from contextlib import asynccontextmanager  # for lifespan event handler
from rich import panel, print
from app.database.session import create_db_tables
from app.api.router import master_router


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("Starting up shipment server...", style="bold green"))
    await create_db_tables()
    yield
    print(panel.Panel("Shutting down shipment server...", style="bold red"))


app = FastAPI(lifespan=lifespan_handler, title="Yamusa's Shipment API", version="0.1.0")
# db = Database()

app.include_router(
    master_router,
)


class City:
    def __init__(self, name, location) -> None:
        self.name: str = name
        self.location: int = location


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
