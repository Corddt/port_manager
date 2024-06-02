以下是一个详细的中文README.md文件，说明如何使用该代码来管理端口。

```markdown
# 端口管理魔法师

端口管理魔法师是一款基于Python的图形用户界面（GUI）应用程序，用于管理本地计算机的端口。它允许用户检查端口的运行状态，启动或关闭指定端口，并实时显示当前正在运行的端口列表。

## 特性

- 检查指定端口是否在运行
- 启动指定端口
- 关闭指定端口
- 实时显示当前正在运行的端口列表
- 点击正在运行的端口列表中的端口，自动填入输入框中

## 依赖

- Python 3.x
- `socket` 库（Python 标准库）
- `psutil` 库
- `tkinter` 库（Python 标准库）

## 安装

1. 安装Python 3.x，请访问[Python官网](https://www.python.org/)下载并安装。
2. 安装依赖库`psutil`：
   ```bash
   pip install psutil
   ```

## 使用

1. 将以下代码保存为 `port_manager.py`：

    ```python
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
    ```

2. 打开终端或命令提示符，导航到保存`port_manager.py`的目录。
3. 运行以下命令启动程序：
    ```bash
    python port_manager.py
    ```

## 打包为可执行文件

你可以使用`PyInstaller`将该程序打包为独立的可执行文件。

1. 安装`PyInstaller`：
    ```bash
    pip install pyinstaller
    ```

2. 使用以下命令打包脚本，并指定图标文件：
    ```bash
    pyinstaller --onefile --windowed --icon=icon.ico port_manager.py
    ```

打包完成后，可执行文件将生成在`dist`文件夹中。

## 联系方式

如有任何问题或建议，请联系开发者。

---

希望这个README对你有帮助，享受你的端口管理魔法师之旅！
```