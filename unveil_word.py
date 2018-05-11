word = 'Python'
# mask = len(word) * '*'
mask = 'P****n'

letter = 'y'



def unveil_word(answer, mask, letter):
    s = ""
    for i in range(len(answer)):
        word_letter = answer[i]
        mask_letter = mask[i]

        if mask_letter != '*':
            s += mask_letter
        elif letter == word_letter:
            s += word_letter
        else:
            s += '*'
    return s

print(unveil_word(word, mask, 'o'))
