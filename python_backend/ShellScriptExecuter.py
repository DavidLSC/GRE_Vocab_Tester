import os


def executeScript():
    shell_script = open("move_GRE_Vocab_List.txt", "r")
    script_str = ""
    for i in shell_script:
        script_str += i

    exit_code = os.system(script_str)

    print()
