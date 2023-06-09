def more_than_3500_tokens(texts):
    '''
    if there are more than > 700 words (3500 tokens): return True
    else: False
    :param text: Enter texts in a file
    :return: boolean
    '''

    words = texts.split()
    num_words = len(words)
    if num_words > 700:
        return True
    return False

