import re
import subprocess
import streamlit as st
import os, sys

# import pdfkit


def web_info():
    # Set the page title
    st.set_page_config(page_title='CleverFox', page_icon='🦊', layout='wide')
    # Set format: logo, result, divider inside the result
    st.markdown(
        '''
        <style>
        [data-testid="stSidebarNav"] {
                    background-image: url(https://i.imgur.com/Qj5z2Du.png);
                    background-repeat: no-repeat;
                    background-size: 30%;
                    background-position:20px 100px;
                    padding-top: 120px;
        }
        [class="fixed"] {
            width:750px
            min-width:750px;
            max-width:750px;
            overflow-x: scroll;
            align-items: center;
            white-space: pre;
            padding-right: 1rem;
            padding-left: 1rem;
            margin-bottom: 0.5rem;
            background-color: rgb(240, 242, 246);
            border-radius: 0.5rem;
            color: rgb(49, 51, 63);
        }
        hr {
            margin: 0.2em 0px;
            padding: 0px;
            color: inherit;
            background-color: transparent;
            border-top: none;
            border-right: none;
            border-left: none;
            border-image: initial;
            border-bottom: 1px solid rgba(49, 51, 63, 0.2);
        }
        </style>
        ''',
        unsafe_allow_html=True,
    )


def submit_button():
    button = {
        "EN": "submit",
        "TN": "送出",
        "JP": "送信",
    }
    return button


def show_result():
    result = {
        "EN": "**Result**",
        "TN": "**批改結果**",
        "JP": "**採点結果**",
    }
    return result


def match_tokens_from_errant(original, correction):
    # Save the original and corrected article
    with open('original.txt', 'w') as file:
        file.write(original)
    with open('correction.txt', 'w') as file:
        file.write(correction)

    # 定義要執行的 errant_parallel 命令
    '''
    S: original sentence(one line)
    A start_token end_token: edit annotation
    '''
    command = "errant_parallel -orig original.txt -cor correction.txt -out diff.txt"
    # 執行命令並將結果輸出到變量中
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(output)
        print("errant_parallel 命令成功執行")
    except subprocess.CalledProcessError as e:
        print(f"命令執行出錯：{e}")

    # 讀出 errant 比較結果
    errant_tag = []
    with open('diff.txt', 'r') as fout:
        lines = fout.readlines()
        for line in range(1, len(lines)):
            errant_tag.append(lines[line].strip())
    # print("errant_tag:\n", errant_tag)

    # 將結果的格式切割
    diff_tag = []  # [['A', start, end, *, corrected_word, *, *, *]]
    for line in errant_tag:
        parts = line.split('|||')
        if len(parts) > 1:
            item = parts[0].split() + parts[1:]
            diff_tag.append(item)
    # print("diff_tag:\n", diff_tag)

    # 取出修改後的詞
    corrected_essay = []
    words = original.split()
    for i in range(len(words)):
        corrected_essay.append(words[i])
    # print("corrected_string:\n", corrected_essay)

    for i in range(len(diff_tag)):
        a = int(diff_tag[i][1])  # 錯誤開始位置
        b = int(diff_tag[i][2])  # 錯誤結束位置
        cor_w = diff_tag[i][4]  # 修正的結果
        sli = " ".join(corrected_essay[a:b])
        if a < b:
            # x = find_nth_word(text, b)
            if cor_w == "":
                revision = "[-" + sli + "-]"
            else:
                revision = "{+" + cor_w + "+} " + "[-" + sli + "-]"
            # corrected_string[a:(b - 1)] = ""
            for x in range(a, b):
                # st.write(a, b, corrected_essay)
                corrected_essay[x] = ""
            corrected_essay[b - 1] = revision
        elif a == b:
            # x = find_nth_word(text, b)
            if cor_w == "":
                revision = "[-" + sli + "-]"
            else:
                revision = corrected_essay[b - 1] + " {+" + cor_w + "+}"
            # temp_word[a:(b - 1)] = ""
            for x in range(a, b):
                corrected_essay[x] = ""
            corrected_essay[b - 1] = revision
    return " ".join(corrected_essay)


def diff_tokens(fixed_sentence):
    '''
    切字，包含以下六種形式
    {+any char} [-any char]
    [-any char]
    {+any char}
    word\d\s
    :
    \d
    \w
    '''
    return re.findall(
        r'\{\+[^}]+?\}\s\[\-[^]]+?\]|\[\-[^]]+?\]|\{\+[^}]+?\}|[^a-zA-Z\d\s:]|:|\d+|\w+|\n',
        fixed_sentence,
    )


# Generate double-spaced sentences with edits
def get_a_line(tokens, limit=68):
    '''
    產生以60個字為一行的文章with double-space sentences
    '''
    # format: color
    original_html_start = '<span style="color:grey;">'  # color=blue
    original_html_end = '</span>'
    edit_html_start = '<span style="color:red;">'  # color=red
    edit_html_end = '</span>'

    line1, line2, line_pure_text = '', '', ''  # original sentence with color format, edit sentence with color format, original sentence
    skip = False  # {++} insert occurs

    for i, token in enumerate(tokens):  # i: position, token: one word
        if skip:
            skip = False
            continue

        text_original, text_edit, text, word_len = '', '', '', 0
        # If token is "{++} [--]"
        if token.startswith('{+') and token.endswith('-]'):
            text_edit, text_original = token[2:-2].split('+} [-')
            # Compute len
            word_len = max(len(text_original), len(text_edit))
            # Formatiing
            text = text_original + (' ' * (word_len - len(text_original)))
            text_original = original_html_start + text_original + original_html_end + (' ' * (word_len - len(text_original)))
            text_edit = edit_html_start + text_edit + edit_html_end + (' ' * (word_len - len(text_edit)))

        # If token is "[--]" then change color
        elif token.startswith('[-'):
            text_original = token[2:-2]
            # Compute len
            word_len = len(text_original)
            # Formatiing
            text = text_original
            text_original = original_html_start + token[2:-2] + original_html_end
            text_edit = ' ' * word_len

        # If token is "{++}" then insert
        elif token.startswith('{+'):
            skip = True
            text_edit = token[2:-2]
            text_next = ''
            # Check if current token is not the last word
            try:
                text_next = tokens[i + 1]
            except:  # if token is the last word
                text_next = ' ' * len(text_edit)
            # If next word is "{++} [--]"
            if text_next.startswith('{+') and text_next.endswith('-]'):
                text_edit_2, text_original_2 = text_next[2:-2].split('+} [-')
                text_next = text_edit_2 if len(text_edit_2) > len(text_original_2) else text_original_2
                # Compute len
                word_len = max(len(text_edit_2), len(text_original_2))
                # Formatting
                text = (' ' * (len(text_edit) + 3)) + text_original_2 + (' ' * (word_len - len(text_original_2)))
                text_original = (' ' * (len(text_edit) + 3)) + original_html_start + text_original_2 + original_html_end + (' ' * (word_len - len(text_original_2)))
                text_edit = edit_html_start + '^ ' + text_edit + edit_html_end + ' ' + edit_html_start + text_edit_2 + edit_html_end + (' ' * (word_len - len(text_edit_2)))
            else:
                # Compute len
                word_len = max(len(text_edit), len(text_next))
                # Formatiing
                text_original = (' ' * (word_len - len(text_next) + 2)) + text_next
                text = text_original
                text_edit = edit_html_start + '^ ' + text_edit + edit_html_end + (' ' * (word_len - len(text_edit)))

        # If token is alpha
        elif token.isalpha():
            # Compute len
            word_len = len(token)
            # Formatiing
            text_original = token
            text = text_original
            text_edit = ' ' * word_len
        # If token is punctuation
        else:
            if token == '\n':
                blank = ' ' * (limit - len(line_pure_text))
                # print('len:[\n] ', len(line_pure_text), len(blank), len(line_pure_text) + len(blank))
                return [line1 + blank, line2 + blank, [t for t in tokens[i + 1 :]]]

            # Compute len
            word_len = len(token)
            # Add token to line
            line1 += token
            line_pure_text = line_pure_text + token
            line2 += ' ' * (word_len)

            if i == len(tokens) - 1:
                blank = ' ' * (limit - len(line_pure_text))
                # print('len:[pu] ', len(line_pure_text), len(blank), len(line_pure_text) + len(blank))
                return [line1 + blank, line2 + blank, [t for t in tokens[i + 1 :]]]
            continue

        # Add token to line if not out of limit
        token_len = len(tokens)
        if (i == 0 and i == len(tokens) - 1):
            line1 += ' ' + text_original if len(line_pure_text) != 0 else text_original
            line2 += ' ' + text_edit if len(line_pure_text) != 0 else text_edit
            line_pure_text += ' ' + text if len(line_pure_text) != 0 else text
            blank = ' ' * (limit - len(line_pure_text))
            print("i == 0, tokens len: ", token_len)
            return [line1 + blank, line2 + blank, []]
        elif len(line_pure_text) + word_len <= limit and (i != len(tokens) - 1):
            line1 += ' ' + text_original if len(line_pure_text) != 0 else text_original
            line2 += ' ' + text_edit if len(line_pure_text) != 0 else text_edit
            line_pure_text += ' ' + text if len(line_pure_text) != 0 else text
        else:
            blank = ' ' * (limit - len(line_pure_text))
            # print('len:[ou] ', len(line_pure_text), len(blank), len(line_pure_text) + len(blank))
            return [line1 + blank, line2 + blank, [t for t in tokens[i:]]]


def print_double_space(fixed_sentence):
    printed_lines = """"""
    sent_tokens = diff_tokens(fixed_sentence)
    while sent_tokens:
        return_data = get_a_line(sent_tokens)
        # lines = [return_data[0].replace(' ', '&nbsp;'), return_data[1].replace(' ', '&nbsp;')]
        printed_lines += return_data[0] + '<br>' + return_data[1] + '<br><hr class="dashed">'
        sent_tokens = return_data[2]
        # print(return_data[2])
    st.markdown('<div class="fixed">' + printed_lines + '</div>', unsafe_allow_html=True)


def delete_previous_revised_essay():
    if os.path.exists("original.txt"):
        os.remove("original.txt")
        st.write("remove original")
    if os.path.exists("correction.txt"):
        os.remove("correction.txt")
        st.write("remove correction.txt")
        # print("removed correction")
    if os.path.exists("diff.txt"):
        os.remove("diff.txt")
        st.write("reomve diff")


def download_pdf(result):
    format1 = """
    <html>
      <head>
        <meta name="pdfkit-page-size" content="Legal"/>
      </head>
      <style>
        [class="fixed"] {
            font-family: Courier New;
            width:750px
            min-width:750px;
            max-width:750px;
            overflow-x: scroll;
            align-items: center;
            white-space: pre;
            padding-right: 1rem;
            padding-left: 1rem;
            margin-bottom: 0.5rem;
            background-color: rgb(240, 242, 246);
            border-radius: 0.5rem;
            color: rgb(49, 51, 63);
        }
        hr {
            margin: 0.2em 0px;
            padding: 0px;
            color: inherit;
            background-color: transparent;
            border-top: none;
            border-right: none;
            border-left: none;
            border-image: initial;
            border-bottom: 1px solid rgba(49, 51, 63, 0.2);
        }
    </style>
    Revise Result
    <div class="fixed">
    """
    format2 = """
    </div>
    </html>
    """

    # result = str(format1) + str(result) + str(format2)
    # st.write(result, unsafe_allow_html=True)

    # left, right = st.columns(2)
    # left.button('Dowload Result', on_click=False)
    # if st.session_state.click:
    #     # Configuring pdfkit to point to our installation of wkhtmltopdf
    #     config = pdfkit.configuration(wkhtmltopdf='../wkhtmltopdf/bin/wkhtmltopdf.exe')

    #     # Storing string to pdf file
    #     pdfkit.from_string(result, 'corrected.pdf')

    #     # Messenge
    #     left.write('Result was downloaded!')
