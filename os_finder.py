import os


class OSHelper:

    # 根节点
    def __init__(self, s_path='r_path'):
        self.root = None
        self.s_path = s_path

    # 输入一个路径，获取目录下的所有文件名
    @staticmethod
    def img_getter(path):
        fin = list()
        if os.path.exists(path) is False:
            os.makedirs(path)
            return []
        for root, dirs, files in os.walk(path):
            for i in files:
                fin.append(path + '/' + i)
            return fin

    # 输入img对象，保存为指定目录指定名字位置
    def img_saver(self, img, name):
        img.save(self.s_path + '/' + name + '.png')


def main():
    oser = OSHelper()
    oser.img_getter('w_path')


if __name__ == '__main__':
    main()
