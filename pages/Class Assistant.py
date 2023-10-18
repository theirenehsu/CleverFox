import openai
import streamlit as st
from streamlit_chat import message
from format import web_info
from streamlit import session_state

web_info()
if(st.session_state.submit_revise_query):
    language = st.session_state.submit_revise_query
else:
    language = "EN"

# initial state
question_related = '''Fake news can be defined as news containing false or misleading information that appears truthful.
Although fake news has long been in existence and this issue is as old as the news industry itself,
the Internet and social media have made creating and sharing fake news easier and faster than ever.
Consequently, people may be deceived by fake news, believing the content to be genuine without questioning the sources.
With so much fake news being spread every day, it is now more important than ever to understand where such news comes from and to question the news stories we read.
'''
ans_related = "Grammar"
response_tone = "Formal English Writing"
Word_limit = 50


# 預設問題：文法、單字、結構，老師可以填入有關課程prompt（可以點擊讓學生看）
def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Who are you?"},
            {"role": "assistant", "content": "I am your remote English Teacher Assistant"},
            {"role": "user", "content": "Introduce the system"},
            {
                "role": "assistant",
                "content": "We can automatic check you grammar and spelling, also list the error in a table below the modified article. There are test zones where you can find problems to start writing.",
            },
            {"role": "user", "content": f"Your answer should be related to {ans_related}"},
            {"role": "assistant", "content": f"Ok, I got it."},
            {"role": "user", "content": f"看到中文輸入時，請用中文回答我"},
            {"role": "assistant", "content": f"好的，我看到中文輸入時，一定會回答中文"},
            {"role": "user", "content": f"你是誰"},
            {"role": "assistant", "content": f"我是你的AI教學助教"},
            {"role": "user", "content": f"Plus是一個好的轉折語嗎？"},
            {"role": "assistant", "content": f"不是，正式英文中我們會使用其他字，如in addition to、furthermore等等"},
            {
                "role": "user",
                "content": f"Answer the question with {response_tone}tone within {Word_limit} words",
            },
            {"role": "assistant", "content": f"Ok, I got it."},
            {"role": "user", "content": f"{prompt}"},
        ],
        temperature=0.3,
        max_tokens=700,
    )
    return response['choices'][0]['message']['content']

title_msg = {
    "EN": "🦊 Hi！I am your AI teaching assistant💡",
    "TN": "🦊 嗨！我是你的AI教學助教💡",
    "JP": "🦊 こんにちは！私はあなたのAIティーチングアシスタントです💡"
}
##Showing setting button
st.title(title_msg[language])

input_key = st.secrets["api_key"]
openai.api_key = input_key
st.divider()

button_msg = {
    "EN": " ▶ Click to expand the teacher setting area ",
    "TN": " ▶ 點擊收放教師設定區 ",
    "JP": " ▶ クリックすると教師設定エリアが展開されます "
}

show_teacher = st.button(button_msg[language])

if "show_teacher" not in st.session_state:
    st.session_state.show_teacher = False
if show_teacher:
    st.session_state.show_teacher = not st.session_state.show_teacher
    st.session_state.something = ''

teacher_set = {
    "EN": "### Teacher Setting Area",
    "TN": "### 教師設定區",
    "JP": "### 教師設定エリア"
}
teacher_hi = {
    "EN": "Hello teacher! Please change the following settings to make the teaching assistant more suitable for your needs.",
    "TN": "老師好！請更改以下設定讓助教更符合您需求的助教",
    "JP": "こんにちは先生！ティーチングアシスタントをニーズに合わせてより適切なものにするために、次の設定を変更してください。"
}

if st.session_state.show_teacher:
    st.markdown(teacher_set[language])

    st.markdown(teacher_hi[language])
    col1, col2 = st.columns([2, 1])  # cut into two sections
    
    # left page：article
    with col1:
        set_1 = {
        "EN": "#### Teaching materials",
        "TN": "#### 教學素材",
        "JP": "#### 教材"
        }
        st.markdown(set_1[language])
        text = ''
        
        set_2 = {
        "EN": "You want students to ask more questions about the following course content",
        "TN": "您希望學生多多詢問有關以下課程內容的問題",
        "JP": "次のコース内容について学生にもっと質問してもらいたい"
        }
        # input raw article
        with st.expander('', expanded=True):
            question = st.text_area(set_2[language], question_related)

    with col2:
        set_3 = {
        "EN": "#### Focus on",
        "TN": "#### 著重面向",
        "JP": "#### 焦点を当てる"
        }
        set_4 = {
        "EN": "You would like the teaching assistant’s answer to focus on one of the following aspects",
        "TN": "您希望助教的回答著重在以下某個方面",
        "JP": "次のいずれかの側面に焦点を当てたティーチングアシスタントの回答を希望します。"
        }
        radio_1 = {
        "EN": "Words that are easy to confuse",
        "TN": "易混肴字詞",
        "JP": "混同しやすい言葉"
        }
        radio_2 = {
        "EN": "Grammar",
        "TN": "文法",
        "JP": "文法"
        }
        radio_3 = {
        "EN": "Vocabulary",
        "TN": "字彙",
        "JP": "語彙"
        }
        radio_4 = {
        "EN": "Article structure",
        "TN": "文章結構",
        "JP": "記事の構成"
        }
        st.markdown(set_3[language])
        st.markdown(set_4[language])
        ans_related = st.radio('', [radio_1[language], radio_2[language], radio_3[language], radio_4[language]])
        st.write(' ')

    word_c = {
        "EN": "#### word count",
        "TN": "#### 字數",
        "JP": "#### 単語数"
        }
    reply = {
        "EN": "Word limit for TA responses",
        "TN": "助教回覆的字數限制",
        "JP": "TA 応答の文字数制限"
        }
    col3, col4 = st.columns(2)
    with col3:
        st.markdown(word_c[language])
        Word_limit = st.text_input(reply[language], Word_limit)
    with col4:
        tone = {
        "EN": "#### intonation",
        "TN": "#### 語調",
        "JP": "#### イントネーション"
        }
        se_1 = {
        "EN": "You would like your TA’s responses to follow the following tone of voice",
        "TN": "您希望助教的回答符合下述語調",
        "JP": "TA の応答が次の口調に従ってほしいとします。"
        }
        se_2 = {
        "EN": "formal english writing",
        "TN": "正式英文寫作",
        "JP": "正式な英語の書き方"
        }
        se_3 = {
        "EN": "Formal English speaking",
        "TN": "正式英文口說",
        "JP": "フォーマルな英語を話す"
        }
        se_4 = {
        "EN": "Standard English usage",
        "TN": "標準英文使用",
        "JP": "標準的な英語の使用法"
        }
        se_5 = {
        "EN": "Professional English teachers",
        "TN": "專業的英文老師",
        "JP": "プロの英語教師"
        }
        se_6 = {
        "EN": "Native English speakers",
        "TN": "英文母語者",
        "JP": "英語ネイティブスピーカー"
        }
        st.markdown(tone[language])
        response_tone = st.selectbox(
            se_1[language], (se_2[language], se_3[language], se_4[language], se_5[language], se_6[language])
        )
    st.divider()


if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

## Clear input_text when submit
if 'something' not in st.session_state:
    st.session_state.something = ''


def submit():
    st.session_state.something = st.session_state.widget
    st.session_state.widget = ''

q1 = {
        "EN": "What do you want to know?",
        "TN": "你想了解什麼？",
        "JP": "何を知りたいですか"
        }
q0= {
        "EN": "Enter your question here",
        "TN": "在這裡輸入問題",
        "JP": "ここに質問を入力してください"
        }
st.text_input(q1[language], key="widget", placeholder=q0[language], on_change=submit)

q3 = {
        "EN": "Generate suggested questions",
        "TN": "產生建議問題",
        "JP": "提案された質問を生成する"
        }
if st.button(q3[language]):
    st.session_state.something = ''
    following_question = generate_response(
        f"Randomly generate three questions related to {question_related} within 10 words"
    )
    q4 = {
        "EN": "🦊 You can try asking:",
        "TN": "🦊 你可以試著問問：",
        "JP": "🦊 次のように質問してみてください。"
        }
    st.write(f"{q4[language]}\n{following_question}")

user_input = st.session_state.something

if user_input:
    output = generate_response(user_input)
    st.session_state['generated'].append(output)
    st.session_state['past'].append(user_input)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state["generated"][i], avatar_style="lorelei", key=str(i))
        message(st.session_state['past'][i], is_user=True, avatar_style="adventurer", key=str(i) + '_user')

# st.markdown(
# '''
# <style> 
# <img src="https://i.imgur.com/Qj5z2Du.png" alt="profile" draggable="false">
# <style>
# ''',
# unsafe_allow_html=True,
# )