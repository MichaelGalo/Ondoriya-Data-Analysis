#!/usr/bin/env python3
import duckdb

duckdb.install_extension("ducklake")
duckdb.load_extension("ducklake")

con = duckdb.connect("ondoriya.db")
con.execute("ATTACH 'ducklake:ondoriya.db' AS my_lake")

con.execute("CREATE SCHEMA IF NOT EXISTS RAW")
con.execute("CREATE SCHEMA IF NOT EXISTS STAGED")
con.execute("CREATE SCHEMA IF NOT EXISTS CLEANED")

# example query
# with open ("sql/query.sql", "r") as f:
#     query = f.read()
# con.execute(query)

def main():
    print("Welcome to a duckdb pipeline!")

if __name__ == "__main__":
    main()
