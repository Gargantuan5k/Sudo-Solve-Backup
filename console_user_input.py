from os import name as os_name
from os import system

import board_prettyprint
from config_validity_checker import fullboard_isvalid as board_isvalid

__SMALLER_TITLE_FILE = "assets/ascii_smaller_title.txt"


def __cls():
    system("cls" if os_name == "nt" else "clear")


def __print_smaller_title():
    with open(__SMALLER_TITLE_FILE, encoding="utf-8") as stf:
        print(stf.read())


# Calculate the number of lines to move the cursor UP by
def calc_up_num(row_idx: int, board_repr: list[list[str]]):
    """
    @returns str: Escape Sequence to move the cursor UP by some number of lines
    """

    up_num = 0
    if 0 <= row_idx < 3:
        up_num = (len(board_repr) - row_idx) + 2  # skip both horz. lns
    elif 3 <= row_idx < 6:
        up_num = (len(board_repr) - row_idx) + 1  # skip only 2nd horz. ln
    elif row_idx >= 6:
        up_num = len(board_repr) - row_idx  # no horizontal lns to skip
    escape_seq = f"\x1B[{up_num}A\x1B[25C"  # move cursor UP by up_num lns

    return escape_seq


def get_input() -> list[list[int]]:
    """
    @returns list[list[int]]: Board configuration to be solved,
    as per user input
    """

    board_repr = [
        [" ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " "],
    ]

    row_idx = 0
    delete = False

    while row_idx < len(board_repr):
        __cls()
        row = board_repr[row_idx]

        if not delete:
            col_idx = 0
        
        delete = False
        while col_idx < len(row):
            board_repr[row_idx][col_idx] = "_"
            board_str = board_prettyprint.prettyprint(board_repr, ret=True)

            escape_seq = calc_up_num(row_idx, board_repr)

            while True:
                if delete:
                    delete = False
                    break

                __print_smaller_title()
                input_num = input(
                    board_str + escape_seq + "<------ [ ] INTEGER FROM 1-9. 0 or No Input for an "
                    "empty square.\x1B[55D"
                )
                try:
                    int(input_num)
                except ValueError:
                    if input_num != 'd':
                        input_num = "0"

                if input_num == "0":
                    input_num = " "

                elif input_num != 'd' and 1 <= int(input_num) <= 9:
                    pass

                elif input_num == 'd':
                    delete = True
                    board_repr[row_idx][col_idx] = " "
                    if col_idx > 0:
                        col_idx -= 1
                        break
                    elif col_idx == 0 and row_idx > 0:
                        col_idx = 8
                        row_idx -= 1
                        break
                    elif row_idx == 0 and col_idx != 0:
                        delete = False
                        __cls()
                        col_idx += 1
                        continue
                    else:
                        input_num = ' '
                    

                else:
                    __cls()
                    continue

                cp_board_repr = board_repr.copy()
                cp_board_repr[row_idx][col_idx] = int(input_num) if input_num != " " else " "
                __cls()

                # Check the validity of entered board config. in current state
                valid, row_inv, col_inv, box_inv = board_isvalid(cp_board_repr)
                if valid:
                    break
                else:
                    if row_inv:
                        repeat_location = "row"
                    elif col_inv:
                        repeat_location = "col"
                    elif box_inv:
                        repeat_location = "3x3 box"

                    print(
                        f"Invalid board configuration! '{input_num}' has been "
                        f"repeated in the same {repeat_location}"
                    )

            if delete:
                break

            board_repr[row_idx][col_idx] = cp_board_repr[row_idx][
                col_idx
            ]
            __cls()

            col_idx += 1

        if delete:
            continue
        row_idx += 1

    print(
        f"You have entered the following board configuration:\n"
        f"{board_prettyprint.prettyprint(board_repr, ret=True)}"
    )

    for row in board_repr:
        for c_idx, item in enumerate(row):
            if item == " ":
                row[c_idx] = 0

    return board_repr


if __name__ == "__main__":
    test_uin = get_input()
