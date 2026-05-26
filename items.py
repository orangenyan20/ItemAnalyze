import streamlit as st
from github import Github
from datetime import datetime

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
# アイテム定義
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
# データ書き込み関数
# =========================
def append_to_github(value):
    try:
        # 現在のファイル取得
        file = repo.get_contents(FILE_PATH, ref=BRANCH)
        current_content = file.decoded_content.decode("utf-8")

        # 追記内容
        new_line = f"{value}\n"
        updated_content = current_content + new_line

        # GitHub更新
        repo.update_file(
            path=FILE_PATH,
            message=f"Add data: {value}",
            content=updated_content,
            sha=file.sha,
            branch=BRANCH
        )

        return True

    except Exception as e:
        st.error(f"エラー: {e}")
        return False

# =========================
# UI
# =========================
st.title("妖怪ウォッチ3 宝箱データ収集")

st.write("出たアイテムのジャンルとグレードを押してください")

for category, grades in categories.items():

    st.subheader(category)

    cols = st.columns(4)

    for i, (grade, value) in enumerate(grades.items()):

        with cols[i]:
            if st.button(f"{grade}", key=f"{category}_{grade}"):

                success = append_to_github(value)

                if success:
                    st.success(f"{category} - {grade} を記録しました ({value})")