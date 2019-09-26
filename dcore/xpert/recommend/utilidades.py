import json
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


def append_arq(name, msg):
    arq = open(name, 'a')
    arq.write(msg + '\n')
    arq.close()


def load_json(path):
    try:     
        with open(path, 'r') as js:
            return json.load(js)
    except FileNotFoundError:
        return json.load('{}')
        
def flush_json(path, bundle):
    with open(path, 'w') as js:
        json.dump(bundle, js)


def create_chat(js, username, _id, chat_id, first_name):
    js[username] = json.loads('{}')
    js[username]['id'] = _id
    js[username]['chat_id'] = chat_id
    js[username]['first_name'] = first_name
    js[username]['new_msg'] = False
    js[username]['last_msg'] = json.loads('{}')
    js[username]['last_msg']['msg'] = ""
    js[username]['last_msg']['label'] = ""
    js[username]['last_msg']['pendings'] = False
