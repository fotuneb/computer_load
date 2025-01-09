import tkinter as tk
from tkinter import ttk
import psutil
import sqlite3
import time
import threading

# Создание базы данных
conn = sqlite3.connect('system_monitor.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS system_usage (
        timestamp TEXT, 
        cpu_usage REAL, 
        ram_usage REAL, 
        disk_usage REAL
    )
''')
conn.commit()

class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")
        self.root.geometry("400x200")

        self.recording = False
        self.start_time = None

        self.cpu_label = ttk.Label(root, text="CPU Usage: 0%")
        self.cpu_label.pack(pady=5)
        self.ram_label = ttk.Label(root, text="RAM Usage: 0%")
        self.ram_label.pack(pady=5)
        self.disk_label = ttk.Label(root, text="Disk Usage: 0%")
        self.disk_label.pack(pady=5)

        self.start_button = ttk.Button(root, text="Начать запись", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(root, text="Остановить", command=self.stop_recording)
        self.stop_button.pack(pady=10)
        self.stop_button.pack_forget()

        self.timer_label = ttk.Label(root, text="Time: 0 s")
        self.timer_label.pack(pady=5)
        self.timer_label.pack_forget()

        self.update_stats()

    def update_stats(self):
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        self.cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
        self.ram_label.config(text=f"RAM Usage: {ram_usage}%")
        self.disk_label.config(text=f"Disk Usage: {disk_usage}%")

        if self.recording:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            c.execute('INSERT INTO system_usage VALUES (?, ?, ?, ?)', 
                      (timestamp, cpu_usage, ram_usage, disk_usage))
            conn.commit()

            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed_time} s")

        self.root.after(1000, self.update_stats)

    def start_recording(self):
        self.recording = True
        self.start_time = time.time()
        self.start_button.pack_forget()
        self.stop_button.pack()
        self.timer_label.pack()

    def stop_recording(self):
        self.recording = False
        self.start_button.pack()
        self.stop_button.pack_forget()
        self.timer_label.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()
