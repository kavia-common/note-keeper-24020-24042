from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from .core.config import load_config
from .routers.notes import router as notes_router

config = load_config()

app = FastAPI(
    **config.openapi_meta(),
    openapi_tags=[
        {
            "name": "Health",
            "description": "Service health and metadata endpoints.",
        },
        {
            "name": "Notes",
            "description": "Create, read, update, and delete notes.",
        },
        {
            "name": "WebSocket",
            "description": "Real-time features (reserved for future use).",
        },
    ],
)

# Allow all origins during development; restrict for prod as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():
    """
    Customize OpenAPI schema metadata and inject Ocean Professional theme hints.
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=config.app_name,
        version=config.version,
        description=config.description,
        routes=app.routes,
    )
    # Add custom extensions for docs UI theming (consumed by external renderers if supported)
    openapi_schema["x-theme"] = {
        "name": config.theme.name,
        "palette": {
            "primary": config.theme.primary,
            "secondary": config.theme.secondary,
            "success": config.theme.success,
            "error": config.theme.error,
            "background": config.theme.background,
            "surface": config.theme.surface,
            "text": config.theme.text,
            "gradient": config.theme.gradient,
        },
        "style": "Modern",
        "notes": "Clean layout, subtle shadows, rounded corners, minimalist design."
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Routers
app.include_router(notes_router)


# PUBLIC_INTERFACE
@app.get(
    "/",
    tags=["Health"],
    summary="Health Check",
    description="Check if the Notes Backend service is up and responsive.",
    responses={200: {"description": "Service is healthy."}},
)
def health_check():
    """Return a simple health status payload."""
    return {"status": "ok", "service": config.app_name, "version": config.version}


# PUBLIC_INTERFACE
@app.get(
    "/docs/usage",
    tags=["Health"],
    summary="API Usage & Realtime Info",
    description=(
        "How to use this API and reserved real-time capabilities.\n\n"
        "WebSocket endpoints are planned for future features such as live note collaboration.\n"
        "When available, connect to: `ws://<host>/ws/notes`.\n"
        "Until then, use the RESTful CRUD endpoints under /notes."
    ),
    responses={200: {"description": "Usage information returned."}},
)
def get_usage_info():
    """Provide human-readable usage notes and future WebSocket guidance."""
    return JSONResponse(
        {
            "theme": {
                "name": config.theme.name,
                "primary": config.theme.primary,
                "secondary": config.theme.secondary,
            },
            "rest_endpoints": {
                "list": "GET /notes",
                "create": "POST /notes",
                "get": "GET /notes/{note_id}",
                "update": "PUT /notes/{note_id}",
                "delete": "DELETE /notes/{note_id}",
            },
            "realtime": {
                "planned": True,
                "websocket_endpoint": "/ws/notes",
                "note": "WebSocket endpoints are not implemented yet; reserved for future."
            },
        }
    )
