# Streamlit×LangGraph（Human-in-the-loop）キャッチコピー生成アプリ

本リポジトリは、StreamlitとLangGraphを用いたキャッチコピー生成アプリのサンプルコードである。  
LangGraphでHuman-in-the-loopの実装も実現している。

<img width="500px" src="./images/demo.gif">

## 使い方
- リポジトリのクローン
```
git clone https://github.com/yamato0811/langgraph-streamlit-human-in-the-loop.git
cd langgraph-streamlit-human-in-the-loop
```
- 仮想環境の作成（任意）
```
python -m venv .venv
source .venv/bin/activate
```
- ライブラリのインストール
```
pip install -r requirements.txt
```
- Streamlitの実行
```
streamlit run app.py
```

## ディレクトリ構成
```
.
├── agent
│   ├── agent.py  # エージェントのメインロジック
│   ├── graph.py  # Graphクラスの定義
│   ├── node.py  # NodeとNode functionの定義
│   ├── output_structure.py  # LLM出力構造の定義
│   ├── prompt
│   │   └── prompt_templates.yaml  # プロンプトテンプレート
│   └── state.py # Stateの定義
├── app.py  # Streamlitアプリのメインロジック
├── components
│   └── input_form.py  # Streamlitの入力フォーム
├── graph.md  # Graphのmermaid書き出しファイル
├── models
│   └── llm.py  # LLMモデルの定義
└── utils
    ├── app_session_manager.py  # Streamlitのセッション管理
    ├── app_user_input_logic.py  # Streamlitのユーザー入力ロジック
    ├── app_util.py  # Streamlitのユーティリティ関数
    └── node_util.py  # Nodeのユーティリティ関数
```