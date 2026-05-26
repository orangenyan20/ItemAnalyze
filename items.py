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
# ジャンル設定
# =========================
categories = {
    "食べ物": 100,
    "漢方": 200,
    "経験値玉": 300,
    "こけし": 400,
    "コイン": 500,
    "バトルアイテム": 600,
    "その他": 700
}

grades = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4
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
            f"Delete {deleted}",
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
# UI上部
# =========================
top1, top2 = st.columns([4, 1])

with top1:
    st.title("妖怪ウォッチ3 宝箱記録")

with top2:
    st.metric("記録数", count)

st.write("数字ボタンを押して記録")

st.divider()

# =========================
# ボタンUI
# =========================
for category_name, category_base in categories.items():

    st.subheader(category_name)

    cols = st.columns(4)

    for i, (grade_name, grade_value) in enumerate(grades.items()):

        value = category_base + grade_value

        with cols[i]:

            if st.button(
                grade_name,
                key=f"{category_name}_{grade_name}"
            ):

                success = append_data(value)

                if success:

                    st.success(
                        f"{value} を記録"
                    )

                    st.rerun()

# =========================
# 削除ボタン
# =========================
st.divider()

if st.button("直近1件を削除"):

    delete_last()

    st.rerun()
