from PIL import Image, ImageTk


class Img:
    """
    产生幻影坦克图片，包括修改大小，显示黑白叠加效果
    """
    # img1， img2代表传入图片路径，fix1， fix2为二次元组，表示对图片高度的修正(默认为0)
    def __init__(self, img1, img2, fix1=(0, 0), fix2=(0, 0)):
        self.img1 = Image.open(img1)
        self.img2 = Image.open(img2)
        self.fix1 = fix1
        self.fix2 = fix2
        self.img = None
        self.height = 0
        self.width = 0
        self.type = 0   # type为-1表示两个图像不同形（1图宽小于高，2图宽大于高）, 1表示图1小，2表示图二小

    # 产生幻影图的img对象，并获取最大宽度与高度,如果图像不同型默认按照1图像处理
    def new(self):
        w1, h1 = self.img1.size
        w2, h2 = self.img2.size
        print(w1, w2)
        print(h1, h2)
        if w1 - h1 <= 0 and w2 - h2 <= 0:
            h = min(h1, h2)
            if h == h1:
                self.type = 1
            else:
                self.type = 2
            self.height = h
            self.width = min(w1, w2)

        elif w1 - h1 >= 0 and w2 - h2 >= 0:
            h = min(h1, h2)
            if h == h1:
                self.type = 1
            else:
                self.type = 2
            self.height = min(h1, h2)
            self.width = min(w1, w2)

        elif w1 - h1 <= 0 and w2 - h2 >= 0:
            print('here')
            self.type = -1
            self.height = h1
            self.width = w1

        else:
            self.type = -2
            self.height = h2
            self.width = w2
        print('here', self.width, self.height)
        img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 1))
        return img

    # 修改图片类型，并统一大小
    def retouch(self):
        self.img1 = self.img1.convert('RGBA')
        self.img2 = self.img2.convert('RGBA')
        # print('img1:{}, {}   img2:{}, {}'.format(*self.img1.size, *self.img2.size))
        if self.type == 1 or self.type == -1:
            w, h = self.img2.size

            ratio = self.width / w
            self.img2 = self.img2.resize((int(w * ratio), int(h * ratio)), Image.ANTIALIAS)
        elif self.type == 2 or self.type == -2:
            w, h = self.img1.size
            ratio = self.width / w
            self.img1 = self.img1.resize((int(w * ratio), int(h * ratio)), Image.ANTIALIAS)
        # print('img1:{}, {}   img2:{}, {}'.format(*self.img1.size, *self.img2.size))

    # 加工成为结果,可以考虑改为多线程
    def process(self):
        fix_w1, fix_h1 = self.fix1
        fix_w2, fix_h2 = self.fix2
        print(self.img1.size, self.img2.size, self.width, self.height)
        for i in range(self.width):
            for j in range(self.height):
                r1, g1, b1, a = self.img1.getpixel((i + fix_w1, j + fix_h1))
                r2, g2, b2, a = self.img2.getpixel((i + fix_w2, j + fix_h2))
                avg1 = int((max(r1, g1, b1) + min(r1, g1, b1)) * 0.95 / 2)
                avg2 = int((max(r2, g2, b2) + min(r2, g2, b2)) * 0.38 / 2)
                a0 = (255 - avg1 + avg2)
                if a0 >= 255:
                    a0 = 255
                if a0 <= 0:
                    a0 = 1
                r0 = int(avg2 * 255 / a0)
                self.img.putpixel((i, j), (r0, r0, r0, a0))

    # 生成白色背景叠加预览,返回一个img对象
    def w_preview(self):
        img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 1))
        for i in range(self.width):
            for j in range(self.height):
                r0, g0, b0, a0 = self.img.getpixel((i, j))
                r = int(r0 * a0 / 255 + (255 - a0))
                img.putpixel((i, j), (r, r, r, 255))
        return img

    # 生成黑色背景叠加预览,返回一个img对象
    def b_preview(self):
        img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 1))
        for i in range(self.width):
            for j in range(self.height):
                r0, g0, b0, a0 = self.img.getpixel((i, j))
                r = int(r0 * a0 / 255)
                img.putpixel((i, j), (r, r, r, 255))
        return img

    # 缩放成屏幕显示大小（返回一个imagetk包装好的类型）
    def show(self, img, w_size=300, h_size=250):
        w, h = img.size
        if w > h:
            ratio = w_size / w
        else:
            ratio = h_size / h

        img2 = img.resize((int(w * ratio), int(h * ratio)), Image.ANTIALIAS)
        return img2

    # 返回处理好的图片(调好大小，但是不存储)
    def main_(self):
        self.img = self.new()
        self.retouch()
        self.process()
        return self.img


def main():
    test = Img('test/test2.jpg', 'test/test.jpg')
    img = test.main_()
    img2 = test.w_preview()
    img3 = test.b_preview()
    img.save('test/res.png')
    img2.save('test/res_w.png')
    img3.save('test/res_b.png')


if __name__ == '__main__':
    main()
