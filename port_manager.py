import socket
import psutil
import tkinter as tk
from tkinter import messagebox, ttk


def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0


def close_port(port):
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            process = psutil.Process(conn.pid)
            process.terminate()
            return True
    return False


def run_port(port):
    # Placeholder for starting a service on the port
    # In a real application, you would start the actual service here
    return True


def update_port_list():
    # 保存当前的滚动条位置
    scroll_position = running_ports.yview()

    running_ports.delete(0, tk.END)
    ports = sorted(set(conn.laddr.port for conn in psutil.net_connections() if conn.status == psutil.CONN_LISTEN))
    for port in ports:
        running_ports.insert(tk.END, port)

    # 恢复滚动条位置
    running_ports.yview_moveto(scroll_position[0])

    root.after(1000, update_port_list)


def confirm_run_port():
    port = int(entry_port.get())
    if check_port(port):
        if messagebox.askyesno("端口状态", f"端口 {port} 已经在运行了。你确定要重启它吗？"):
            if run_port(port):
                messagebox.showinfo("端口状态", f"端口 {port} 已经重启成功。")
                update_port_list()
            else:
                messagebox.showerror("错误", f"重启端口 {port} 失败。")
    else:
        if messagebox.askyesno("确认运行", f"你确定要启动端口 {port} 吗？"):
            if run_port(port):
                messagebox.showinfo("端口状态", f"端口 {port} 现在正在运行。")
                update_port_list()
            else:
                messagebox.showerror("错误", f"启动端口 {port} 失败。")


def confirm_close_port():
    port = int(entry_port.get())
    if check_port(port):
        if messagebox.askyesno("确认关闭", f"端口 {port} 正在运行。你确定要关闭它吗？"):
            if close_port(port):
                messagebox.showinfo("端口状态", f"端口 {port} 已经关闭。")
                update_port_list()
            else:
                messagebox.showerror("错误", f"关闭端口 {port} 失败。")
    else:
        messagebox.showinfo("端口状态", f"端口 {port} 没有在使用中。")


def on_port_select(event):
    selected_port = running_ports.get(running_ports.curselection())
    entry_port.delete(0, tk.END)
    entry_port.insert(0, selected_port)


# 创建主窗口
root = tk.Tk()
root.title("端口管理魔法师")
root.geometry("300x400")
root.resizable(False, False)

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 10), padding=10)
style.configure("TLabel", font=("Helvetica", 12))

# 创建并放置控件
label_port = ttk.Label(root, text="请输入端口号：")
label_port.pack(pady=10)

entry_port = ttk.Entry(root)
entry_port.pack(pady=5)

button_run = ttk.Button(root, text="启动端口", command=confirm_run_port)
button_run.pack(pady=5)

button_close = ttk.Button(root, text="关闭端口", command=confirm_close_port)
button_close.pack(pady=5)

label_running_ports = ttk.Label(root, text="正在运行的端口：")
label_running_ports.pack(pady=10)

running_ports = tk.Listbox(root, height=10)
running_ports.pack(pady=5, fill=tk.BOTH, expand=True)
running_ports.bind('<<ListboxSelect>>', on_port_select)

update_port_list()

# 运行主事件循环
root.mainloop()
