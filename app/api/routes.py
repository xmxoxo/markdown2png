from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import sys
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.md2png_lib import md_to_png, get_base64
from src.qiniu_lib import upload_to_qiniu
from app.core.config import settings

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str


class Markdown2PngRequest(BaseModel):
    md_text: str = ""
    isupload: Optional[bool] = False
    cssfile: Optional[str] = "template/base.css"
    template: Optional[str] = ""
    width: Optional[int] = 1080
    from_url: Optional[str] = ""


class Markdown2PngResponse(BaseModel):
    success: bool
    message: str
    local_path: Optional[str] = None
    qiniu_url: Optional[str] = None
    base64: str


@router.get("/health", response_model=HealthResponse, summary="健康检查")
async def health():
    """
    健康检查接口，用于验证服务是否正常运行
    """
    return {
        "status": "ok",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@router.post("/markdown2png", response_model=Markdown2PngResponse, summary="Markdown转PNG")
async def markdown2png_api(request: Markdown2PngRequest):
    """
    将Markdown文本转换为PNG图片
    
    - **md_text**: Markdown文本内容
    - **from_url**: 从URL地址读取markdown，如果不为空则优先读取，覆盖md_text参数
    - **isupload**: 是否上传到七牛云存储，默认false
    - **cssfile**: CSS样式文件路径，默认"template/base.css"
    - **template**: HTML模板文件路径，默认空字符串（不使用模板）
    - **width**: 输出图片宽度，默认1080
    """
    try:
        md_text = request.md_text
        from_url = request.from_url.strip()
        
        if from_url:
            try:
                response = requests.get(from_url, timeout=30)
                response.raise_for_status()
                response.encoding = "utf-8"
                md_text = response.text
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"从URL读取markdown失败: {str(e)}")
        
        if not md_text.strip():
            raise HTTPException(status_code=400, detail="md_text不能为空")
        
        output_path = settings.OUTPUT_DIR
        os.makedirs(output_path, exist_ok=True)
        
        local_file = await md_to_png(
            md_text=md_text,
            output_path=output_path,
            cssfile=request.cssfile,
            template_file=request.template,
            width=request.width
        )
        
        if not local_file:
            raise HTTPException(status_code=500, detail="图片生成失败")
        
        qiniu_url = None
        if request.isupload:
            if not settings.QINIU_ACCESS_KEY or not settings.QINIU_SECRET_KEY:
                qiniu_url = ""
                # raise HTTPException(status_code=400, detail="七牛云配置未设置")
            
            qiniu_url = upload_to_qiniu(local_file, "markdown2png")
            if not qiniu_url:
                qiniu_url = ""
                # raise HTTPException(status_code=500, detail="七牛云上传失败")
        
        # 计算相对路径
        output_dir_name = os.path.basename(os.path.normpath(output_path))
        relative_path = f"/{output_dir_name}/{os.path.basename(local_file)}"
        
        # 增加返回base64
        b64 = get_base64(local_file)

        return {
            "success": True,
            "message": "图片生成成功",
            "local_path": relative_path,
            "qiniu_url": qiniu_url,
            "base64": b64
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")