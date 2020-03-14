def diff_lists(list1, list2):
    return list(set(list1) - set(list2))


if __name__ == '__main__':
    import list_
    list_yandex = []
    list_db = []
    for i in list_.list1.splitlines():
        list_yandex.append(i)
    for i in list_.list2.splitlines():
        list_db.append(i)
    a = (diff_lists(list_yandex, list_db))
    b = (diff_lists(list_db, list_yandex))
    print(a)
    print(b)
    for i in a:
        print(i)
