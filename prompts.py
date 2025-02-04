SYSTEM_PROMPT = """
將使用者提供的資訊組合成圖像生成的提示詞,

請以 JSON 格式回傳結構化輸出，包含以下鍵值對:
{{
    "action_background": "圖片中角色的行為和背景",
    "character_features": "圖片中角色的外貌特徵"
}}
"""

USER_PROMPT = """
請根據以下資訊，生成圖像生成的提示詞。

- 在哪裡：{where}
- 有誰：{who}
- 做什麼：{what}
"""

IMAGE_PROMPT_REQUEST_EXAMPLE = {
    "where": "城市街頭",
    "who": "一名男子",
    "what": "騎著滑板",
}

IMAGE_PROMPT_RESPONSE_EXAMPLE = {
    "action_background": "在一個充滿活力的城市街頭，一名身穿紅色夾克的男子正騎著滑板穿梭在人群中，背景是高樓林立的都市風景",
    "character_features": "金色短髮、藍色眼睛、穿著紅色夾克、牛仔褲、約25歲、高挑身材、歐美人種",
}

NOTES = f"""
注意事項:
1. `action_background` 必須描述完整、具體，例如:
    {IMAGE_PROMPT_RESPONSE_EXAMPLE["action_background"]}

2. `character_features` 必須包含髮型、髮色、眼睛顏色、服飾風格、身高、年齡範圍、種族等，例如:
   {IMAGE_PROMPT_RESPONSE_EXAMPLE["character_features"]}
"""
