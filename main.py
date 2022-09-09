import tkinter
from tkinter import *
from PIL import ImageTk, Image
import os
print(())
root = Tk()

root.title('Image Viewer')
root.geometry(f'25x{root.winfo_screenheight()}+0+0') # moving root window to the left
root.iconphoto(False, PhotoImage(file='image.png'))
dir_list = []
used_list = []
forbidden_list = []
pic_list = []
pic_name_list = []
pic_container = None
img_root = None

def pic_opener(pic_path):
    global pic_container, img_root
    if img_root: # making only one pic window opened
        img_root.destroy()
    img_root = Toplevel(root)
    pic_container = ImageTk.PhotoImage(Image.open(pic_path))
    img_root.geometry(f'{pic_container.width()}x{pic_container.height()}+100+0')
    img_widget = Label(img_root, image=pic_container)
    img_widget.grid()


def permission_check(folder):  # check if we have access to the folder
    try:
        os.scandir(folder)
    except PermissionError:
        forbidden_list.append(folder)
        print(f'{folder} folder is forbidden')


def pic_path_add(folder):  # get pic formats and add full path as string to list
    pic_list.extend([[i.name, f'{folder}/{i.name}'] for i in os.scandir(folder) if
                     i.name.endswith('.jpeg') or i.name.endswith('.jpg')])


def pic_finder(initial_folder):
    permission_check(initial_folder)  # check folder for access
    # print(pic_list)
    if initial_folder not in used_list and initial_folder not in forbidden_list:
        pic_path_add(initial_folder)  # get pics full path to list
        for i in os.scandir(initial_folder):
            if i.is_dir() and not i.name.startswith('$'):
                dir_list.append(f'{initial_folder}/{i.name}')
            used_list.append(initial_folder)
        for folder in dir_list:
            pic_finder(folder)

    return dir_list, pic_list


pic_finder('D:/music')


class SpecificButton(Button):  # create custom class with fixed command function
    def fixed_command(self, name, dest):
        self.title = name
        self.path = dest
        fixed_but = Button(root, text=self.title, command=lambda: pic_opener(self.path),width=25)
        fixed_but.pack(side=TOP)
        print(fixed_but.winfo_screenwidth())


# print(list(os.scandir('D:/music')))
for pic in pic_list:
    cl_but = SpecificButton()
    cl_but.fixed_command(pic[0], pic[1])

root.mainloop()
