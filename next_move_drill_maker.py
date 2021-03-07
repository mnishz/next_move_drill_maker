# How to use: $ python3 next_move_drill_maker.py sfen_example

import sys
import urllib.parse

import Ayane.source.shogi.Ayane as ayane
import python_shogi.shogi as shogi

HANKAKU  = [ '1',  '2',  '3',  '4',  '5',  '6',  '7',  '8',  '9']
ZENKAKU  = ['１', '２', '３', '４', '５', '６', '７', '８', '９']
ALPHABET = [ 'a',  'b',  'c',  'd',  'e',  'f',  'g',  'h',  'i']
KANJI    = ['一', '二', '三', '四', '五', '六', '七', '八', '九']

def eval_sfen(sfen):

    time_to_think_ms = 2000
    bad_move_diff_criteria = 500
    bad_move_abs_criteria = 3000
    mate_criteria = 99950
    num_yomisuji = 3

    # 相手の応手が期待通りだったときに探索を改善する方法があるようなので、
    # 一つで解析するよりも二つで交互に解析したほうがいいのかもしれない
    usi = ayane.UsiEngine()
    usi.set_engine_options({
        "MultiPV": num_yomisuji  # 読み筋の数
    })
#     usi.debug_print = True
    usi.connect("YaneuraOu/source/YaneuraOu-by-gcc")

    start_str = "startpos moves"
    sfen_list = sfen[sfen.find(start_str) + len(start_str) + 1:].split()
    curr_sfen = start_str

    # -1: 先手 positive, 後手 negative
    #  1: 先手 negative, 後手 positive
    teban = -1

    prev_eval = 0
    bestmove = ""
    last_bestmove = ""

    board = shogi.Board()

    for i, move in enumerate(sfen_list):

        curr_sfen += " " + move

        # shortcut
#         if i < 40:
#             teban *= -1
#             board.push_usi(move)
#             continue

        usi.usi_position(curr_sfen)

        usi.usi_go_and_wait_bestmove("time 0 byoyomi " + str(time_to_think_ms))

        last_bestmove = bestmove
        bestmove = usi.think_result.bestmove

        # 読み筋
#         for candidate in range(num_yomisuji):
#             print(usi.think_result.pvs[candidate].to_string())

        curr_eval = usi.think_result.pvs[0].eval * teban

        ignore_bad_move = (curr_eval > bad_move_abs_criteria and prev_eval > bad_move_abs_criteria) or (curr_eval < -bad_move_abs_criteria and prev_eval < -bad_move_abs_criteria)

        text = ""

        if abs(curr_eval - prev_eval) > bad_move_diff_criteria and not ignore_bad_move:
            text += "悪手, "
        if abs(curr_eval) > mate_criteria:
            text += "{} 手詰め, ".format(100000 - abs(curr_eval))
        if abs(prev_eval) > mate_criteria and abs(curr_eval) < mate_criteria:  # 先手後手の評価が入れ替わった時の条件が怪しいかも
            text += "詰み逃し, "

        if text:
            print("{}: {} ({})".format(i + 1, curr_eval, text[:-2]))
        else:
            print("{}: {}".format(i + 1, curr_eval))

        if "悪手" in text and teban == -1:  # 先手での悪手のみを pick up
            url = "https://sfenreader.appspot.com/sfen?turn=off&sfen="
            url += urllib.parse.quote(board.sfen())
            last_move = str(board.peek())[2:4]
            last_move = last_move[0] + str(ord(last_move[1]) - ord('a') + 1)
            url += "&lm=" + last_move
            print(url)

            print("best move is " + last_bestmove + ", " + get_kif_move(last_bestmove, board))
#             break

        board.push_usi(move)

        prev_eval = curr_eval

        teban *= -1

    usi.disconnect()

def get_kif_move(move, board):

    # その到達地点に行ける同じ種類の駒が複数ある時の処理がない、右左上寄引

    if move[1] is '*':
        koma = shogi.PIECE_JAPANESE_SYMBOLS[shogi.PIECE_SYMBOLS.index(move[0].lower())]
    else:
        square = (9 - int(move[0])) + (ord(move[1]) - ord('a')) * 9
        koma = board.piece_at(square).japanese_symbol()

    kif = ZENKAKU[HANKAKU.index(move[2])]
    kif += KANJI[ALPHABET.index(move[3])]
    kif += koma

    if len(move) == 5 and move[4] is '+':
        kif += '成'

    if move[1] is '*':
        kif += '打'

    return kif

if __name__ == "__main__":

    args = sys.argv
    file_name = args[1]
    print("file_name: {}".format(file_name))

    with open(file_name, 'r') as f:
        sfen = f.read()
    print("sfen: {}".format(sfen))

    eval_sfen(sfen)
