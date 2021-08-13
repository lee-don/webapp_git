import json

from MyQR import myqr
import os
import shutil
from tools.common.cm import get_a_uuid



def encoding_words(words):
    return words.encode().decode("unicode_escape")

def get_qrcode(words):
    words1 = json.dumps(words)
    words1 = words1.replace('\"','\'')
    words1 = words1.strip('\'')
    myqr.run(words=words1,colorized = True)
    src = 'qrcode.png'
    file = str(get_a_uuid())
    file = os.path.join('.', 'tmp', file+'.png')
    os.rename(src,file)
    return os.path.abspath(file)

def remove_tmp():
    d = os.path.join('.', 'tmp')
    d = os.path.abspath(d)
    try:
        shutil.rmtree(d)
        os.mkdir(d)
        return True
    except:
        os.mkdir(d)
        remove_tmp()


if __name__ == '__main__':
    print(remove_tmp())
    x = get_qrcode('中文ss')
    print(x)




