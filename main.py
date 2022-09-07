from tkinter import *
from PIL import ImageTk, Image
import os

root = Tk()
root.title('Image Viewer')
root.iconphoto(False, PhotoImage(file='image.png'))
dir_list = []
used_list = []
forbidden_list = []
pic_list = []
pic_name_list = []

# img = ImageTk.PhotoImage(
#     Image.open('D:/music/Moby - All Visible Objects (2020)/sleeves/Moby - All Visible Objects (9).jpg'))
#
# img_widget = Label(image=img)
# img_widget.pack()


def pic_opener(pic_path):
    print(pic_path)
    img_root = Toplevel(root)
    img = ImageTk.PhotoImage(Image.open(pic_path))
    img_widget = Label(img_root, image=img)
    img_widget.pack()


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

# print(list(os.scandir('D:/music')))
counter = 0
# for pic in pic_list:
#     # print(pic)
#     pics = Button(root, text=pic[0], width=10, command=lambda: pic_opener(pic[1]))
#     pics.pack(expand=TRUE, fill=X)
#     counter += 1
# img = ImageTk.PhotoImage(Image.open('D:/music/Moby - All Visible Objects (2020)/sleeves/Moby - All Visible Objects (9).jpg'))
# img_widget = Label(image=img)
# img_widget.pack()
vv = Toplevel(root)
img = ImageTk.PhotoImage(Image.open('D:/music/Moby - All Visible Objects (2020)/sleeves/Moby - All Visible Objects (9).jpg'))
def bb(adress):
    img_widget = Label(vv,image=img)
    print(bool(img_widget))
    img_widget.pack()

a = Button(root,command=lambda :bb('D:/music/Moby - All Visible Objects (2020)/sleeves/Moby - All Visible Objects (9).jpg'))
a.pack()

root.mainloop()
