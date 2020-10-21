import psycopg2
import argparse
import core.PASSWORDS as PASSWORDS


def copy_table(connectionStringSrc, connectionStringDst, table_name_src, table_name_dst, verbose=False, condition=""):
    with psycopg2.connect(connectionStringSrc) as connSrc:
        with psycopg2.connect(connectionStringDst) as connDst:
            query = "SELECT * FROM {} {};".format(table_name_src, condition)
            with connSrc.cursor() as curSrc:
                curSrc.execute(query)
                print("Source number of rows =", curSrc.rowcount)
                with connDst.cursor() as curDst:
                    for row in curSrc:
                        # generate %s x columns
                        query_columns = ','.join([desc[0] for desc in curSrc.description])
                        query_values = ','.join('%s' for x in range(len(curSrc.description)))
                        query = "INSERT INTO {} ({}) VALUES ({});".format(table_name_dst, query_columns, query_values)
                        param = [item for item in row]
                        if verbose:
                            print(curDst.mogrify(query, param))
                        curDst.execute(query, param)


"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("cs_src", type=str,
                        help='connection string source like: "host=localhost port=5432 user=admin password=mypwd dbname=mydbname"')
    parser.add_argument("cs_dst", type=str,
                        help='connection string destination like: "host=localhost port=5432 user=admin password=mypwd dbname=mydbname"')

    parser.add_argument("tablename", type=str,
                        help='Table name')

    parser.add_argument("-w", "--where", type=str,
                        help='append sql where query "WHERE id = 123"')

    parser.add_argument("-v", "--verbose",
                        help='increase output verbosity', action="store_true")

    args = parser.parse_args()
    copy_table(args.cs_src, args.cs_dst, args.tablename, args.verbose, args.where)
"""
if __name__ == '__main__':
    connectionStringSrc = f"host={PASSWORDS.settings['postgres_host']} port={PASSWORDS.settings['postgres_port']} user={PASSWORDS.settings['postgres_user']} password={PASSWORDS.settings['postgres_password']} dbname={PASSWORDS.settings['postgres_dbname_src']}"
    connectionStringDst = f"host={PASSWORDS.settings['postgres_host']} port={PASSWORDS.settings['postgres_port']} user={PASSWORDS.settings['postgres_user']} password={PASSWORDS.settings['postgres_password']} dbname={PASSWORDS.settings['postgres_dbname_dst']}"
    table_name_src = PASSWORDS.settings['table_name_src']
    table_name_dst = PASSWORDS.settings['table_name_dst']
    copy_table(connectionStringSrc, connectionStringDst, table_name_src, table_name_dst, verbose=True)
