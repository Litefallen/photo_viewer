from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import os

root = Tk()
root.title('Image Viewer')
sidebar_sizes = (int(root.winfo_screenwidth() / 8), int(root.winfo_screenheight() - root.winfo_screenheight() / 10))
# root.geometry(f'200x200')  # moving root window to the left and set its size
root.iconphoto(False, PhotoImage(file='image.png'))
root.state("zoomed")
# creating interface
main_frame = Frame(root, bd=0)
# main_frame.pack(fill=Y,expand=1)
main_frame.grid(row=0, column=0, sticky=NSEW)
main_canvas = Canvas(main_frame, width=int(root.winfo_screenwidth() / 8),
                     height=int(root.winfo_screenheight() - root.winfo_screenheight() / 10))
# main_canvas.grid(row=0,column=0,side=LEFT,fill=BOTH,expand=1)
main_canvas.grid(row=0, column=0, sticky=NSEW)
# scrollbar_frame = Frame(root,bd=0)
# scrollbar_frame.grid(row=0,column=1,sticky=NS)
scrollbar = ttk.Scrollbar(main_frame, command=main_canvas.yview)
scrollbar.grid(row=0, column=1, sticky=NS)
# scrollbar.grid(row=0,column=1,sticky=NS,)
main_canvas.configure(yscrollcommand=scrollbar.set)
main_canvas.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox('all')))
frame_with_buttons = Frame(main_canvas)

main_canvas.create_window((0, 0), window=frame_with_buttons, anchor=NW)

# back end stuff

dir_list = []
used_list = []
forbidden_list = []
pic_list = []
pic_name_list = []
pic_container = None
last_folder = None


def pic_resizer(pic):
    width, height = pic.width, pic.height
    print(f' initial picture width is : {width} and initial height is {height}')
    print(f' window width is : {(root.winfo_screenwidth() - root.winfo_screenwidth() / 8)} and window height is {root.winfo_screenheight() - root.winfo_screenheight() / 10}')

    width_dif = ((root.winfo_screenwidth() - root.winfo_screenwidth() / 8) / width)
    height_dif = ((root.winfo_screenheight() - root.winfo_screenheight() / 10) / height)
    print(width_dif,height_dif)
    resized_pic_width = int(width * min(width_dif,height_dif))
    resized_pic_height = int(height * min(width_dif,height_dif))
    # print(resized_pic_width,resized_pic_height)
    print(resized_pic_width, resized_pic_height)
    # print(main_canvas.winfo_screenheight(),main_canvas.winfo_screenwidth())
    return resized_pic_width, resized_pic_height


def pic_opener(pic_path):
    global pic_container
    # if img_root:  # making only one pic window opened
    #     img_root.destroy()
    # img_root = Toplevel(root)
    # pic_container = ImageTk.PhotoImage(Image.open(pic_path))

    opened_pic = Image.open(pic_path)
    # print(opened_pic.width,opened_pic.height)
    # print((pic_resizer(opened_pic)))
    opened_pic = opened_pic.resize((pic_resizer(opened_pic)))
    # opened_pic = opened_pic.resize((1777,1777))
    pic_container = ImageTk.PhotoImage(opened_pic)
    # img_root.geometry(f'{pic_container.width()}x{pic_container.height()}+{sidebar_sizes[0]}+0')
    img_widget = Label(main_frame, image=pic_container, anchor=NW)

    img_widget.grid(row=0, column=3, sticky=NSEW)
    # print(pic_container.width(), pic_container.height())


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
        fixed_but.pack(fill=BOTH, expand=1)


pic_finder('D:/music')
# print(list(os.scandir('D:/music')))


root.bind('<Escape>', lambda e: root.quit())

for pic in pic_list:
    cl_but = SpecificButton()
    cl_but.fixed_command(pic[0], pic[1])

root.mainloop()
