from tkinter import *
from tkinter import ttk
import subprocess

option_list = ["file", "folder", "back", ".py"]
option_dict = {"file":"*","folder":"Folder", "back":"Directory\\Background", ".py" : "SystemFileAssociations\\.py"}

Registry_name = "py_menu_"

# cmd呼び出し
def call_cmd(cmd):
	return [i.decode("shift_jis").rstrip('\r\n') for i in subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr = subprocess.DEVNULL, shell=True).stdout.readlines()]

# レジストリキー内のキー一覧
def rq_key(key):
	return call_cmd("reg query \"" + key + "\" /f * /k")[1:-1]

# レジストリキー内の値一覧
def rq_value(key):
	return call_cmd("reg query \"" + key + "\" /f * /v")[2:-2]

# レジストリキーの既定値
def rq_ve(key):
	return call_cmd("reg query \"" + key + "\" /ve")[2].split("    ")[3]

# 右クリックメニュー用レジストリキーの取得
def get_key(name, option="back", cmd=True):
	base = "HKEY_CURRENT_USER\\Software\\Classes\\"
	cmd_str = "command"
	if not(type(name) == str or len(name)==0):
		raise ValueError("name is wrong.")
	if not(option in option_list):
		raise ValueError("option is wrong.")
	return base + option_dict[option] + "\\Shell\\" + name + ("\\" + cmd_str if cmd else "")

# 右クリックメニュー用レジストリ一覧表示用キーの取得
def get_base(option="back"):
	base = "HKEY_CURRENT_USER\\Software\\Classes\\"
	if not(option in option_list):
		raise ValueError("option is wrong.")
	return base + option_dict[option] + "\\Shell"

# 現在適応されている右クリックメニュー一覧
def get_list():
	menus = []
	for i in option_list:
		base = get_base(i)
		for j in rq_key(base):
			key_name = j.replace(base + "\\", "")
			if key_name.find(Registry_name)==0:
				menus.append((key_name, i, rq_ve(j), rq_ve(j + "\\command")))
	return menus

# 現在適応されている右クリックメニューkey_name一覧
def get_key_name():
	menus = []
	for i in option_list:
		base = get_base(i)
		for j in rq_key(base):
			key_name = j.replace(base + "\\", "")
			if key_name.find(Registry_name)==0:
				menus.append(key_name)
	return menus

# 右クリックメニュー追加
def add_menu(name, command, option="back"):
	if not(type(name) == str or len(name)==0):
		raise ValueError("name is wrong.")
	if not(option in option_list):
		raise ValueError("option is wrong.")
	i = 1
	name_list = get_key_name()
	while True:
		key_name = Registry_name + str(i)
		if not(key_name in name_list):
			break
		i += 1
	key     = get_key(key_name, option, False)
	key_cmd = get_key(key_name, option, True)
	call_cmd("reg add \"" + key + "\" /ve /d " + "\"" + name + "\"")
	call_cmd("reg add \"" + key_cmd + "\" /ve /d " + "\"" + command + "\"")
	return i

def delete_menu(num):
	if type(num) != int:
		raise ValueError("num is wrong.")
	l = get_list()
	for i in l:
		if i[0] == Registry_name + str(num):
			call_cmd("reg delete \"" + get_key(i[0], i[1], False) + "\" /f")
			return

def button1_clicked():
	if eb1.get()=="" or eb2.get()=="":
		return
	num = add_menu(eb1.get(), eb2.get(), v1.get())
	tree.insert("", "end", values=(v1.get(), eb1.get(), eb2.get(), num))

def button2_clicked():
	item = tree.selection()
	delete_menu(int(tree.item(item, 'values')[3]))
	tree.delete(item)
	for i in range(3):
		entry_list[i].configure(state='normal')
		entry_list[i].delete(0, END)
		entry_list[i].configure(state='readonly')

def tree_selected(event):
	item = tree.selection()
	for i in range(3):
		entry_list[i].configure(state='normal')
		entry_list[i].delete(0, END)
		entry_list[i].insert(END, tree.item(item, 'values')[i])
		entry_list[i].configure(state='readonly')

if __name__ == '__main__':
	root = Tk()
	root.title("Context_Menu_Editor")
	root.geometry("640x480")
	root.minsize(640, 480)
	all_padx = 3
	all_pady = 3
	
	# Treeview
	tree = ttk.Treeview(root)
	
	tree["show"] = "headings"
	cfg_width    = [60, 275, 275]
	cfg_minwidth = [60, 150, 150]
	cfg_text     = ["Type","Text","Command"]
	cfg_anchor   = ["c","w","w"]
	tree["columns"] = list(range(len(cfg_text)))
	
	for i in range(len(cfg_text)):
		tree.column(i,width=cfg_width[i], minwidth=cfg_minwidth[i], anchor=cfg_anchor[i])
		tree.heading(i,text=cfg_text[i])
	
	for i in get_list():
		tree.insert("",int(i[0].replace(Registry_name, "")), values=list(i[1:])+[i[0].replace(Registry_name, "")])
	tree.grid(row=0, column=0, sticky=W+E+N+S, padx=all_padx, pady=all_pady)
	tree.bind("<<TreeviewSelect>>", tree_selected)
	
	# addFrame
	frame1 = ttk.LabelFrame(root, text="add", relief = 'groove', padding=5)
	frame1.grid(row=1, column=0, padx=all_padx, pady=all_pady)
	
	# Combobox
	v1 = StringVar()
	cb = ttk.Combobox(frame1, width=8, textvariable=v1)
	
	cb["values"]=option_list
	cb.set("back")
	cb.grid(row=1, column=0, padx=all_padx, pady=all_pady)
	
	# Label1
	label1 = []
	for i in range(len(cfg_text)):
		label1.append(Label(frame1, text=cfg_text[i]))
		label1[i].grid(row=0, column=i)
	
	# Entry1
	eb1 = ttk.Entry(frame1, width=200)
	eb1.grid(row=1, column=1, sticky=N+S, padx=all_padx, pady=all_pady)
	
	# Entry2
	eb2 = ttk.Entry(frame1, width=200)
	eb2.grid(row=1, column=2, sticky=N+S, padx=all_padx, pady=all_pady)
	
	# Button1
	button1 = ttk.Button(frame1, text='追加', command=button1_clicked)
	button1.grid(row=1, column=3, padx=all_padx, pady=all_pady)
	
	# deleteFrame
	frame2 = ttk.LabelFrame(root, text="delete", relief = 'groove', padding=5)
	frame2.grid(row=2, column=0, padx=all_padx, pady=all_pady)
	
	# Label
	label2 = []
	for i in range(len(cfg_text)):
		label2.append(Label(frame2, text=cfg_text[i]))
		label2[i].grid(row=0, column=i, padx=all_padx, pady=all_pady)
	
	# entry_list
	entry_list = []
	for i in range(len(cfg_text)):
		entry_list.append(ttk.Entry(frame2))
		entry_list[i].configure(state='readonly')
		entry_list[i].grid(row=1, column=i, padx=all_padx, pady=all_pady)
	entry_list[0]["width"] = 11
	entry_list[1]["width"] = 200
	entry_list[2]["width"] = 200
	
	# Button2
	button2 = ttk.Button(frame2, text='削除', command=button2_clicked)
	button2.grid(row=1, column=3, padx=all_padx, pady=all_pady)
	
	root.grid_columnconfigure(0, weight = 1)
	root.grid_rowconfigure(0, weight = 1)
	frame1.grid_columnconfigure(1, weight = 1)
	frame1.grid_columnconfigure(2, weight = 1)
	frame2.grid_columnconfigure(1, weight = 1)
	frame2.grid_columnconfigure(2, weight = 1)
	root.mainloop()
