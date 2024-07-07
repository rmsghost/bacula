import os

def comando():
    comando = 'ls'
    execute = os.system(comando)
    
    print (execute)

comando()
