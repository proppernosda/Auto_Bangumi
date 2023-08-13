from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse

from module.conf import LOG_PATH
from module.security.api import get_current_user, UNAUTHORIZED
from module.models import APIResponse

router = APIRouter(prefix="/log", tags=["log"])


@router.get("")
async def get_log(current_user=Depends(get_current_user)):
    if not current_user:
        raise UNAUTHORIZED
    if LOG_PATH.exists():
        with open(LOG_PATH, "rb") as f:
            return Response(f.read(), media_type="text/plain")
    else:
        return Response("Log file not found", status_code=404)


@router.get("/clear", response_model=APIResponse)
async def clear_log(current_user=Depends(get_current_user)):
    if not current_user:
        raise UNAUTHORIZED
    if LOG_PATH.exists():
        LOG_PATH.write_text("")
        return JSONResponse(
            status_code=200,
            content={"msg_en": "Log cleared successfully.", "msg_zh": "日志清除成功。"},
        )
    else:
        return JSONResponse(
            status_code=406,
            content={"msg_en": "Log file not found.", "msg_zh": "日志文件未找到。"},
        )
