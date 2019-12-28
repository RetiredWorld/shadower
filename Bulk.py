from tkinter import Tk, Button, Label, Entry, IntVar
from PIL import ImageTk, Image

from Img import Img
from os_finder import OSHelper

# 沙雕tkinter（解释器？）需要全局变量才能不回收phototk对象,容纳这四个对象
img_lis = [x for x in range(4)]


class Bulk:
    # 传入路径名称，实例化窗口
    def __init__(self, w_path, b_path, s_path):
        self.w_path = w_path
        self.b_path = b_path
        self.s_path = s_path
        self.oser = OSHelper(s_path=self.s_path)

        self.w_img_lis = None       # 所有白底目录下图片的名称
        self.b_img_lis = None       # 所有黑底目录下图片的名称
        self.w_img = None           # 目前操作的黑底图片
        self.w_img = None           # 目前操作的白底图片
        self.shadow = None          # 幻影tk
        self.b_i = 0                # 黑底图片index
        self.w_i = 0                # 白底图片index

        self.kit = dict()           # 保存所有组件
        self.root = Tk()            # 实例化
        self.bw_value = IntVar(self.root)   # 翻页选择值

        self.process = None

    # 初始化，得到所有图片名称,调整gui属性
    def init(self):
        self.w_img_lis = self.oser.img_getter(self.w_path)
        self.b_img_lis = self.oser.img_getter(self.b_path)
        self.root.wm_geometry("900x640+200+4")
        self.root.wm_title('ShadowSocketR')

    # gui实现组件主体
    def gui(self):
        """
        组件对照表
        show_img：               显示原图片提示label
        w_img:                   白底原图label
        b_img：                  黑底原图label
        w_prior:                 白底图片上一张button
        w_next:                  白底图片下一张button
        b_prior:                 黑底图片上一张button
        b_next:                  黑底图片下一张button

        show_preview：           显示预览（黑白底叠加结果）提示label
        wd_img:                  白底原图label
        bd_img：                 黑底原图label
        wd_up:                   白底图片位置上调button
        wd_down:                 白底图片位置下调button
        wd_left:                 白底图片位置左调button
        wd_right:                白底图片位置右调button
        bd_up:                   黑底图片位置上调button
        bd_down:                 黑底图片位置下调button
        bd_left:                 黑底图片位置左调button
        bd_right:                黑底图片位置右调button

        generate：               生成button
        save：                   保存button
        save_name:               保存名字entry
        """
        # 定义组件
        self.kit['show_img'] = Label(self.root, text='原图')
        self.kit['show_img'].grid(row=0, column=0)

        self.kit['w_img'] = Label(self.root, text='test\n')
        self.kit['w_img'].grid(row=1, column=0, rowspan=2)

        self.kit['b_img'] = Label(self.root, text='test\n')
        self.kit['b_img'].grid(row=1, column=3, rowspan=2)

        self.kit['w_prior'] = Button(self.root, text='上一张', command=self.w_change1)
        self.kit['w_prior'].grid(row=1, column=1)

        self.kit['w_next'] = Button(self.root, text='下一张', command=self.w_change2)
        self.kit['w_next'].grid(row=2, column=1)

        self.kit['b_prior'] = Button(self.root, text='上一张', command=self.b_change1)
        self.kit['b_prior'].grid(row=1, column=4)

        self.kit['b_next'] = Button(self.root, text='下一张', command=self.b_change2)
        self.kit['b_next'].grid(row=2, column=4)

        self.kit['show_preview'] = Label(self.root, text='预览')
        self.kit['show_preview'].grid(row=3, column=0)

        self.kit['wd_img'] = Label(self.root, text='test\n')
        self.kit['wd_img'].grid(row=4, column=0, rowspan=2)

        self.kit['bd_img'] = Label(self.root, text='test\n')
        self.kit['bd_img'].grid(row=4, column=3, rowspan=2)

        self.kit['wd_up'] = Button(self.root, text='向上调')
        self.kit['wd_up'].grid(row=4, column=1)

        self.kit['wd_down'] = Button(self.root, text='向下调')
        self.kit['wd_down'].grid(row=4, column=2)

        self.kit['bd_up'] = Button(self.root, text='向上调')
        self.kit['bd_up'].grid(row=4, column=4)

        self.kit['bd_down'] = Button(self.root, text='向下调')
        self.kit['bd_down'].grid(row=4, column=5)

        self.kit['wd_left'] = Button(self.root, text='向左调')
        self.kit['wd_left'].grid(row=5, column=1)

        self.kit['wd_right'] = Button(self.root, text='向右调')
        self.kit['wd_right'].grid(row=5, column=2)

        self.kit['bd_left'] = Button(self.root, text='向左调')
        self.kit['bd_left'].grid(row=5, column=4)

        self.kit['bd_right'] = Button(self.root, text='向右调')
        self.kit['bd_right'].grid(row=5, column=5)

        self.kit['generate'] = Button(self.root, text='生成', command=self.gene)
        self.kit['generate'].grid(row=6, column=2)

        self.kit['save'] = Button(self.root, text='保存', command=self.saver)
        self.kit['save'].grid(row=6, column=3)

        self.kit['save_entry'] = Entry(self.root, text='保存')
        self.kit['save_entry'].grid(row=6, column=4)

        global ori_img1, ori_img2
        self.process = Img(self.w_img_lis[self.w_i], self.b_img_lis[self.b_i])
        img1 = self.process.show(self.process.img1)
        ori_img1 = ImageTk.PhotoImage(image=img1)
        self.kit['w_img']['image'] = ori_img1
        img2 = self.process.show(self.process.img2)
        ori_img2 = ImageTk.PhotoImage(image=img2)
        self.kit['b_img']['image'] = ori_img2

    # 传入图像，显示图像, i表示位置（0： 白底原图， 1： 黑底原图， 2： 白底预览， 3: 黑底预览）
    def show_ori(self, img, i):
        global img_lis
        img_lis[i] = ImageTk.PhotoImage(image=img)
        if i == 0:
            self.kit['w_img']['image'] = img_lis[i]
        elif i == 1:
            self.kit['b_img']['image'] = img_lis[i]
        elif i == 2:
            self.kit['wd_img']['image'] = img_lis[i]
        else:
            self.kit['bd_img']['image'] = img_lis[i]

    # 以下四个为 原图换页切换
    def w_change1(self):
        self.w_i -= 1
        if self.w_i < 0:
            self.w_i = len(self.w_img_lis) - 1
        self.process = Img(self.w_img_lis[self.w_i], self.b_img_lis[self.b_i])
        self.show_ori(self.process.show(self.process.img1), 0)

    def w_change2(self):
        self.w_i += 1
        if self.w_i >= len(self.w_img_lis):
            self.w_i = 0
        self.process = Img(self.w_img_lis[self.w_i], self.b_img_lis[self.b_i])
        self.show_ori(self.process.show(self.process.img1), 0)

    def b_change1(self):
        self.b_i -= 1
        if self.b_i < 0:
            self.b_i = len(self.b_img_lis) - 1
        self.process = Img(self.w_img_lis[self.w_i], self.b_img_lis[self.b_i])
        self.show_ori(self.process.show(self.process.img2), 1)

    def b_change2(self):
        self.b_i += 1
        if self.b_i >= len(self.b_img_lis):
            self.b_i = 0
        self.process = Img(self.w_img_lis[self.w_i], self.b_img_lis[self.b_i])
        self.show_ori(self.process.show(self.process.img2), 1)

    # 生成幻影tank
    def gene(self):
        self.shadow = self.process.main_()
        self.show_ori(self.process.show(self.process.w_preview()), 2)
        self.show_ori(self.process.show(self.process.b_preview()), 3)

    # 保存图片在指定文件夹中,默认保存为temp.png
    def saver(self):
        if self.shadow is None:
            return
        name = self.kit['save_entry'].get()
        if name is '':
            name = 'temp'
        self.oser.img_saver(self.shadow, name)

    # 运行，开始消息循环
    def main_(self):
        self.init()
        self.gui()
        self.root.mainloop()


def main():
    bulk = Bulk('w_path', 'b_path', 's_path')
    bulk.main_()


if __name__ == '__main__':
    main()
