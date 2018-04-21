import sqlite3

class SkrepkaDB:

    table_FirstHelp = 'First_help'
    table_Tags = 'Tags'
    table_Graph = 'Graph'

    def __init__(self, path):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        try:
            self.create_HelpTable()
            self.create_TagTable()
            self.create_GraphTable()
        except:
            pass
        return

    def create_GraphTable(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE " + self.table_Graph + " ("
                                                                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                                                                "type TEXT, "
                                                                "text TEXT,"
                                                                "child_nodes TEXT"
                                                                ");")
        self.conn.commit()
        cursor.close()
        return True

    def create_HelpTable(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE " + self.table_FirstHelp + " ("
                                                                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                                                                    "path TEXT, "                                                                
                                                                    "text TEXT"
                                                                    ");")
        self.conn.commit()
        cursor.close()
        return True

    def create_TagTable(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE " + self.table_Tags + " ("
                                                                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                                                                "path TEXT, "
                                                                "tag TEXT"
                                                                ");")
        self.conn.commit()
        cursor.close()
        return True

    def add_tag_to_path(self, tag, path):
        cursor = self.conn.cursor()
        values = [None, path, tag]
        cursor.execute("INSERT INTO " + self.table_Tags + " VALUES(" + "?,"
                                                                       "?,"
                                                                       "?"
                                                                       ")",
                       values)
        self.conn.commit()
        cursor.close()
        return True

    def add_text_to_path(self, text, path):
        cursor = self.conn.cursor()
        values = [None, path, text]
        cursor.execute("INSERT INTO " + self.table_FirstHelp + " VALUES(" + "?,"
                                                                       "?,"
                                                                       "?"
                                                                       ")",
                       values)
        self.conn.commit()
        cursor.close()
        return True

    def delete_all_text(self, path):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM " + self.table_FirstHelp + " WHERE path = ?", (path,))
        self.conn.commit()
        cursor.close()
        return True

    def delete_all_tags(self, path):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM " + self.table_Tags + " WHERE path = ?", (path,))
        self.conn.commit()
        cursor.close()
        return True

    def add_tags(self, path, tags):
        tags = tags.split(' ')
        for tag in tags:
            self.add_tag_to_path(tag, path)

    def get_text(self, path):
        cursor = self.conn.cursor()
        cursor.execute("SELECT text FROM " + self.table_FirstHelp + " WHERE path = ?", (path,))
        data = cursor.fetchall()
        if len(data) == 0:
            cursor.close()
            return -1
        data = data[0][0]
        cursor.close()
        return data

    def get_tags(self, path):
        cursor = self.conn.cursor()
        cursor.execute("SELECT tag FROM " + self.table_Tags + " WHERE path = ?", [path])
        data = cursor.fetchall()
        if len(data) == 0:
            cursor.close()
            return -1
        data_arr = []
        for tag in data:
            data_arr.append(tag[0])
        cursor.close()
        return data_arr

    def get_path(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT path FROM " + self.table_Tags)
        data = cursor.fetchall()
        if len(data) == 0:
            cursor.close()
            return -1
        data_arr = []
        for path in data:
            data_arr.append(path[0])
        cursor.close()
        return data_arr

    def get_path_by_tag(self,tag):
        cursor = self.conn.cursor()
        cursor.execute("SELECT path FROM " + self.table_Tags + " WHERE tag='" + tag +"'")
        data = cursor.fetchall()
        if len(data) == 0:
            cursor.close()
            return -1
        data_arr = []
        for path in data:
            data_arr.append(path[0])
        cursor.close()
        return data_arr

    def get_parent(self, id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM " + self.table_Graph + " WHERE child_nodes LIKE '% " + str(id) + " %'")
        data = cursor.fetchall()
        if len(data) == 0:
            cursor.close()
            return -1
        data = data[0][0]
        cursor.close()
        return data

    def get_node_by_id(self, id):
        def get_node_by_id(self, id):
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM " + self.table_Graph + " WHERE id = ?", (id,))
            data = cursor.fetchall()[0]
            if len(data) == 0:
                return -1
            cursor.close()
            parent = self.get_parent(id)
            data_arr = []
            for i in range(1, len(data)):
                data_arr.append(data[i])
            data_arr.append(parent)
            cursor.close()
            return data_arr

    def add_node(self, type, text, parent_id):
        cursor = self.conn.cursor()
        values = [None, type, text, '']
        cursor.execute("INSERT INTO " + self.table_Graph + " VALUES(" + "?,"
                                                                        "?,"
                                                                        "?,"
                                                                        "?"
                                                                        ")",
                       values)
        if parent_id != -1:
            id_value = cursor.lastrowid
            cursor.execute("SELECT child_nodes FROM " + self.table_Graph + " WHERE id = ?", (parent_id,))
            children = cursor.fetchall()[0][0]
            cursor.execute("UPDATE " + self.table_Graph + " SET child_nodes = ? WHERE id = ?;",
                           (children + " " + str(id_value) + " ",
                            parent_id))
        self.conn.commit()
        cursor.close()
        return True

    def node_list(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT max(id) FROM " + self.table_Graph)
        max_id = cursor.fetchone()[0]
        data_arr = []
        for id in range(1,max_id+1):
            cursor.execute("SELECT * FROM " + self.table_Graph + " WHERE id = ?", (id,))
            node_data = cursor.fetchall()[0]
            tmp_data = []
            for i in node_data:
                tmp_data.append(i)
            data_arr.append(tmp_data)
            data_arr[id - 1].append(self.get_parent(id))
        cursor.close()
        return data_arr

    def del_node(self, id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT child_nodes FROM " + self.table_Graph + " WHERE id = ?", (id,))
        children = cursor.fetchall()[0][0].split(' ')
        children_arr = []
        for data in children:
            if data != '':
                children_arr.append(data)
        for i in children_arr:
            self.del_node(i)
        cursor.execute("DELETE FROM " + self.table_Graph + " WHERE id = ?", (id,))
        self.conn.commit()
        cursor.close()

    def child_info(self, id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT child_nodes FROM " + self.table_Graph + " WHERE id = ?", (id,))
        children = cursor.fetchall()[0][0].split(" ")
        child_array = []
        for id_c in children:
            if id_c != '':
                cursor.execute("SELECT * FROM " + self.table_Graph + " WHERE id = ?", (id_c,))
                info = cursor.fetchall()[0]
                tmp_array = []
                for i in info:
                    tmp_array.append(i)
                child_array.append(tmp_array)
        cursor.close()
        return child_array

