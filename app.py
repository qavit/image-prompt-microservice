import json
import logging
import os
import re

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 載入自定義的提示詞
from prompts import (
    SYSTEM_PROMPT,
    USER_PROMPT,
    NOTES,
    IMAGE_PROMPT_REQUEST_EXAMPLE,
    IMAGE_PROMPT_RESPONSE_EXAMPLE,
)

# 載入 .env 文件中的環境變數
load_dotenv()

app = FastAPI(
    title="圖片提示詞微服務",
    description="此 API 可根據使用者提供的地點、人物和行為生成圖像提示詞。",
    version="1.0.0",
)

# 設定 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 設置日誌級別，預設為 DEBUG
log_level = os.getenv("LOG_LEVEL", "DEBUG").upper()
logging.basicConfig(level=log_level)
logger = logging.getLogger()


# 定義請求模型
class ImagePromptRequest(BaseModel):
    where: str = "未知地點"
    who: str = "未知人物"
    what: str = "未知行為"

    class Config:
        json_schema_extra = {"example": IMAGE_PROMPT_REQUEST_EXAMPLE}


# 定義回應模型
class ImagePromptResponse(BaseModel):
    action_background: str
    character_features: str

    class Config:
        json_schema_extra = {"example": IMAGE_PROMPT_RESPONSE_EXAMPLE}


@app.post("/", response_model=ImagePromptResponse)
async def generate_image_prompt(
    data: ImagePromptRequest
) -> ImagePromptResponse:
    """根據提供的地點、人物和行為生成圖像提示詞。

    此端點接受包含可選參數 `where`、`who` 和 `what` 的 JSON 請求體，
    構建發送到 OpenAI API 的請求，並返回結構化的圖像提示詞。

    Parameters:
    - data (ImagePromptRequest): 包含 `where`、`who` 和 `what` 的請求體。

    Returns:
    - ImagePromptResponse: 回應體，包含 `action_background` 和 `character_features`。

    Raises:
    - HTTPException: 如果未提供任何參數（`where`、`who`、`what`）。
    """
    try:
        # 驗證至少有一個參數存在
        if not any([data.where, data.who, data.what]):
            raise HTTPException(
                status_code=400, detail="至少提供一個參數 (where、who、what)"
            )

        logger.debug(f"\n收到請求體：\n{data.model_dump()}\n")

        # 構建請求負載
        payload = {
            "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT + NOTES},
                {
                    "role": "user",
                    "content": USER_PROMPT.format(
                        where=data.where, who=data.who, what=data.what
                    ),
                },
            ],
            "temperature": 0.7,
        }

        logger.debug(f"\n即將向 OpenAI API 發送請求體：\n{payload}\n")

        # 設置請求標頭
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json",
        }

        # 發送請求到 OpenAI API
        url = os.getenv("OPENAI_API_ENDPOINT")
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()

        # 提取生成的提示詞
        choices = response_data.get("choices", [{}])
        message_content = choices[0].get("message", {}).get("content", "生成失敗")

        logger.debug(f"\n回應體：\n{message_content}\n")

        # 假設 message_content 是 JSON 格式的字串，解析它
        try:
            clean_content = re.sub(r"```json|```", "", message_content).strip()
            content_json = json.loads(clean_content)
            action_background = content_json.get("action_background", "解析失敗")
            character_features = content_json.get("character_features", "解析失敗")
        except json.JSONDecodeError:
            action_background = "解析失敗"
            character_features = "解析失敗"

        # 返回成功回應
        return ImagePromptResponse(
            action_background=action_background,
            character_features=character_features
        )

    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail="伺服器內部錯誤，請稍後重試")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
