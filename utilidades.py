
def number_on_string(txt):
    words = txt.split(' ')
    num = -1
    for i in range(0, len(words)):
        try:
            num = int(words[i])
            return num
        except:
            num = -1
    return -1

def search_string(txt, target):
    return len(txt.upper().split(target.upper()) > 1)
