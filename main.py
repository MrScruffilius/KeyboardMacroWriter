# TODO beispielprogramme in README
# TODO checken ob auf anderen rechnern python auch ausführbar ist
# TODO lexikon hinzufügen
# TODO edge cases abfangen

lexikon = ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome',
'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
'command', 'option', 'optionleft', 'optionright']
# interpretiert die file.txt und macht daraus eine .py und dann eine .exe
def file_interpreter(file_name):
    file_name = str(file_name)
    orig_file_name = file_name
    file_name = file_name.__add__(".txt")

    try:
        readin = open(file_name, "rt")
    except:
        print("ERROR: No such file")
        return
    liste = readin.readlines()

    for i in range(len(liste)):
        liste[i] = liste[i].replace('\n', '')

    f = open(orig_file_name + ".py", "w")
    f.write("import time\n")
    f.write("import pyautogui as pa\n")
    f.write("if __name__=='__main__':\n")
    # text muss mit tab davor geschrieben werden

    flag_dict = dict()
    jump_dict = dict()
    i = 0
    while i < len(liste):
        temp = liste[i].split(' ', 10000)
        if temp[0] == "//":
            pass
        elif temp[0].lower() == "t>"or temp[0][0:2].lower()=="t>":
            if temp[0].lower() != "t>":
                f.write("\tpa.typewrite('" + liste[i][2:] + "')\n")
            else:
                f.write("\tpa.typewrite('" + liste[i][3:] + "')\n")
        elif temp[0].lower() == "f>" or temp[0][0:2].lower()=="f>":
            if temp[0].lower()!="f>":
                flag_dict[temp[0][2:]] = i
            # adds flag and line to dictionary
            else:
                flag_dict[temp[1]] = i
        elif temp[0].lower() == "jmp>" or temp[0][0:4].lower()=="t>":
            if temp[0].lower()!="t>":
                if int(temp[1]) < 1:
                    continue
                if i in jump_dict:
                    if jump_dict[i] >= 1:
                        jump_dict[i] -= 1;
                        i = flag_dict[temp[0][4:]]
                    else:
                        jump_dict.pop(i)
                else:
                    jump_dict[i] = int(temp[1])

                    jump_dict[i] -= 1;
                    if jump_dict[i] < 1:
                        jump_dict.pop(i)
                    i = flag_dict[temp[0][4:]]
            else:
                if int(temp[2]) < 1:
                    continue
                if i in jump_dict:
                    if jump_dict[i] >= 1:
                        jump_dict[i] -= 1;
                        i = flag_dict[temp[1]]
                    else:
                        jump_dict.pop(i)
                else:
                    jump_dict[i] = int(temp[2])

                    jump_dict[i] -= 1;
                    if jump_dict[i] < 1:
                        jump_dict.pop(i)
                    i = flag_dict[temp[1]]
        elif temp[0].lower() == "w>" or temp[0][0:2].lower()=="w>":
            if temp[0].lower()!="w>":
                f.write("\ttime.sleep(" + str((int(temp[0][2:]) / 1000)) + ")\n")
            # adds flag and line to dictionary
            else:
                f.write("\ttime.sleep(" + str((int(temp[1]) / 1000)) + ")\n")

        elif temp.__sizeof__() > 1:
            for k in range(len(temp)):
                if temp[k].lower() not in lexikon:
                    print("Error: No such key -> "+temp[k])
                    return
            hk_string = "'" + temp[0].lower() + "'"
            counter = 1
            while counter < len(temp):
                hk_string = hk_string.__add__(", '" + temp[counter].lower() + "'")
                counter += 1
            f.write("\tpa.hotkey(" + hk_string + ")\n")
        else:
            if temp[0].lower() not in lexikon:
                print("Error: No such key -> " + temp[0].lower())
                return
            f.write("\tpa.press('" + temp[0].lower() + "')\n")
        i += 1
    f.close()
    readin.close()
    print("Build " + orig_file_name + ".py successfull")


def print_help():
    print("mac <file_name>  ")
    print(" - add the correct name of the file without ")
    print("   the .txt-ending to translate it")
    print("help")
    print(" - ...")


if __name__ == '__main__':
    print("")
    print(">-{ WELCOME TO THE MACRO-WRITER }-<")
    print("")
    print("write -> help <- to learn more")
    while True:
        inpu = input("\n")
        inpu = inpu.replace(' ', '')
        inpu = inpu.lower()
        if inpu == "help":
            print_help()
        elif inpu[0:3] == "mac":
            if inpu.__sizeof__() > 1:
                file_interpreter(inpu[3:])
