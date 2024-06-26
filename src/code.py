import sqlite3
from typing import Optional
import pandas as pd


class DonationRecord:

    def __init__(self, ingredients:dict,name:str, contact_number:str, book:str, place:str, date:str, book_serial_num : str,id:Optional[int]=None):
        self.id = id
        self.book = book
        self.name = name
        self.contact_number = contact_number
        self.place = place
        self.date = date 
        self.book_serial_num = book_serial_num
        self.ingredients = {key: 0 for key in DonationRecord.get_columns()}
        self.ingredients.update(ingredients)

    
    def __str__(self) -> str:
        return self.name
    
    
    def get_params(self) -> dict:
        return self.__dict__
    
    
    def get_data_tuple(self) -> tuple:
        return tuple(self.__dict__.values())

    @staticmethod
    def get_columns() -> list[str]:
        with sqlite3.connect("./db/madurai.db") as con:
            table = pd.read_sql("SELECT * FROM donation_records ;", con)
            cols = [col for col in table.columns if table[col].dtype != "O"]
            return cols[1:]
        
    
    def insert_record(self) -> bool:
        
        with sqlite3.connect("./db/madurai.db") as con:
            
            try :
                
                cur = con.cursor()
                
                columns = tuple(self.get_params().keys())[1:-1] + tuple(self.get_params()["ingredients"].keys())
                values = tuple(self.get_params().values())[1:-1] + tuple(self.get_params()["ingredients"].values())
                statement = f"INSERT INTO donation_records {columns} VALUES {values};"
                
                cur.execute(statement)
                # statement = f"INSERT INTO donation_records_nt {columns} VALUES {values};"
                # cur.execute(statement)
                con.commit()
                return True
            
            except Exception as e:
                print(e)
        
    
    def update_record(self,new_ingredients:dict) -> bool:

        with sqlite3.connect("./db/madurai.db") as con:

            cur = con.cursor()
            
            set_clause = ", ".join([f"'{key}'={value}" for key, value in filter_ingredients(ingredients=new_ingredients).items()])
            statement = f"UPDATE donation_records SET {set_clause} WHERE id={self.id};"
            cur.execute(statement)

            con.commit()
            return True
        
    def delete_record(self) -> bool:
        
        with sqlite3.connect("./db/madurai.db") as con:
            
            cur = con.cursor()
            
            statement = f"DELETE FROM donation_records WHERE id = {self.id};"
            cur.execute(statement)
            # statement = f"DELETE FROM donation_records_nt WHERE id = {self.id};"
            # cur.execute(statement)
            con.commit()
            return True


def filter_ingredients(ingredients) -> dict:
    return {key:value for key, value in ingredients.items() if key in DonationRecord.get_columns() and value is not None}



class Allocation:

    def __init__(
            self,team_name : str, 
            team_supervisor : str, 
            date : str, dish : str,
            team_supervisor_contact_number : str,
            ingredients : dict,
            allocation_id = None) -> None :
        self.allocation_id = allocation_id
        self.team_name = team_name
        self.team_supervisor = team_supervisor
        self.team_supervisor_contact_number = team_supervisor_contact_number
        self.date = date
        self.dish = dish 
        self.ingredients =  {product : 0 for product in DonationRecord.get_columns()}
        self.ingredients.update(ingredients)

    def get_params(self):
        return self.__dict__
    
    def get_data_tuple(self):

        return tuple(self.__dict__.values())
    
    def insert_record(self) -> bool:

        with sqlite3.connect("./db/madurai.db") as con:

            try :

                cur = con.cursor()
                
                columns = tuple(self.get_params().keys())[1:-1] + tuple(self.get_params()["ingredients"].keys())
                values = tuple(self.get_params().values())[1:-1] + tuple(self.get_params()["ingredients"].values())
                statement = f"INSERT INTO allocation {columns} VALUES {values};"
                
                # print(statement)   
                cur.execute(statement)
                con.commit()
                return True
            
            except Exception as e:
                return e

