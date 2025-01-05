from dotenv import load_dotenv
load_dotenv()
import sqlite3
import os
from supabase import create_client
import time        

class DataBase():
    def __init__(self):
        database_name = 'newsappdb.db'
        # we start to connect at ours databases
        self.con = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}", check_same_thread=False)
        cur = self.con.cursor()

        # we creer ours databases if not exist
            # 1. Theme Data
        cur.execute("CREATE TABLE IF NOT EXISTS ThemeData (theme TEXT)")
        self.con.commit()
            # 2. Data News
        cur.execute("CREATE TABLE IF NOT EXISTS DataNews (ID INTEGER, Title TEXT, Image_path TEXT, Subtitle TEXT, Date TEXT, Heure TEXT)")
        self.con.commit()

        # we create LastNewsId database
        cur.execute("CREATE TABLE IF NOT EXISTS LastNewsId (Numero INTEGER)")
        self.con.commit()

        # We create login database 
        cur.execute("CREATE TABLE IF NOT EXISTS Login (email TEXT)")
        self.con.commit()

        # We try to get a data on ThemeData database 
        cur.execute("SELECT * FROM ThemeData")
        row = cur.fetchall()
        nbrelmdb = len(row)

            # If not exist we insert one
        if nbrelmdb == 0:
            cur.execute("INSERT INTO ThemeData (theme) VALUES ('system')")
            self.con.commit()

        # We try to get a data on Login database 
        cur.execute("SELECT * FROM ThemeData")
        row = cur.fetchall()
        user = len(row)

            # If not exist we insert one
        if user == 0:
            cur.execute("INSERT INTO Login (email) VALUES ('Aucun')")
            self.con.commit()
        
        # we try too for lastnewsid database 
        cur.execute("SELECT * FROM LastNewsId")
        row = cur.fetchall()
        nbrelmdb = len(row)

            # If not exist we insert one
        if nbrelmdb == 0:
            cur.execute("INSERT INTO ThemeData (Numero) VALUES ('1000')")
            self.con.commit()
        
        cur.close()
    
    def Update_ThemeData (self, theme):
        
        cursor = self.con.cursor()
        query = f"UPDATE ThemeData SET theme = ? ;"
        cursor.execute(query, (theme,))
        cursor.close()
        self.con.commit()
        return

    def insert_to_News_DataBase(self, ID, title,Image_path ,Subtitle, Date, Heure):
        cursor = self.con.cursor()
        query = f"INSERT INTO DataNews (ID, Title, Image_path, Subtitle, Date, Heure) VALUES (?,?,?,?,?,?);"
        cursor.execute(query, (ID, title,Image_path ,Subtitle, Date, Heure))
        cursor.close()
        self.con.commit()
        return

    def get_themedata_mode(self):
        cursor = self.con.cursor()
        query = f"SELECT * FROM ThemeData"
        cursor.execute(query, ())
        result = cursor.fetchall()
        cursor.close()
        return result

    def get__email_on_Login_Database(self):
        cursor = self.con.cursor()
        query = f"SELECT * FROM Login"
        cursor.execute(query, ())
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_data_on_local_database(self):
        cursor = self.con.cursor()
        query = f"SELECT * FROM DataNews"
        cursor.execute(query, ())
        result = cursor.fetchall()
        cursor.close()
        result.sort(reverse=True)
        # news = result.sort()
        return result
    
    def change_lastnewsId(self, Id_for_updating):
        cursor = self.con.cursor()
        query = f"UPDATE LastNewsId SET Numero = ? ;"
        cursor.execute(query, (Id_for_updating,))
        cursor.close()
        self.con.commit()
        return

    def listen_change_in_local_database(self, fonction_for_insertion):
        # get the laster element in local database
        laster_element = self.get_data_on_local_database()[0]
        id_laster_element = laster_element[0]

        # get register id in LastNewsId database 
        cursor = self.con.cursor()
        query = f"SELECT * FROM LastNewsId"
        cursor.execute(query, ())
        result = cursor.fetchall()

        laster_id = result[0][0]

        if laster_id != id_laster_element :
            fonction_for_insertion(laster_element)
            self.change_lastnewsId(id_laster_element)

    def update_login_database(self, email):
        cursor = self.con.cursor()
        query = f"UPDATE Login SET email = ? ;"
        cursor.execute(query, (email,))
        cursor.close()
        self.con.commit()
        return

class DataBaseOnline():
    def __init__(self):
        try : 
            url = os.environ.get("SUPABASE_URL")
            key = os.environ.get("SUPABASE_KEY")
            self.supabase = create_client(url, key)
            while True : 
                time.sleep(5)
                self.get_all_news()
        except :
            print("Pas des connection internet !")

    def get_all_news(self):
        data_news_in_only_database = self.supabase.table("News").select("*").execute()
        Database_news_in_local_database = DataBase().get_data_on_local_database()
        for i in data_news_in_only_database.data :
            actuality_finded = 0
            for j in Database_news_in_local_database :
                if i['ID'] == j[0] :
                    actuality_finded = 1
                
            if actuality_finded == 0 :
                id = i['ID']
                Title = i['Title']
                image_path = i['Image_path']
                subtitle = i['Subtitle']
                Date = i['Date']
                Heure = i['Heure']
                DataBase().insert_to_News_DataBase(id, Title, image_path, subtitle, Date, Heure)
                actuality_finded = 0

class DataBaseOnlineAgain():
    def __init__(self):
        try : 
            url = os.environ.get("SUPABASE_URL")
            key = os.environ.get("SUPABASE_KEY")
            self.supabase = create_client(url, key)
        except :
            return "NoConnection"

    def create_a_new_user_compte(self, email, name, password):
        email_user = email
        name_user = name
        password_user = password
        try : 
            self.supabase.table("Users").insert(
                {
                    "email": email_user,
                    "name": name_user,
                    "password": password_user
                }
            ).execute()
            DataBase().update_login_database(email_user)
            return "succes"
        except :
            return "NoConnection"
    def have_a_count(self, email, password) :
        email_user = email
        password_user = password

        try :

            all_user_get_unformated = self.supabase.table("Users").select("*").execute()

            all_user = all_user_get_unformated.data

            user_finded = 0
            for i in all_user :
                if i['email'] == email_user :
                    user_finded = 1
                    print("11")
                    if i['password'] == password_user :
                        print("12")
                        DataBase().update_login_database(email_user)
                        return "Goodpassword"
                    else :
                        return "Badpassword"

            if user_finded == 0 :
                return "NoEmail"
            
        except :
            return "NoConnection"

    def get_image_affiche(self):
        try : 
            all_image = self.supabase.table("ImageAffiche").select("*").execute()
            liste_image = []
            for i in all_image.data :
                liste_image.append(i['Link'])

            return liste_image
        except Exception as e :
            print(e)
