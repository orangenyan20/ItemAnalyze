import streamlit as st
from github import Github

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

REPO_NAME = "ユーザー名/リポジトリ名"
FILE_PATH = "data.txt"
BRANCH = "main"

# =========================
# GitHub接続
# =========================
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# =========================
# データ定義
# =========================
categories = {
    "食べ物": {
        "粗品": 1,
        "普通": 2,
        "高級": 3,
        "最高級": 4
    },

    "経験値玉": {
        "粗品": 5,
        "普通": 6,
        "高級": 7,
        "最高級": 8
    },

    "バトルアイテム": {
        "粗品": 9,
        "普通": 10,
        "高級": 11,
        "最高級": 12
    }
}

# =========================
# ファイル取得
# =========================
def get_file_data():

    file = repo.get_contents(FILE_PATH, ref=BRANCH)

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

    try:

        file, lines = get_file_data()

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
        st.error(e)
        return False

# =========================
# 最新削除
# =========================
def delete_last():

    try:

        file, lines = get_file_data()

        if len(lines) == 0:
            st.warning("データがありません")
            return

        deleted = lines.pop()

        updated_content = "\n".join(lines)

        if updated_content != "":
            updated_content += "\n"

        repo.update_file(
            FILE_PATH,
            f"Delete last line {deleted}",
            updated_content,
            file.sha,
            branch=BRANCH
        )

        st.success(f"削除しました: {deleted}")

    except Exception as e:
        st.error(e)

# =========================
# 件数取得
# =========================
_, current_lines = get_file_data()

count = len(current_lines)

# =========================
# UI
# =========================
col1, col2 = st.columns([4, 1])

with col1:
    st.title("妖怪ウォッチ3 宝箱記録")

with col2:
    st.metric("記録数", count)

st.write("出たアイテムを押してください")

# =========================
# ボタン
# =========================
for category, grades in categories.items():

    st.subheader(category)

    cols = st.columns(4)

    for i, (grade, value) in enumerate(grades.items()):

        with cols[i]:

            if st.button(
                f"{grade}",
                key=f"{category}_{grade}"
            ):

                success = append_data(value)

                if success:
                    st.success(
                        f"{category} {grade} を記録"
                    )

                    st.rerun()

# =========================
# 削除ボタン
# =========================
st.divider()

if st.button("直近1件を削除"):

    delete_last()

    st.rerun()
