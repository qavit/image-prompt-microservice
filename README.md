# 圖片提示詞微服務
根據人物、地點和行為，生成專供 LLM圖像生成的提示詞。
使用模型：OpenAI `gpt-4o-mini`

## 設置和執行

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

### API 規格

#### 概述
此 API 用於根據提供的地點、人物和行為生成圖像提示詞。

#### 端點
- `POST /`：接受 JSON 格式的請求，包含 `where`、`who`、`what` 參數，返回生成的圖像提示詞。

#### 請求參數
- `where`（可選）：描述地點的字串。
- `who`（可選）：描述人物的字串。
- `what`（可選）：描述行為的字串。

#### 回應
- 成功時返回 `200 OK`，包含 `action_background` 和 `character_features`。
- 失敗時返回 `400 Bad Request` 或 `500 Internal Server Error`。

#### 回應格式

API 會以 JSON 格式回傳結構化輸出

```json
{
    "action_background": "圖片中角色的行為和背景",
    "character_features": "圖片中角色的外貌特徵"
}
```

- `"action_background"` 的值描述完整、具體。
  - 範例：`"在一個充滿活力的城市街頭，一名身穿紅色夾克的男子正騎著滑板穿梭在人群中，背景是高樓林立的都市風景"`

- `"character_features"` 的值包含髮型、髮色、眼睛顏色、服飾風格、身高、年齡範圍、種族等。
  - 範例：`"金色短髮、藍色眼睛、穿著紅色夾克、牛仔褲、約25歲、高挑身材、歐美人種"`

#### 錯誤處理
- 如果沒有提供任何參數，返回 `400 Bad Request`。
- 如果發生伺服器錯誤，返回 `500 Internal Server Error`。

#### 安全性
- 使用 Bearer Token 進行 API 認證。
