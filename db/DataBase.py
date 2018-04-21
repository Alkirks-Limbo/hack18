import sqlite3

class DataBase:

    tableUsers_DataBase = 'Users'
    tableBills_DataBase = 'Bills'
    tableCards_DataBase = 'Cards'
    tableDrivers_DataBase = 'Drivers'


    def __init__(self, path):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        try:
            self.create_BillsTable()
            self.create_CardsTable()
            self.create_DriversTable()
            self.create_UsersTable()
        except:
            pass
        return

    def create_UsersTable(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE " + self.tableUsers_DataBase + " ("
                                                                         "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                                                                         "email TEXT, "
                                                                         "full_name TEXT, "
                                                                         "company TEXT, "
                                                                         "phone TEXT,"
                                                                         "password TEXT"
                                                                         ");")
        self.conn.commit()
        cursor.close()
        return

    def create_BillsTable(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE " + self.tableBills_DataBase + " ("
                                                                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                                                                    "number TEXT, "
                                                                    "owner_email TEXT,"
                                                                    "account INT"
                                                                    ");")
        self.conn.commit()
        cursor.close()
        return

    def create_CardsTable(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE " + self.tableCards_DataBase + " ("
                                                                         "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                                                                         "number TEXT, "
                                                                         "owner_billNumber TEXT, "
                                                                         "consumption INT"
                                                                         ");")
        self.conn.commit()
        cursor.close()
        return

    def create_DriversTable(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE " + self.tableDrivers_DataBase + " ("
                                                                         "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                                                                         "full_name TEXT, "
                                                                         "owner_email TEXT, "
                                                                         "card TEXT, "
                                                                         "car_number TEXT"  
                                                                         ");")
        self.conn.commit()
        cursor.close()
        return

    def reg_user(self, full_name, email, password, company, phone):
        if not self.check_reg_user(email):
            return False
        cursor = self.conn.cursor()
        values = [None, email, full_name, company, phone, password]
        cursor.execute("INSERT INTO " + self.tableUsers_DataBase + " VALUES(" + "?,"
                                                                                "?,"
                                                                                "?,"
                                                                                "?,"
                                                                                "?,"
                                                                                "?"
                                                                                ")",
                       values)
        self.conn.commit()
        cursor.close()
        return True

    def check_reg_user(self, email):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM "+ self.tableUsers_DataBase +" WHERE email = ?", (email, ))
        data=cursor.fetchall()
        if len(data)==0:
            cursor.close()
            return True
        cursor.close()
        return False

    def login_user(self, email, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT password FROM " + self.tableUsers_DataBase + " WHERE email = ?", (email,))
        check_password = cursor.fetchall()[0][0]
        cursor.close()
        if check_password == password:
            return True
        return False

    def update_pass_user(self, email, new_pass):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE " + self.tableUsers_DataBase + " SET password = ? WHERE email = ?;", (new_pass, email))
        cursor.close()
        self.conn.commit()

    def create_user_pocket(self, email, pocket_number):

        cursor = self.conn.cursor()
        values = [None, pocket_number, email, 0]
        cursor.execute("INSERT INTO " + self.tableBills_DataBase + " VALUES(" + "?,"
                                                                                "?,"
                                                                                "?,"
                                                                                "?"
                                                                                ")",
                       values)
        self.conn.commit()
        cursor.close()
        return True

    def add_cart2pocket_user(self, card_number, pocket):
        cursor = self.conn.cursor()
        values = [None, card_number, pocket, 0]
        cursor.execute("INSERT INTO " + self.tableCards_DataBase + " VALUES(" + "?,"
                                                                                "?,"
                                                                                "?,"
                                                                                "?"
                                                                                ")",
                       values)
        self.conn.commit()
        cursor.close()
        return True

    def get_user_info(self, email):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM " + self.tableUsers_DataBase + " WHERE email = ?", (email,))
        data = cursor.fetchall()[0]
        data_dict = {}
        data_dict['id'] = data[0]
        data_dict['email'] = data[1]
        data_dict['full_name'] = data[2]
        data_dict['company'] = data[3]
        data_dict['phone'] = data[4]
        data_dict['password'] = data[5]
        cursor.close()
        return data_dict

    def get_user_pockets_and_money(self, email):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM " + self.tableBills_DataBase + " WHERE owner_email = ?", (email,))
        data = cursor.fetchall()[0]
        data_dict = {}
        data_dict['pocket_number'] = data[1]
        data_dict['money_amount'] = data[3]
        cursor.close()
        return data_dict

    def update_prefs_user(self, old_email, new_email, full_name, phone, company):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE " + self.tableUsers_DataBase + " SET full_name = ?, phone = ?, company = ? "
                                                              "WHERE email = ?;",
                       (full_name, phone, company, old_email))
        self.change_email_everywhere(old_email, new_email)
        self.conn.commit()
        cursor.close()
        return True

    def change_email_everywhere(self, old_email, new_email):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE " + self.tableUsers_DataBase + " SET email = ? "
                                                              "WHERE email = ?;", (new_email, old_email))
        cursor.execute("UPDATE " + self.tableBills_DataBase + " SET owner_email = ? "
                                                              "WHERE owner_email = ?;", (new_email, old_email))
        cursor.execute("UPDATE " + self.tableDrivers_DataBase + " SET owner_email = ? "
                                                                "WHERE owner_email = ?;", (new_email, old_email))
        self.conn.commit()
        cursor.close()
        return True

    def add_money2pocket(self, pocket_number, amount_money):
        cursor = self.conn.cursor()
        cursor.execute("SELECT account FROM " + self.tableBills_DataBase + " WHERE number = ?", (pocket_number,))
        count = cursor.fetchall()[0][0]
        cursor.execute("UPDATE " + self.tableBills_DataBase + " SET account = ? WHERE number = ?;", (count + amount_money,
                                                                                                     pocket_number,))
        self.conn.commit()
        cursor.close()
        return True

    def del_card(self, cardnum):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM " + self.tableCards_DataBase + " WHERE number = ?", (cardnum,))
        cursor.execute("UPDATE " + self.tableDrivers_DataBase + " SET card = ? WHERE card = ?", ('', cardnum,))
        self.conn.commit()
        cursor.close()
        return True

    def add_driver(self, boss_email, driver_full_name, card_number, driver_car):
        cursor = self.conn.cursor()
        values = [None, driver_full_name, boss_email, card_number, driver_car]
        cursor.execute("INSERT INTO " + self.tableDrivers_DataBase + " VALUES(" + "?,"
                                                                                  "?,"
                                                                                  "?,"
                                                                                  "?,"
                                                                                  "?"
                                                                                  ")",
                       values)
        self.conn.commit()
        cursor.close()
        return True

    def get_cards(self, pocket):
        cursor = self.conn.cursor()
        cursor.execute("SELECT number FROM " + self.tableCards_DataBase + " WHERE owner_billNumber = ?", (pocket,))
        data = cursor.fetchall()
        data_arr = []
        for i in data:
            data_arr.append(i[0])
        cursor.close()
        return data_arr

    def get_drivers(self, boss_email):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM " + self.tableDrivers_DataBase + " WHERE owner_email = ?", (boss_email,))
        data = cursor.fetchall()
        data_arr = []
        for i in data:
            data_arr.append([i[1], i[2], i[3]])
        cursor.close()
        return data_arr

    def find_driver(self, cardnum):
        cursor = self.conn.cursor()
        cursor.execute("SELECT full_name FROM " + self.tableDrivers_DataBase + " WHERE card = ?", (cardnum,))
        try:
            data = cursor.fetchall()[0][0]
            cursor.close()
            return data
        except:
            cursor.close()
            return ""

    def delete_driver(self, cardnum):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM " + self.tableDrivers_DataBase + " WHERE card = ?", (cardnum,))
        self.conn.commit()
        cursor.close()



