#rabotaem
import re
import tkinter.messagebox as text_window
import customtkinter
import os
import sqlite3


class Database_window(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.geometry("700x800")
        self.title("Визуализатор")
        
        self.textbox = customtkinter.CTkTextbox(self, width=700, height=500, corner_radius=0)
        self.textbox.grid(row=1, column=1, sticky="nsew")
        
        self.label = customtkinter.CTkLabel(self, text="Выгруженные данные: ")
        self.label.grid(row=0, column=1, padx=20)
        
        self.textbox = customtkinter.CTkTextbox(self, width=700, height=500, corner_radius=0)
        self.textbox.grid(row=1, column=1, sticky="nsew")
        
        #------------------------------------------------------------------------------------#
        conn = sqlite3.connect('user_logger.db')
        cursor = conn.cursor()
        
        logs = os.path.join('.','access_logs.log')
        pattern = r'^([\d\.]+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"$'

        with open(logs, 'r') as file:
            for line in file:
                match = re.match(pattern, line)
                if match:
                    user_ip = match.group(1)
                    user_timestamp = match.group(2)
                    user_request = match.group(3)
                    user_status_code = match.group(4)
                    user_content_size = match.group(5)
                    user_referrer = match.group(6)
                    user_agent = match.group(7)
                    
                    cursor.execute(
                                    "INSERT INTO user_logs (user_ip, user_timestamp, user_request, user_status_code, user_content_size, user_referrer, user_agent) VALUES (?,?,?,?,?,?,?)",
                                    (user_ip, user_timestamp, user_request, user_status_code, user_content_size, user_referrer, user_agent),
                                  )

        conn.commit()
        # cursor.close()
        #------------------------------------------------------------------------------------#

        query = "SELECT id, user_ip, user_timestamp, user_request, user_status_code, user_content_size, user_referrer, user_agent FROM user_logs"
        cursor.execute(query)

        result = cursor.fetchall()
    
        for row in result:
            self.textbox.insert("0.0", f"ID: {row[0]}\n")
            self.textbox.insert("0.0", f"IP: {row[1]}\n")
            self.textbox.insert("0.0", f"Timestamp: {row[2]}\n")
            self.textbox.insert("0.0", f"Request: {row[3]}\n")
            self.textbox.insert("0.0", f"Status Code: {row[4]}\n")
            self.textbox.insert("0.0", f"Content Size: {row[5]}\n")
            self.textbox.insert("0.0", f"Referrer: {row[6]}\n")
            self.textbox.insert("0.0", f"User Agent: {row[7]}\n")
            self.textbox.insert("0.0", "---------------------------\n")
                
        conn.commit()
        conn.close()
        
        self.textbox.configure(state="disabled")
        
        self.button_delete = customtkinter.CTkButton(self, width=240, height=100, border_width=0, corner_radius=0, command=self.enter_number, text="Удаление по ID", fg_color=("#008205", "#364900"))
        self.button_delete.grid(row=3, column=1, pady=25)
        
        self.button_refresh = customtkinter.CTkButton(self, width=240, height=100, border_width=0, corner_radius=0, command=self.DB_refresh, text="Обновить текстовое окно БД", fg_color=("#008205", "#364900"))
        self.button_refresh.grid(row=4, column=1)
        
        
    def enter_number(self):
        dialog_window = customtkinter.CTkInputDialog(text="Введите id, который желаете удалить:", title="Ввод ID", fg_color=("#008205", "#364900"), button_fg_color=("#364900", "#364900"))
        число = dialog_window.get_input()
        if int(число) > 0:
            self.Удаление_по_ID(число)
        else: text_window.showinfo("Ой!", "Ты ввел либо нолик, либо что-то ненормальное. Надо вводить реальный ID!")
        
    def Удаление_по_ID(self, число):
        conn = sqlite3.connect('user_logger.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM user_logs WHERE id = ?', (число,))
        conn.commit()
        conn.close()
    
    def DB_refresh(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        conn = sqlite3.connect('user_logger.db')
        cursor = conn.cursor()
        query = "SELECT id, user_ip, user_timestamp, user_request, user_status_code, user_content_size, user_referrer, user_agent FROM user_logs"
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            self.textbox.insert("0.0", f"ID: {row[0]}\n")
            self.textbox.insert("0.0", f"IP: {row[1]}\n")
            self.textbox.insert("0.0", f"Timestamp: {row[2]}\n")
            self.textbox.insert("0.0", f"Request: {row[3]}\n")
            self.textbox.insert("0.0", f"Status Code: {row[4]}\n")
            self.textbox.insert("0.0", f"Content Size: {row[5]}\n")
            self.textbox.insert("0.0", f"Referrer: {row[6]}\n")
            self.textbox.insert("0.0", f"User Agent: {row[7]}\n")
            self.textbox.insert("0.0", "---------------------------\n")
                
        conn.commit()
        conn.close()
        self.textbox.configure(state="disabled")
        
    
class User_logger_mainmenu(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.geometry("800x800")
        self.title("Вход в логгер")
        self.grid_columnconfigure((0), weight=1)
        
        
        
        
        self.button_open_database_window = customtkinter.CTkButton(self, width=240, height=200, border_width=0, corner_radius=15, command=self.Database_window_open, text="Открыть базу данных", fg_color=("#008205", "#364900"))
        self.button_open_database_window.grid(row=1, column=0, padx=50, pady=200)
        
        self.button_create_database= customtkinter.CTkButton(self, width=240, height=200, border_width=0, corner_radius=15, command=self.Database_create, text="Создать базу данных", fg_color=("#008205", "#364900"))
        self.button_create_database.grid(row=1, column=1, padx=80, pady=200)
        
        self.Database_window_open = None
        
    def Database_create(self):
        conn = sqlite3.connect('user_logger.db')
        cur = conn.cursor()

        cur.execute('''
        CREATE TABLE IF NOT EXISTS user_logs
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_ip TEXT,
            user_timestamp TEXT,
            user_request TEXT,
            user_status_code TEXT,
            user_content_size TEXT,
            user_referrer TEXT,
            user_agent TEXT
        )
        ''')

        conn.close()
        
    def Database_window_open(self):
        
        if os.path.exists("user_logger.db"):
            if self.Database_window_open is None or not self.Database_window_open.winfo_exists():
                self.Database_window_open = Database_window(self)
                self.iconify()
                self.Database_window_open.protocol("WM_DELETE_WINDOW", self.Database_window_close)
            else:
                self.Database_window_open.focus()
        else: text_window.showinfo("Внимание!", "У вас не создана БАЗА. Создайте ее перед запуском основного окна!")
        
    def Database_window_close(self):
            self.Database_window_open.destroy()
            self.deiconify()



if __name__ == "__main__":
    programm = User_logger_mainmenu()
    programm.mainloop()

# class User_logger_mainmenu(customtkinter.CTk):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        
#         ################################ Настройки окна ###################################
#         self.geometry("1000x800")
#         self.title("СуперОрганайзер by Gregulas")
#         ##################################################################
        
# #-------------------------------------------------------------------------------------#         

# #-------------------------------Цикл для работы программы-----------------------------#
# if __name__ == "__main__":
#     app = User_logger_mainmenu()
#     app.resizable(False, False)
#     app.mainloop()
# #-------------------------------------------------------------------------------------#