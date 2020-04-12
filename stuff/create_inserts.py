"""
Для Друзей Школы
"""
import csv


def gsf():  # Givin School Friends
    f = open(r"d:\!SAVE\table\1.tsv", "r", encoding="utf-8")
    f1 = f.readlines()
    f1 = f1[1:]
    result = []
    for line in f1:
        # print(line)
        line2 = line.split("\t")
        # line2 = line.split(",")
        # print(line2)
        if line2[3] == "":
            telegram = "NULL"
        else:
            telegram = f"'{line2[3]}'"
        if line2[9] == "":
            until_date = "NULL"
        else:
            until_date = f"to_date('{line2[9]}', 'DD.MM.YYYY')"
        if len(line2[11]) <= 1:
            comment = "NULL"
        else:
            comment = f"'{line2[11]}'"
            comment = comment.replace('\r', ' ').replace('\n', ' ')
        result.append(f"INSERT INTO participants"
                      f"(last_name, first_name,"
                      f" fio,"
                      f" email, telegram, login,"
                      f" password,"
                      f" payment_date, number_of_days,"
                      f" deadline, until_date,"
                      f" comment, type)"
                      f" VALUES ('{line2[0].upper().strip()}', '{line2[1].upper().strip()}', "
                      f"'{(line2[0].upper() + ' ' + line2[1].upper()).strip()}',"
                      f" '{line2[2].lower().strip()}', {telegram.lower().strip()}, '{line2[4].lower().strip()}',"
                      f" '{line2[5].strip()}',"
                      f" to_date('{line2[6]}', 'DD.MM.YYYY'), {line2[7]},"
                      f" to_date('{line2[8]}', 'DD.MM.YYYY'), {until_date}, "
                      f"{comment.strip()}, '{line2[12].strip()}');")
    # for x in result:
    #    print(x)
    with open(r'd:\!SAVE\table\inserts1.sql', 'w') as filehandle:
        filehandle.writelines("%s\n" % place for place in result)


def tm():  # Team Members
    f = open(r"c:\!SAVE\list2.csv", "r", encoding="utf-8")
    f1 = f.readlines()
    result = []
    for line in f1:
        line = line.split(";")
        # print(line)
        fio = line[0].split(" ")
        last_name = fio[0].upper()
        first_name = fio[1].upper()
        email = line[1].lower()
        password = line[2]
        if line[3] == "\n":
            telegram = "NULL"
        else:
            telegram = line[3].lower().replace("\n", "")
        result.append(f"INSERT INTO public.team_members(last_name, first_name, email, password, telegram) "
                      f"VALUES ('{last_name}', '{first_name}', '{email}', '{password}', '{telegram}');")
    # for x in result:
    #     print(x)
    with open(r'c:\!SAVE\inserts1.sql', 'w') as file:
        file.writelines("%s\n" % place for place in result)


def tm2(file):  # Team Members
    result = []
    with open(file, "r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        for line in reader:
            # print(line)
            # ['Агафонова Ксения', 'Москва', '@Ksenya_Agafonova', 'жен', 'Сентябрята']
            fio = line[0].split(" ")
            last_name = fio[0].upper()
            first_name = fio[1].upper()
            filial = line[1]
            telegram = line[2].lower()
            if line[3] == "муж":
                sex = True
            else:
                sex = False
            retrit = line[4]
            result.append(f"INSERT INTO public.team_members(last_name, first_name, sex, filial, retrit, telegram) "
                          f"VALUES ('{last_name}', '{first_name}', {sex}, '{filial}', '{retrit}', '{telegram}');")
    # for x in result:
    #     print(x)
    with open(r'c:\!SAVE\inserts1.sql', 'w') as file:
        file.writelines("%s\n" % place for place in result)


def zoom_member(file):  # Join zoom conference and team member
    result = []
    with open(file, "r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for line in reader:
            # print(line)
            # ['MYROSLAVA XXXXX', 'xxx@gmail.com']
            zoom_name = line[0]
            zoom_name_norm = line[0].strip().lower()
            zoom_email = line[1].strip().lower()
            result.append(f"INSERT INTO public.zoom_join_zoom_and_members(zoom_name, zoom_name_norm, zoom_email, "
                          f"member_id) VALUES ('{zoom_name}', '{zoom_name_norm}', '{zoom_email}', 7777);")
    # for x in result:
    #     print(x)
    with open(r'c:\!SAVE\inserts1.sql', 'w') as file:
        file.writelines("%s\n" % place for place in result)

if __name__ == "__main__":
    file_name = r"c:\!SAVE\data-1586684131740.txt"
    # gsf()
    # tm2(file_name)
    zoom_member(file_name)
