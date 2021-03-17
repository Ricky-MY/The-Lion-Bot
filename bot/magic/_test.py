import time

PLAYER_1 = ' 🔴 '
PLAYER_2 = ' 🔵 '
BLANK = ' ⚪ '

BASE_LINE = [[' ⚪ ', ' 🔵 ', ' ⚪ ', ' 🔴 ', ' ⚪ ', ' ⚪ ', ' ⚪ '],
             [' ⚪ ', ' 🔵 ', ' ⚪ ', ' ⚪ ', ' ⚪ ', ' ⚪ ', ' ⚪ '],
             [' ⚪ ', ' 🔵 ', ' ⚪ ', ' ⚪ ', ' ⚪ ', ' ⚪ ', ' ⚪ '],
             [' ⚪ ', ' 🔴 ', ' ⚪ ', ' ⚪ ', ' ⚪ ', ' ⚪ ', ' ⚪ '],
             [' ⚪ ', ' ⚪ ', ' ⚪ ', ' 🔴 ', ' ⚪ ', ' ⚪ ', ' ⚪ '],
             [' ⚪ ', ' 🔴 ', ' 🔴 ', ' 🔴 ', ' 🔴 ', ' ⚪ ', ' ⚪ ']]


def get_report(self, board) -> str:
        board = tuple([tuple(line) for line in board])
        vertical_board = tuple(zip(*board))
        for line in board:
            if PLAYER_1 in line or PLAYER_2 in line:
                start_on = None
                horizon_count = 1
                for character in line:
                    if character == BLANK:
                        continue
                    if character == PLAYER_1 and start_on == PLAYER_1:  
                        horizon_count += 1
                    elif character == PLAYER_1 and start_on == PLAYER_2:
                        horizon_count = 1

                    if character == PLAYER_2 and start_on == PLAYER_2:
                        horizon_count += 1
                    elif character == PLAYER_2 and start_on == PLAYER_1:
                        horizon_count = 1

                    if character == PLAYER_1:
                        start_on = PLAYER_1
                    elif character == PLAYER_2:
                        start_on = PLAYER_2

                    if horizon_count == 4:
                        return "win", start_on
        for verline in vertical_board:
            if PLAYER_1 in verline or PLAYER_2 in verline:
                vertical_count = 1
                ver_start_on = None
                for character in verline:
                    if character == BLANK:
                        continue
                    if character == PLAYER_1 and ver_start_on == PLAYER_1:  
                        vertical_count += 1
                    elif character == PLAYER_1 and ver_start_on == PLAYER_2:
                        vertical_count = 1

                    if character == PLAYER_2 and ver_start_on == PLAYER_2:
                        vertical_count += 1
                    elif character == PLAYER_2 and ver_start_on == PLAYER_1:
                        vertical_count = 1

                    if character == PLAYER_1:
                        ver_start_on = PLAYER_1
                    elif character == PLAYER_2:
                        ver_start_on = PLAYER_2
                    if vertical_count == 4:
                        return "win", ver_start_on
        return None, None

start = time.time()
print(get_report('2', BASE_LINE))
end = time.time()
print(end-start, ' seconds')