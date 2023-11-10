import re

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
        print(return_data[2])

line = '{+distressing.+} [-Starting now, conserve water whenever possible, improve education, and cherish our Mother Earth. I hope for a better world.-]'

print_double_space(line)
