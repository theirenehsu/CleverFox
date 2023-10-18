import streamlit as st
import pandas as pd
from format import web_info, submit_button
from streamlit import session_state

web_info()
language = st.session_state.submit_revise_query
title_msg = {
    "EN": "🦊 Hello, Pf. David!",
    "TN": "🦊 您好！郝多章老師",
    "JP": "🦊 こんにちは！田中先生",
}
subheader_msg = {
    "EN": "Here is the writing record of the students",
    "TN": "以下是您指導的學生寫作紀錄",
    "JP": "以下はあなたの指導した学生の執筆記録です",
}
st.title(title_msg[language])
st.subheader(subheader_msg[language])
# table subtitle
title_name = {
    "EN": "Names",
    "TN": "姓名",
    "JP": "名前",
}
number_of_articles = {
    "EN": "number of articles",
    "TN": "文章數",
    "JP": "記事数",
}
number_of_grammar_error = {
    "EN": "Grammar errors in the latest article (number of errors)",
    "TN": "最新文章的文法改錯（錯誤次數）",
    "JP": "最新の記事の文法修正（誤り回数）",
}
number_of_word_level_up = {
    "EN": "Word Level Enhancement in the Latest Article (Number of Replacements)",
    "TN": "最新文章的文字等級提升（替換次數）",
    "JP": "最新記事の文言レベル向上（置き換え回数）",
}
number_of_rhetorical = {
    "EN": "Word Level Enhancement in the Latest Article (Number of Replacements)",
    "TN": "最新文章的轉折詞分析（出現次數）",
    "JP": "最新記事の転折句分析（出現回数）",
}
# table content
names_en = [
    'John',
    'Keren',
    'Ann',
    'Rina',
    'Willian',
    'Emily',
    'Michael',
    'Sarah',
    'Olivia',
    'James',
    'Benjamin',
    'Ava',
]
names_tn = [
    '許宗儒',
    '陳昱翔',
    '蔡宜庭',
    '張宇軒',
    '林子傑',
    '何思妤',
    '陳雅築',
    '張家豪',
    '柯宥辰',
    '藍佳穎',
    '古彥均',
    '莊庭瑜',
]
names_jp = [
    '田中太郎',
    '山田花子',
    '鈴木雅子',
    '伊藤太郎',
    '高橋真理',
    '中村太郎',
    '佐藤梨子',
    '木村雄一',
    '加藤麻美',
    '小林健太',
    '渡辺美佳',
    '松本隆二',
]
names = {
    "EN": names_en,
    "TN": names_tn,
    "JP": names_jp,
}

category = ['3', '4', '6', '2', '8', '3', '8', '4', '6', '1', '4', '8']
grammer = ['10', '12', '15', '13', '4', '20', '22', '12', '1', '10', '21', '16']
level = ['1', '13', '12', '28', '10', '9', '9', '7', '23', '27', '10', '11']
tran = ['6', '7', '5', '28', '7', '6', '4', '2', '6', '8', '5', '3']
data = {
    title_name[language]: names[language],
    number_of_articles[language]: category,
    number_of_grammar_error[language]: grammer,
    number_of_word_level_up[language]: level,
    number_of_rhetorical[language]: tran,
}
df = pd.DataFrame(data)

st.dataframe(data=df, width=1000)

# Feedback area
feedback = {
    "EN": "Feedback",
    "TN": "回饋區",
    "JP": "フィードバックエリア",
}
comment = st.button(feedback[language])
if "comment" not in st.session_state:
    st.session_state.comment = False
if comment:
    st.session_state.comment = not st.session_state.comment
if st.session_state.comment:
    msg = {
        "EN": "Hello, teacher! You can leave the feedback you want to give to the students here.",
        "TN": "老師好！此處可以留下您想給學生的回饋",
        "JP": "先生、こんにちは！こちらには生徒に提供したいフィードバックを残すことができます。",
    }
    st.markdown(msg[language])

    selection = {
        "EN": "##### Select a student",
        "TN": "##### 選擇學生",
        "JP": "##### 生徒を選択",
    }
    content = {
        "EN": "##### Content",
        "TN": "##### 回饋內容",
        "JP": "##### フィードバック内容",
    }
    submit = submit_button()
    notification = {
        "EN": "Submission succeeded.",
        "TN": "已送出",
        "JP": "送信完了",
    }
    st.selectbox(selection[language], names[language])

    st.text_input(content[language], '')
    feedback_button = st.button(submit[language])
    if feedback_button:
        st.toast(notification[language])
