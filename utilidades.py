#Busca o primeiro número presenete em uma string
def number_on_string(txt):
    words = txt.split(' ')
    for i in range(0, len(words)):
        try:
            num = int(words[i])
            return num
        except:
            pass
    return None

def search_string(txt, target):
    return len(txt.upper().split(target.upper()) > 1)
