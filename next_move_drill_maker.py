# How to use: $ python3 next_move_drill_maker.py sfen_example

import sys
import Ayane.source.shogi.Ayane as ayane

def eval_sfen(sfen):

    time_to_think_ms = 2000
    bad_move_diff_criteria = 500
    bad_move_abs_criteria = 3000
    mate_criteria = 99950

    # 相手の応手が期待通りだったときに探索を改善する方法があるようなので、
    # 一つで解析するよりも二つで交互に解析したほうがいいのかもしれない
    usi = ayane.UsiEngine()
#     usi.debug_print = True
    usi.connect("YaneuraOu/source/YaneuraOu-by-gcc")

    start_str = "startpos moves"
    sfen_list = sfen[sfen.find(start_str) + len(start_str) + 1:].split()
    curr_sfen = start_str

    # -1: 先手 positive, 後手 negative
    #  1: 先手 negative, 後手 positive
    teban = -1

    prev_eval = 0

    for i, sashite in enumerate(sfen_list):

        curr_sfen += " " + sashite

#         if i < 115:
#             teban *= -1
#             continue

        usi.usi_position(curr_sfen)

        usi.usi_go_and_wait_bestmove("time 0 byoyomi " + str(time_to_think_ms))

        bestmove = usi.think_result.bestmove

        curr_eval = usi.think_result.pvs[0].eval * teban

        ignore_bad_move = (curr_eval > bad_move_abs_criteria and prev_eval > bad_move_abs_criteria) or (curr_eval < -bad_move_abs_criteria and prev_eval < -bad_move_abs_criteria)

        text = ""

        if abs(curr_eval - prev_eval) > bad_move_diff_criteria and not ignore_bad_move:
            text += "悪手, "
        if abs(curr_eval) > mate_criteria:
            text += "{} 手詰め, ".format(100000 - abs(curr_eval))
        if abs(prev_eval) > mate_criteria and abs(curr_eval) < mate_criteria: # 先手後手の評価が入れ替わった時の条件が怪しいかも
            text += "詰み逃し, "

        if text:
            print('{}: {} ({})'.format(i + 1, curr_eval, text[:-2]))
        else:
            print('{}: {}'.format(i + 1, curr_eval))

#         print(bestmove)

        prev_eval = curr_eval

        teban *= -1

    usi.disconnect()

if __name__ == "__main__":

    args = sys.argv
    file_name = args[1]
    print("file_name: {}".format(file_name))

    with open(file_name, 'r') as f:
        sfen = f.read()
    print("sfen: {}".format(sfen))

    eval_sfen(sfen)