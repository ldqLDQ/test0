from stockfish import Stockfish
from pwn import *
context.log_level = 'debug'
p = remote("138.91.120.132", 8083)

ai = Stockfish("./stockfish_20090216_x64.exe")


def fromUciToNum(uci):
    print(f'[+] uci : {uci}')
    up = uci[:2]
    up = (ord(up[0])-ord('a')) + (int(up[1])-1)*8
    down = uci[2:]
    down = (ord(down[0])-ord('a')) + (int(down[1])-1)*8
    return (up, down)


# def fromNumToUci(num):
#     up = chr((num[0] % 8) + ord('a')) + str(num[0]//8+1)
#     down = chr((num[1] % 8) + ord('a')) + str(num[1]//8+1)
#     uci = up+down
#     return uci


def getNextMove(fen):
    ai.set_fen_position(fen)
    uci = ai.get_best_move()
    return fromUciToNum(uci)


def getFen(board):
    fen = '/'.join(board).replace('........', '8').replace('.......', '7').replace('......', '6').replace(
        '.....', '5').replace('....', '4').replace('...', '3').replace('..', '2').replace('.', '1')
    fen+=' w - - 0 1'
    return fen


fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1"
p.recvuntil(b"Plz input your next step like '1 18'")
while True:
    (up, down) = getNextMove(fen)
    p.sendline(f'{up} {down}'.encode())
    p.recvuntil(b"Plz continue")
    board_raw = p.recvuntil(b'Plz').decode(
    )[:-3].strip().replace('\r', '').replace(' ', '')
    board_raw = board_raw.split('\n')
    fen = getFen(board_raw)
    print(f'[+] {fen}')
    p.recvuntil("'1 18'")
p.interactive()
