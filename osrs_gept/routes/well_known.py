from fastapi.responses import FileResponse
from fastapi.routing import APIRouter

router = APIRouter()


@router.get("/ai-plugin.json", include_in_schema=False)
def get_ai_plugin():
    return FileResponse("osrs_gept/static/ai-plugin.json")


@router.get("/logo.png", include_in_schema=False)
def get_logo():
    return FileResponse("osrs_gept/static/logo.png")
