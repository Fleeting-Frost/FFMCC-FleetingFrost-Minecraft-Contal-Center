import os
import tkinter as tk
from tkinter import filedialog, messagebox

class PluginManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft插件管理器")
        self.root.geometry("600x400")
        self.root.iconbitmap("timerange.ico")  # 设置窗口图标

        self.plugins_dir = "plugins"  # 设置插件目录
        self.enabled_plugins = []
        self.disabled_plugins = []

        # 创建容器frame来组织界面布局
        self.left_frame = tk.Frame(self.root)
        self.right_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 创建启用插件标签和列表框
        self.enabled_label = tk.Label(self.left_frame, text="启用的插件", fg="green")
        self.enabled_label.pack(pady=10)
        self.enabled_listbox = tk.Listbox(self.left_frame, selectmode=tk.MULTIPLE)
        self.enabled_listbox.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        # 创建禁用插件标签和列表框
        self.disabled_label = tk.Label(self.right_frame, text="禁用的插件", fg="red")
        self.disabled_label.pack(pady=10)
        self.disabled_listbox = tk.Listbox(self.right_frame, selectmode=tk.MULTIPLE)
        self.disabled_listbox.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        # 创建应用更改按钮
        self.apply_button = tk.Button(self.root, text="应用更改", command=self.apply_changes)
        self.apply_button.pack(side=tk.BOTTOM, pady=10)

        self.scan_plugins()

    def scan_plugins(self):
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir)  # 如果plugins目录不存在，则创建它
        for file in os.listdir(self.plugins_dir):
            if file.endswith(".jar"):
                self.enabled_plugins.append(file)
            elif file.endswith(".ban"):
                self.disabled_plugins.append(file)

        self.update_listboxes()

    def update_listboxes(self):
        self.enabled_listbox.delete(0, tk.END)
        self.disabled_listbox.delete(0, tk.END)

        for plugin in self.enabled_plugins:
            self.enabled_listbox.insert(tk.END, plugin)

        for plugin in self.disabled_plugins:
            self.disabled_listbox.insert(tk.END, plugin)

    def apply_changes(self):
        enabled_selection = self.enabled_listbox.curselection()
        disabled_selection = self.disabled_listbox.curselection()

        enabled_plugins_to_disable = [self.enabled_listbox.get(index) for index in enabled_selection]
        disabled_plugins_to_enable = [self.disabled_listbox.get(index) for index in disabled_selection]

        for plugin in enabled_plugins_to_disable:
            os.rename(os.path.join(self.plugins_dir, plugin), os.path.join(self.plugins_dir, plugin.replace(".jar", ".ban")))
            self.enabled_plugins.remove(plugin)
            self.disabled_plugins.append(plugin.replace(".jar", ".ban"))

        for plugin in disabled_plugins_to_enable:
            os.rename(os.path.join(self.plugins_dir, plugin), os.path.join(self.plugins_dir, plugin.replace(".ban", ".jar")))
            self.disabled_plugins.remove(plugin)
            self.enabled_plugins.append(plugin.replace(".ban", ".jar"))

        self.update_listboxes()
        messagebox.showinfo("成功", "插件状态已更新")

if __name__ == "__main__":
    root = tk.Tk()
    plugin_manager = PluginManager(root)
    root.mainloop()
