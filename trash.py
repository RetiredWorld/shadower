from PIL import Image
from PIL import ImageTk
from tkinter import Label, Tk


b = dict()
root = Tk()
image = Image.open('test/test2.jpg')
a = ImageTk.PhotoImage(image=image)
b['h'] = Label(root, text='sa')
l1 = Label(root, text='asddsa')
l1.place(x=600, y=0)
b['h']['image'] = a
b['h'].grid()

root.mainloop()
