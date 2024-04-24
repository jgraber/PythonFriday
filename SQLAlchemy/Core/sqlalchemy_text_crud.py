from sqlalchemy import create_engine, text

def create():
    insert = text("""
                INSERT INTO "main"."Employee" 
                ("LastName", "FirstName", "Title", "BirthDate") 
                VALUES 
                (:last, :first, :title, :dob);                
                """)
    connection_string = "sqlite:///Northwind_small.sqlite"
    engine = create_engine(connection_string, echo=False)
    with engine.begin() as con:
        con.execute(insert, {"last":"Davolio","first":"Nancy","title":"Sales","dob":"1980-05-29"})
        new_id = con.execute(text("SELECT last_insert_rowid() AS Id;")).first()
        print(new_id)    
        return new_id[0]


def read(id):
    select = text("""
            SELECT Id, LastName, FirstName, Title, BirthDate 
            FROM Employee
            WHERE LastName = :last AND FirstName IS NOT :first AND Id = :id
            """)
    
    connection_string = "sqlite:///Northwind_small.sqlite"
    engine = create_engine(connection_string, echo=False)
    with engine.begin() as con:
        for row in con.execute(select, {"last":"Davolio", "first":"Robert", "id":id}):
            print(row)
            print(row[1])


def update(id):
    update = text("""
            UPDATE Employee
            SET LastName = :last, 
            FirstName = :first
            WHERE Id = :id
            """)
    
    connection_string = "sqlite:///Northwind_small.sqlite"
    engine = create_engine(connection_string, echo=False)
    with engine.begin() as con:
        con.execute(update, {"last":"D'Avolio","first":"Patricia","id":id})
    
    with engine.begin() as con2:
        for row in con2.execute(text("SELECT Id, LastName, FirstName FROM Employee WHERE id = :id"), {"id":id}):
            print(row)


def delete(id):
    delete = text("""
                  DELETE from Employee WHERE Id = :id
                  """)

    connection_string = "sqlite:///Northwind_small.sqlite"
    engine = create_engine(connection_string, echo=False)
    with engine.begin() as con:
        con.execute(delete, {"id":id})
        
    with engine.begin() as con2:
        for row in con2.execute(text("SELECT Id, LastName, FirstName FROM Employee WHERE id = :id"), {"id":id}):
            print(row)
        else:
            print("No rows found")

if __name__ == '__main__':
    print("--- create() ---")
    id = create()
    print("--- read() ---")
    read(id)
    print("--- update() ---")
    update(id)
    print("--- delete() ---")
    delete(id)