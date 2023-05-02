from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from osrs_gept.container import OsrsContainer
from osrs_gept.routes import (
    latest,
    mapping,
    time_block,
    well_known,
)


def init_app(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    ctr = OsrsContainer()
    ctr.init_resources()
    ctr.wire(modules=[time_block, latest, mapping])

    @app.on_event("startup")
    async def startup():
        pass

    @app.on_event("shutdown")
    async def shutdown():
        pass

    # Wire up the routes
    app.include_router(time_block.router)
    app.include_router(latest.router)
    app.include_router(mapping.router)
    app.include_router(well_known.router, prefix="/.well-known")

    add_pagination(app)
