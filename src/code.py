import sqlite3
from typing import Optional


class DonationRecord:
    def __init__(self, ingredients:dict,name:str, contact_number:str, book:str, place:str, date:str, id:Optional[int]=None):
        self.id = id
        self.book = book
        self.name = name
        self.contact_number = contact_number
        self.place = place
        self.date = date 
        self.ingredients = {key: 0 for key in DonationRecord.get_columns()}
        self.ingredients.update(filter_ingredients(ingredients))

    def __str__(self):
        return self.name
    
    def get_params(self):
        return self.__dict__
    
    def get_data_tuple(self):
        return tuple(self.__dict__.values())

    @staticmethod
    def get_columns():
        return [
            'Manjal Podi', 'Pachai Arisi(bag)', 'Pachai Arisi(Loose)',
            'Puzungal Arisi(Bag)', 'Puzungal Arisi(Loose)', 'Ulundhu', 'Nei',
            'Sugar', 'Arisi maavu', 'Thu Parupu', 'Pa parupu', 'Annasi Poo',
            'Ginger', 'Rock Salt', 'Table Salt', 'Elachi', 'Groundnut Oil',
            'Ka parupu', 'Kadala Mavu', 'Kadugu', 'Garam Masala', 'Krambu',
            'seeragam', 'Sombu', 'Grapes', 'Gingerly oil', 'Pattai', 'Brinji Ilai',
            'Perungayam', 'Puli', 'Malli', 'Malli powder', 'Milagai Vathal',
            'Milagai Powder', 'Milagu', 'Milagu Thul', 'Cashew', 'Rava',
            'Refined oil', 'Vendhayam', 'Vellam', 'Garlic', 'Kal Pasi', 'Pumpkin',
            'Sambar Powder', 'Potato', 'katti peruganyam', 'Mango Pack', 'Nuts',
            'Giragam', 'Kalkandu', 'Mumthal', 'Tea Powder', 'Coconut', 'Appalam',
            'Lk Glass', 'Silvar Glass', 'Sabeena Powder', 'Rava.1', 'Kungumam',
            'Kismis', 'Fortune Oil', 'Sengal(Bricks)', 'Mango(Mangai)', 'Javaraci',
            'Hp Gas', 'Curd', 'Vetttrillai', 'Pakku', 'Butter', 'Valiaikai',
            'Samiya', 'Gold Winner', 'Dates', 'Ballari', 'Manjal Kayiru',
            'Kungumam pack', 'Catds', 'Kungumam cover', 'Plastic Cup', 'Sponge',
            'Coffee powder', 'Gas cylinder', 'palasaraku porul', 'Pam poil'
          ]
    
    def insert_record(self) -> bool:
        with sqlite3.connect("./data/madurai.db") as con:
            try :
                cur = con.cursor()
                columns = tuple(self.get_params().keys())[1:-1] + tuple(self.get_params()["ingredients"].keys())
                values = tuple(self.get_params().values())[1:-1] + tuple(self.get_params()["ingredients"].values())
                statement = f"INSERT INTO donation_records {columns} VALUES {values};"
                cur.execute(statement)
                con.commit()
                return True
            except Exception as e:
                pass

    def update_record(self,new_ingredients:dict)->bool:
        with sqlite3.connect("./data/madurai.db") as con:
            cur = con.cursor()
            set_clause = ", ".join([f"'{key}'={value}" for key, value in filter_ingredients(ingredients=new_ingredients).items()])
            statement = f"UPDATE donation_records SET {set_clause} WHERE id={self.id};"
            cur.execute(statement)
            con.commit()
            return True


def filter_ingredients(ingredients):
    return {key:value for key, value in ingredients.items() if key in DonationRecord.get_columns()}
