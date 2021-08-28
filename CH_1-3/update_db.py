from sqlalchemy import update, select
import build_db

connection = build_db.engine.connect()


# update the value of the quantity column for chocolate chip cookies
u = update(build_db.cookies).where(
    build_db.cookies.c.cookie_name == "chocolate chip")
u = u.values(quantity=(build_db.cookies.c.quantity + 120))
result = connection.execute(u)
print(result.rowcount)

s = select([build_db.cookies]).where(
    build_db.cookies.c.cookie_name == "chocolate chip")
result = connection.execute(s).first()
for key in result.keys():
    print('{:>20}: {}'.format(key, result[key]))
