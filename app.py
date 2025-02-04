from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/image-prompt', methods=['POST'])
def generate_image_prompt():
    try:
        data = request.get_json()

        # 驗證至少有一個參數存在
        if not any(key in data for key in ['where', 'who', 'what']):
            return jsonify({"error": "至少提供一個參數 (where、who、what)"}), 400

        # 提取參數
        where = data.get('where', '未知地點')
        who = data.get('who', '未知人物')
        what = data.get('what', '未知行為')

        # 模擬生成提示詞
        action_background = f"{where}，{who}正在{what}。"
        character_features = f"{who}的描述：{what}。"

        # 返回成功回應
        return jsonify({
            "action_background": action_background,
            "character_features": character_features
        }), 200

    except Exception:
        return jsonify({"error": "伺服器內部錯誤，請稍後重試"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
