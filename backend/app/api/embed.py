from fastapi import APIRouter, Query, HTTPException, Request
from app.auth.users import get_user_context
from app.services.powerbi import PowerBIService

router = APIRouter()
powerbi_service = PowerBIService()


@router.post("/embed-info")
def get_embed_info(request: Request, user: str = None):

    auth_header = request.headers.get("Authorization")
    user_token = None

    if auth_header and auth_header.startswith("Bearer "):
        user_token = auth_header.split(" ")[1]

    # CASO USER OWNS DATA
    if user_token:
        embed_info = powerbi_service.get_embed_info_user(user_token)

        return {
            "user": "SSO user",
            "embedInfo": embed_info
        }

    # CASO APP OWNS DATA (vecchio)
    if not user:
        raise HTTPException(status_code=400, detail="User parameter required")

    try:
        user_context = get_user_context(user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    embed_info = powerbi_service.get_embed_info(user_context)

    if "error" in embed_info:
        return embed_info

    return {
        "user": user_context.username,
        "embedInfo": embed_info
    }

