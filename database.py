import sqlite3

class Database():
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def add_waiting(self, chat_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `wait_room` (`chat_id`) VALUES (?)", (chat_id,))

    def delete_wating(self, chat_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `wait_room` WHERE chat_id = ?", (chat_id,))

    def delete_chat(self, id_chat):
        with self.connection:
            return self.cursor.execute("DELETE FROM `chats` WHERE id = ?", (id_chat,))

    def get_user_id(self):
        with self.connection:
            user_id = self.cursor.execute("SELECT * FROM `wait_room`", ()).fetchmany(1)
            if(bool(len(user_id))):
                for row in user_id:
                    return row[1]
            else:
                return False

    def get_info(self, chat_id, first_name, gender):
        with self.connection:
           
            self.cursor.execute("INSERT INTO `users` (`chat_id`, `first_name`, `pol`) VALUES (?, ?, ?)", (chat_id, first_name, gender))


    def create_chat(self, chat_1, chat_2):
        with self.connection:
            if chat_2 != 0:
                self.cursor.execute("DELETE FROM `wait_room` WHERE chat_id = ?", (chat_2,))
                self.cursor.execute("INSERT INTO `chats` (`user_1`, `user_2`) VALUES (?, ?)", (chat_1, chat_2))
                return True
            else:
                return False

    def get_active_chat(self, chat_id):
        with self.connection:
            chat = self.cursor.execute("SELECT * FROM `chats` WHERE `user_1` = ?", (chat_id,))
            id_chat = 0
            for row in chat:
                id_chat = row[0]
                chat_info = [row[0], row[2]]

            if id_chat == 0:
                chat = self.cursor.execute("SELECT * FROM `chats` WHERE `user_2` = ?", (chat_id,))
                for row in chat:
                    id_chat = row[0]
                    chat_info = [row[0], row[1]]
                if id_chat == 0:
                    return False
                else:
                    return chat_info
            
            else:
                return chat_info
