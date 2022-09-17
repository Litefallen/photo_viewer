from tkinter import *
from PIL import ImageTk, Image
import os

root = Tk()
root.title('Image Viewer')
sidebar_sizes = (int(root.winfo_screenwidth() / 8), int(root.winfo_screenheight() - root.winfo_screenheight() / 10))
# root.geometry(f'{sidebar_sizes[0]}x{sidebar_sizes[1]}+0+0')  # moving root window to the left and set its size
root.iconphoto(False, PhotoImage(file='image.png'))

# creating interface
main_frame = Frame(root)
main_frame.pack(fill=Y,expand=1)
main_canvas = Canvas(main_frame)
main_canvas.pack(side=LEFT,fill=BOTH,expand=1)

scrollbar = Scrollbar(main_frame, command=main_canvas.yview)
scrollbar.pack(side=RIGHT,fill=Y)
main_canvas.configure(yscrollcommand=scrollbar.set)
main_canvas.bind("<Configure>",lambda e: main_canvas.configure(scrollregion=main_canvas.bbox('all')))
frame_with_buttons = Frame(main_canvas,bg="blue")

main_canvas.create_window((0,0),window=frame_with_buttons,anchor=NW)

# back end stuff

dir_list = []
used_list = []
forbidden_list = []
pic_list = []
pic_name_list = []
pic_container = None
img_root = None
last_folder = None


def pic_opener(pic_path):
    global pic_container, img_root
    if img_root:  # making only one pic window opened
        img_root.destroy()
    img_root = Toplevel(root)
    pic_container = ImageTk.PhotoImage(Image.open(pic_path))

    img_root.geometry(f'{pic_container.width()}x{pic_container.height()}+{sidebar_sizes[0]}+0')
    img_widget = Label(img_root, image=pic_container)
    img_widget.grid()


def permission_check(folder):  # check if we have access to the folder
    try:
        os.scandir(folder)
        return True
    except PermissionError:
        forbidden_list.append(folder)
        print(f'{folder} folder is forbidden')


def pic_path_add(folder):  # get pic formats and add full path as string to list
    pic_list.extend([[i.name, f'{folder}/{i.name}'] for i in os.scandir(folder) if
                     i.name.endswith('.jpeg') or i.name.endswith('.jpg')])


def pic_finder(initial_folder):
    global last_folder
    last_folder = initial_folder
    if permission_check(initial_folder):  # check folder for access
        for i in os.scandir(initial_folder):
            if i.is_dir() and not i.name.startswith('$'):
                dir_list.append(f'{initial_folder}/{i.name}')
        pic_path_add(initial_folder)  # get pics full path to list
        used_list.append(initial_folder)
    for folder in dir_list:
        if folder not in used_list and folder not in forbidden_list:
            pic_finder(folder)
    return dir_list


# Buttons
class SpecificButton(Button):  # create custom class with fixed command function
    def fixed_command(self, name, dest):
        self.title = name
        self.path = dest
        fixed_but = Button(frame_with_buttons, text=self.title, command=lambda: pic_opener(self.path),
                           anchor=NW)
        fixed_but.pack(fill=BOTH,expand=1)


pic_finder('D:/music')
# print(list(os.scandir('D:/music')))


root.bind('<Escape>', lambda e: root.quit())

for pic in pic_list:
    cl_but = SpecificButton()
    cl_but.fixed_command(pic[0], pic[1])

root.mainloop()
