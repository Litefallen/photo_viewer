from tkinter import *
import os

root = Tk()

dir_list = []
used_list = []
forbidden_list = []
pic_list = []

def pic_opener(pic):
    pass

def permission_check(folder):  # check if we have access to the folder
    try:
        os.scandir(folder)
    except PermissionError:
        forbidden_list.append(folder)
        print(f'{folder} folder is forbidden')


def pic_path_add(folder):  # get pic formats and add full path as string to list
    pic_list.extend([f'{folder}/{i.name}' for i in os.scandir(folder) if i.name.endswith('.jpeg') or i.name.endswith('.jpg')])


def pic_finder(initial_folder):
    permission_check(initial_folder) # check folder for access
    pic_path_add(initial_folder) # get pics full path to list
    if initial_folder not in used_list and initial_folder not in forbidden_list:
        for i in os.scandir(initial_folder):
            if i.is_dir() and not i.name.startswith('$'):
                dir_list.append(f'{initial_folder}/{i.name}')
        used_list.append(initial_folder)
        for folder in dir_list:
            pic_finder(folder)
    return dir_list, pic_list


print(*pic_finder('D:/music'), sep='\n\n\n\n')
# print(list(os.scandir('D:/music')))
for pic in pic_list:
    pics = Label(root,text=pic)
    pics.pack()

root.mainloop()