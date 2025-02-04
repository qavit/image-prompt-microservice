# 圖片提示詞 API 微服務
根據人物、地點和行為，生成專供 LLM 圖像生成的提示詞。
目前使用模型：OpenAI `gpt-4o-mini`

## 目錄

1. [API 規格](#api-規格)
   - [規格文件](#規格文件)
   - [端點](#端點)
      - [請求](#請求)
      - [回應](#回應)
      - [錯誤處理](#錯誤處理)
      - [安全性](#安全性)
2. [開發者使用指南](#開發者使用指南)
   - [前置條件](#前置條件)
   - [步驟](#步驟)


## API 規格

此 API 服務可根據提供的地點、人物和行為生成圖像提示詞。

### 規格文件

請使用以下路徑進入 API 規格文件。

- `{base_url}/docs`（Swagger UI）
- `{base_url}/redoc`（Redocly）

### 端點

只有一個端點

```http
POST {base_url}/
```

#### 請求

接受 JSON 格式的請求體，包含 `where`、`who`、`what` 三個參數，至少提供一個。範例如下：

```json
{
    "where": "在一個充滿活力的城市街頭，一名身穿紅色夾克的男子正騎著滑板穿梭在人群中，背景是高樓林立的都市風景",
    "who": "一名男子",
    "what": "騎著滑板"
}
```

| 參數 | 描述 | 必填/選填 | 預設值 |
| --- | --- | --- | --- |
| `where` | 描述地點的字串 | 選填 | `"未知地點"` |
| `who` | 描述人物的字串 | 選填 | `"未知人物"` |
| `what` | 描述行為的字串 | 選填 | `"未知行為"` |

#### 回應

成功時回傳狀態碼 `200 Successful Response`，回應體會被解析成 JSON 格式


```json
{
  "action_background": "在一個充滿活力的城市街頭，一名身穿紅色夾克的男子正騎著滑板穿梭在人群中，背景是高樓林立的都市風景",
  "character_features": "金色短髮、藍色眼睛、穿著紅色夾克、牛仔褲、約25歲、高挑身材、歐美人種"
}
```

#### 錯誤處理
- 如果沒有提供任何參數，回傳 `400 Bad Request`。
- 如果發生伺服器錯誤，回傳 `500 Internal Server Error`。


#### 安全性
- 使用 Bearer Token 驗證請求中攜帶可用的 OpenAI API 金鑰。



## 開發者使用指南

### 前置條件

- 確保已安裝 Python。
- 確保已安裝 pip。

### 步驟

1. **複製儲存庫**
   ```bash
   git clone https://github.com/qavit/image-prompt-microservice.git
   cd image-prompt-microservice
   ```

2. **設置虛擬環境**
   ```bash
   python -m venv .venv
   source .venv/bin/activate # Linux/macOS
   ```

   ```powershell
   python -m venv .venv
   . .venv/Scripts/activate # Windows
   ```

3. **安裝相依套件**
   ```bash
   pip install -r requirements.txt
   ```

4. **設置環境變數**
   - 複製 `.env.example` 文件為 `.env`
   - 在 `.env` 文件中填寫您的 OpenAI API 金鑰：
     ```bash
     OPENAI_API_KEY=your-openai-api-key
     ```

5. **執行應用程式**
   ```bash
   uvicorn app:app --reload
   ```

   這將啟動一個執行在 `http://127.0.0.1:8000` 的伺服器。

   **使用 Docker 執行**

   您也可以使用 Docker 來執行應用程式：
   ```bash
   docker build -t image-prompt-microservice .
   docker run -p 8000:8000 image-prompt-microservice
   ```

   這將在 Docker 容器中執行應用程式，並將其映射到 localhost的 8000 埠。
