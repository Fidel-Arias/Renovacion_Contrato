import poplib
import os

# datos para identificación
usuario = 'fr06arias16@gmail.com'                # usuario para Gmail
password = os.environ['PASSWORD']                      # contraseña para Gmail

M = poplib.POP3_SSL('pop.gmail.com', '995')
is_body = False
M.user(usuario)
M.pass_(password)
numMessages = len(M.list()[1])
for i in range(numMessages):
    for j in M.retr(i+1)[1]:
        decode_line = j.decode('utf-8')
        if is_body:
            print(decode_line)
        if decode_line == '':
            is_body = True
M.quit()