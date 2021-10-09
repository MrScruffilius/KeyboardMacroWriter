# TODO in README schreiben welche module verwendet wurden
# TODO beispielprogramme in README
# TODO checken ob auf anderen rechnern python auch ausführbar ist
# TODO Space notwendigkeit abschaffen
# TODO help befehl abändern
# TODO lexikon hinzufügen
# TODO edge cases abfangen


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
        elif temp[0].lower() == "t>":
            f.write("\tpa.typewrite('" + liste[i][3:] + "')\n")
        elif temp[0].lower() == "f>":
            # adds flag and line to dictionary
            flag_dict[temp[1]] = i
        elif temp[0].lower() == "jmp>":
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
        elif temp[0].lower() == "w>":
            # adds flag and line to dictionary
            f.write("\ttime.sleep(" + str((int(temp[1])/1000)) + ")\n")
        elif temp.__sizeof__() > 1:
            hk_string = "'" + temp[0].lower() + "'"
            counter = 1
            while counter < len(temp):
                hk_string = hk_string.__add__(", '" + temp[counter].lower() + "'")
                counter += 1
            f.write("\tpa.hotkey(" + hk_string + ")\n")
        else:
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
