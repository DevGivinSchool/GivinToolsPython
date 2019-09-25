def main():
    f = open(r"d:\!SAVE\table\gs.csv", "r", encoding="utf-8")
    f1 = f.readlines()
    f1 = f1[1:]
    result = []
    for line in f1:
        # print(line)
        line2 = line.split(",")
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
                      f" email, telegram, login, password,"
                      f" payment_date, number_of_days,"
                      f" deadline, until_date,"
                      f" comment)"
                      f" VALUES ('{line2[0].upper()}', '{line2[1].upper()}', "
                      f"'{line2[0].upper() + ' ' + line2[1].upper()}',"
                      f" '{line2[2]}', {telegram}, '{line2[4]}', '{line2[5]}',"
                      f" to_date('{line2[6]}', 'DD.MM.YYYY'), {line2[7]},"
                      f" to_date('{line2[8]}', 'DD.MM.YYYY'), {until_date}, "
                      f"{comment});")
    # for x in result:
    #    print(x)
    with open(r'd:\!SAVE\table\inserts.sql', 'w') as filehandle:
        filehandle.writelines("%s\n" % place for place in result)


if __name__ == "__main__":
    main()
