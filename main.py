from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog
import os
import sys

root = Tk()
root.iconphoto(False, PhotoImage(file='image.png'))
root.withdraw()

folder = filedialog.askdirectory(initialdir='/', title='Choose a folder to search for pictures')
if not folder:
    root.destroy()
else:
    root.bind('<Escape>', lambda e: root.quit())
    root.state('zoomed')
    root.title('Image Viewer')
    sidebar_sizes = (int(root.winfo_screenwidth() / 8), int(root.winfo_screenheight() - root.winfo_screenheight() / 10))
    # creating interface
    main_frame = Frame(root)
    main_frame.grid(row=0, column=0, sticky=NSEW)
    main_canvas = Canvas(main_frame, width=int(root.winfo_screenwidth() / 8),
                         height=int(root.winfo_screenheight() - root.winfo_screenheight() / 10))
    main_canvas.grid(row=0, column=0)
    scrollbar = ttk.Scrollbar(main_frame, command=main_canvas.yview)
    scrollbar.grid(row=0, column=1, sticky=NS)
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
    rec_limit = 1000
    counter = 1


    def pic_resizer(pic):
        width, height = pic.width, pic.height
        width_dif = ((root.winfo_screenwidth() - (root.winfo_screenwidth() / 8 )-40)/ width)
        height_dif = ((root.winfo_screenheight() - root.winfo_screenheight() / 10)/ height)
        resized_pic_width = int(width * min(width_dif, height_dif))
        resized_pic_height = int(height * min(width_dif, height_dif))
        print(width,height)
        print(resized_pic_width, resized_pic_height)
        print(root.winfo_screenwidth()-root.winfo_screenwidth() / 8,root.winfo_screenheight()- root.winfo_screenheight() / 10)
        return resized_pic_width, resized_pic_height


    def pic_opener(pic_path):
        global pic_container
        opened_pic = Image.open(pic_path)
        opened_pic = opened_pic.resize((pic_resizer(opened_pic)))
        pic_container = ImageTk.PhotoImage(opened_pic)
        img_widget = Label(main_frame, image=pic_container,anchor=NW)
        img_widget.grid(row=0, column=2,sticky=NSEW)


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
        global last_folder, counter
        last_folder = initial_folder
        if permission_check(initial_folder):  # check folder for access
            for i in os.scandir(initial_folder):
                if i.is_dir() and not i.name.startswith('$'):
                    dir_list.append(f'{initial_folder}/{i.name}')
            pic_path_add(initial_folder)  # get pics full path to list
            used_list.append(initial_folder)
        for folder in dir_list:
            if folder not in used_list and folder not in forbidden_list:
                global rec_limit # 'fixing' recursion limit issue, if amount of folded folders is too big
                if (rec_limit - counter) < 10:
                    rec_limit += 15
                    sys.setrecursionlimit(rec_limit)
                counter += 1
                pic_finder(folder)

    sys.setrecursionlimit(1000) # revert recursion limit settings
    # Buttons
    class SpecificButton(Button):  # create custom class with fixed command function
        def fixed_command(self, name, dest):
            self.title = name
            self.path = dest
            fixed_but = Button(frame_with_buttons, text=self.title, command=lambda: pic_opener(self.path),
                               anchor=W, width=sidebar_sizes[0])
            fixed_but.pack()

    # pic_finder('D:\music')
    pic_finder(folder)
    # print(pic_list)
    if not pic_list:
        label = Label(root, text='No pictures were found')
        label.place(rely=0.5, relx=0.5)
    for pic in pic_list:
        cl_but = SpecificButton()
        cl_but.fixed_command(pic[0], pic[1])

root.mainloop()
