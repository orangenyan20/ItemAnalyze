import streamlit as st
from github import Github
from datetime import datetime
import time

# =========================
# ページ設定
# =========================
st.set_page_config(
    page_title="妖怪ウォッチ3 宝箱記録",
    layout="wide"
)

# =========================
# CSS
# =========================
st.markdown("""
<style>

div.stButton > button {
    width: 100%;
    height: 60px;
    font-size: 20px;
    font-weight: bold;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

h3 {
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# =========================
# パスワード認証
# =========================
APP_PASSWORD = st.secrets["APP_PASSWORD"]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:

    st.title("ログイン")

    password = st.text_input(
        "パスワード",
        type="password"
    )

    if st.button("ログイン"):

        if password == APP_PASSWORD:

            st.session_state.authenticated = True
            st.rerun()

        else:

            st.error("パスワードが違います")

    st.stop()

# =========================
# GitHub設定
# =========================
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]

REPO_NAME = "orangenyan20/ItemAnalyze"
FILE_PATH = "data.txt"
BRANCH = "main"

# =========================
# GitHub接続
# =========================
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# =========================
# ジャンル
# =========================
categories = {
    "食べ物": [101, 102, 103, 104],
    "漢方": [201, 202, 203, 204],
    "経験値玉": [301, 302, 303, 304],
    "こけし": [401, 402, 403, 404],
    "コイン": [501, 502, 503, 504],
    "バトル": [601, 602, 603, 604],
    "その他": [701, 702, 703, 704]
}

# =========================
# 最新ファイル取得
# =========================
def get_latest_data():

    file = repo.get_contents(
        FILE_PATH,
        ref=BRANCH
    )

    content = file.decoded_content.decode("utf-8")

    lines = [
        line for line in content.splitlines()
        if line.strip() != ""
    ]

    return file, lines

# =========================
# データ追加
# =========================
def append_data(value):

    for _ in range(3):

        try:

            file, lines = get_latest_data()

            lines.append(str(value))

            updated_content = "\n".join(lines) + "\n"

            repo.update_file(
                FILE_PATH,
                f"Add {value}",
                updated_content,
                file.sha,
                branch=BRANCH
            )

            return True

        except Exception as e:

            time.sleep(1)

    st.error("書き込み失敗")

    return False

# =========================
# 最新削除
# =========================
def delete_last():

    try:

        file, lines = get_latest_data()

        if len(lines) == 0:

            st.warning("データなし")
            return

        deleted = lines.pop()

        updated_content = "\n".join(lines)

        if updated_content != "":
            updated_content += "\n"

        repo.update_file(
            FILE_PATH,
            f"Delete {deleted}",
            updated_content,
            file.sha,
            branch=BRANCH
        )

        st.success(f"削除: {deleted}")

    except Exception:

        st.error("削除失敗")

# =========================
# 現在データ取得
# =========================
_, current_lines = get_latest_data()

count = len(current_lines)

last_data = current_lines[-1] if count > 0 else "-"

# =========================
# 上部UI
# =========================
top1, top2, top3 = st.columns([4, 1, 1])

with top1:
    st.title("妖怪ウォッチ3 宝箱")

with top2:
    st.metric("記録数", count)

with top3:
    st.metric("最新", last_data)

st.caption(
    f"最終更新: {datetime.now().strftime('%H:%M:%S')}"
)

st.divider()

# =========================
# 横並びボタン
# =========================
category_cols = st.columns(len(categories))

for col, (category_name, values) in zip(category_cols, categories.items()):

    with col:

        st.subheader(category_name)

        for value in values:

            if st.button(
                str(value),
                key=f"{category_name}_{value}"
            ):

                success = append_data(value)

                if success:
                    st.rerun()

# =========================
# 削除
# =========================
st.divider()

if st.button("直近1件を削除"):

    delete_last()

    st.rerun()
