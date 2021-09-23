import string 
from random import randint

def createid():
    chars=string.printable[:62]
    id=''
    for i in range(6):
       char = chars[randint(0,61)]
       id=id+char 
    return id

