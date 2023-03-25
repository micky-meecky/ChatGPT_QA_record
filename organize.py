# 该文件用于统计self-attention.txt文件中的问题数
import os
import argparse
import shutil
import time
import datetime

class Organize:
    def __init__(self, config):
        self.lines = None
        self.file = None
        self.path = config.path
        self.Md_path = config.Md_path
        self.readme_path = config.readme_path
        self.Qnum = 0
        self.Anum = 0
        self.QAnum = 0
        self.history_path = './history/'
        self.QLines = []
        self.ALines = []
        self.QA = []



    # 读取文件
    def ReadFile(self):
        self.file = open(self.path, 'r')
        # 获取文件内容的编码格式类型
        # q: 为什么要获取文件内容的编码格式类型？ a: 为了解决编码问题。
        print('文件编码格式为：', self.file.encoding)
        # q: 这一步是什么意思？ a: 读取文件中的所有行，存储在一个列表中。
        self.lines = self.file.readlines()
        # 输出lines的形状大小
        print('lines的形状大小为：', len(self.lines))
        # q: lines是什么类型？ a: list类型。
        self.file.close()

    # 统计问题回答数
    def TallyUpNum(self):
        self.ReadFile()
        digits = 0
        for line in self.lines:
            # 如果改行开头是以Q+数字开头的，并它的前两行是空行，那么该行就是问题行，问题数加1
            foreline1 = self.lines[self.lines.index(line) - 1]
            foreline2 = self.lines[self.lines.index(line) - 2]
            if line.startswith('Q') and foreline1 == '\n' and foreline2 == '\n':
                self.Qnum += 1
                # 获取Q后面的数字, 一般形式为Q+数字+;+空格+问题内容
                # q: 为什么要获取Q后面的数字？ a: 为了统计问题数。
                digits = line.split('Q')[1].split(':')[0]
                # 将数字转换为int类型
                digits = int(digits)

            # 如果该行开头是以A+digits开头的，形式为A+数字+;+空格+回答内容，那么该行就是回答行，回答数加1
            if line.startswith('A' + str(digits)):
                self.Anum += 1

        # 打印文本内容中的digits数
        print('digits数为：', digits)
        self.QAnum = digits

    # 创建名为name的文件夹
    def CreateFolder(self, name):
        # 判断history_path是否存在，如果不存在，则创建
        if not os.path.exists(self.history_path):
            os.makedirs(self.history_path)

        # 判断文件夹是否存在，如果不存在，则创建
        if not os.path.exists(name):
            os.makedirs(name)

    # 将这些内容写入一个md文件中
    def EmbeddingList(self):
        # 先执行一次TallyUpNum()函数
        self.TallyUpNum()
        _is_Qline = False   # 用于判断当前行是不是问题行
        _is_Aline = False   # 用于判断当前行是不是问题行或者回答行
        subQ = []  # 用于存储问题i中的行
        subA = []  # 用于存储回答i中的行
        idx = 0  # 用于记录当前行的索引
        q_idx = 0  # 用于记录当前问题的索引
        a_idx = 0  # 用于记录当前回答的索引
        digits = 0  # 用于记录当前行的数字

        # 首先读取TXT文件内容并按照问题和回答的形式分割，将其转换为一个嵌套列表（list of lists）的形式，每个子列表包含一个问题和其对应的回答。
        # 不需要调用ReadFile()函数，因为TallyUpNum()函数中已经调用过了。
        # self.ReadFile()
        # 遍历所有行
        for line in self.lines:
            # 检测那些行是问题行，比如第一行开头是以Q+数字开头的，并它的前两行是空行，那么该行就是问题行
            # 但是有些问题不只一行，所以要检测下面一行是不是问题行，可是下一行并不会再以Q+数字开头，所以只能检测下一行和下下行是不是都是空行，
            # 如果都是空行，那么从Q+数字开头的那行算起到那连续的两行空行前面的那行都是问题行。
            foreline1 = self.lines[self.lines.index(line) - 1]
            foreline2 = self.lines[self.lines.index(line) - 2]
            # 获取后两行的内容
            backline1 = self.lines[self.lines.index(line) + 1]
            backline2 = self.lines[self.lines.index(line) + 2]
            if line.startswith('Q') and foreline1 == '\n' and foreline2 == '\n':
                digits = line.split('Q')[1].split(':')[0]  # 获取Q后面的数字, 一般形式为Q+数字+;+空格+问题内容
                # 去除开头的Q/A+数字+;
                line = line.split(':')[1]
                # 在line的开头加三个空格，作为缩进
                line = '  ' + line
                if backline1.startswith('A'):  # 说明此时的line是问题行的最后一行
                    # 说明此时的line是问题行的最后一行
                    subQ.append(line)
                    # 重置标志位
                    _is_Qline = False
                    # 将subQ添加到QLines中
                    self.QLines.append(subQ)
                    # 清空 subQ
                    subQ = []
                    q_idx += 1  # 问题索引加1
                else:
                    subQ.append(line)  # 将问题行添加到subQ中
                    # 将问题行的标志位设置为True
                    _is_Qline = True
                    _is_Aline = False

            elif line.startswith('A' + str(digits)):
                digits = line.split('A')[1].split(':')[0]  # 获取A后面的数字, 一般形式为A+数字+;+空格+回答内容
                # 去除开头的Q/A+数字+;+空格
                line = line.split(':')[1]
                # 在line的开头加三个空格，作为缩进
                line = '  ' + line
                if backline1 == '\n' and backline2 == '\n':
                    # 说明此时的line是回答行的最后一行
                    subA.append(line)
                    # 重置标志位
                    _is_Qline = False
                    _is_Aline = False
                    # 将subA添加到ALines中
                    self.ALines.append(subA)
                    # 清空 subA
                    subA = []
                    a_idx += 1
                else:
                    subA.append(line)  # 将回答行添加到subA中
                    # 将问题行的标志位设置为True
                    _is_Qline = False
                    _is_Aline = True
            else:
                if _is_Qline:
                    # 如果backline1是以A+数字开头的，则说明该行为问题行的最后一行
                    if backline1.startswith('A'):   # 说明此时的line是问题行的最后一行
                        # 说明此时的line是问题行的最后一行
                        subQ.append(line)
                        # 重置标志位
                        _is_Qline = False
                        _is_Aline = False
                        # 将subQ添加到QLines中
                        self.QLines.append(subQ)
                        # 清空 subQ
                        subQ = []
                        q_idx += 1  # 问题索引加1
                    else:   # 说明Qline还没结束
                        subQ.append(line)
                        _is_Qline = True
                        _is_Aline = False

                if _is_Aline:
                    # 如果backline1和backline2都是空行，则说明该行为回答行的最后一行
                    if backline1 == '\n' and backline2 == '\n':
                        # 说明此时的line是回答行的最后一行
                        subA.append(line)
                        # 重置标志位
                        _is_Qline = False
                        _is_Aline = False
                        # 将subA添加到ALines中
                        self.ALines.append(subA)
                        # 清空 subA
                        subA = []
                        a_idx += 1
                    else:   # 说明Aline还没结束
                        subA.append(line)
                        _is_Qline = False
                        _is_Aline = True
            idx += 1
        # 遍历完成后，QLines和ALines中的元素个数应该是一样的
        assert len(self.QLines) == len(self.ALines)
        # QList 和 AList 加到 QA 中
        self.QA.append(self.QLines)
        self.QA.append(self.ALines)
        print("QList和AList加到QA中完成！")


    # 用函数实现写入md文件
    def WriteToMd(self):
        self.EmbeddingList()

        # 如果self.Md_path存在，那么先将其移动到history文件夹中
        if not os.path.exists(self.Md_path):
            # 如果self.Md_path不存在，那么直接创建
            # 创建一个新的md文件
            with open(self.Md_path, 'w', encoding='utf-8') as f:
                # 向文件中写入标题
                f.write('# Title\n\n')
                # 写入小标题
                f.write('## 1. Introduction\n\n')
                f.write('The purpose of this document is to provide a comprehensive overview of the'
                        'questions and answers on the ChatGPT. \n'
                        'The document is structured as follows: Section 2 provides a summary of the questions and answers.'
                        'The document concludes with a list of references used to prepare this summary.'
                        '\n\n')
        else:
            # 先创建history文件夹
            self.CreateFolder(self.history_path)
            # 首先获取原始文件名
            md_name = self.Md_path.split('/')[-1].split('.')[0]  # 去掉路径，去掉后缀
            # 获取当前日期并将其格式化为年月日格式
            current_date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")  # 获取当前时间
            # 去掉年份中前面的'20'
            current_date = current_date[2:]
            # 其次在这个文件名后面加上时间戳
            md_name = md_name + '_' + current_date + '.md'  # 加上时间戳
            # 最后将文件复制到history文件夹中，注意是复制，不是移动
            # os.rename(self.Md_path, self.history_path + md_name)
            shutil.move(self.Md_path, self.history_path + md_name)
            # 创建一个新的md文件
            with open(self.Md_path, 'w', encoding='utf-8') as f:
                # 向文件中写入标题
                f.write('# ChatGPT Q&A Record\n\n')
                # 写入小标题
                f.write('\n## 1. Introduction\n\n')
                f.write('   The purpose of this document is to provide a comprehensive overview of the'
                        'questions and answers on the ChatGPT. \n'
                        'The document is structured as follows: Section 1 provides a '
                        'summary of the questions and answers.'
                        'Section 2 provides the specific questions and answers. '
                        'The document concludes with a list of references used to prepare this summary.'
                        '\n\n')
                f.write('## 2. Q&A\n\n')

        # 遍历读取QA中的内容，追加写入到md文件中
        with open(self.Md_path, 'a', encoding='utf-8') as f:
            # 添加问题索引
            f.write('\n### Section 1: Questions Index. \n\n')
            for i in range(len(self.QA[0])):
                f.write('#### [Q' + str(i + 1) + ']' + '(#Q' + str(i + 1) + ')' + ':' + self.QA[0][i][0])
            f.write('\n\n')
            f.write('\n### Section 2: Specific Q&A. \n\n')
            for i in range(len(self.QA[0])):
                # 写入问题
                # f.write('#### Q' + str(i + 1) + ':' + self.QA[0][i][0])
                f.write('#### <a name = "Q' + str(i + 1) + '"></a>' + 'Q' + str(i + 1) + ':' + self.QA[0][i][0])
                # 写入回答
                for j in range(1, len(self.QA[0][i])):
                    f.write(self.QA[0][i][j])
                f.write('\n\n')
                f.write('#### A' + str(i + 1) + ': \n' + self.QA[1][i][0])
                # 写入回答
                for j in range(1, len(self.QA[1][i])):
                    f.write(self.QA[1][i][j])
                f.write('\n\n')


        # 最后将md文件复制一份到readme.md中
        shutil.copy(self.Md_path, self.readme_path)

# 设置参数parser
def parse_args():
    parser = argparse.ArgumentParser(description="organize")
    parser.add_argument('--path', type=str, default='./self-attention.txt')
    parser.add_argument('--TallyUpNum', type=bool, default=True, help='统计问题和回答数吗？')
    parser.add_argument('--Md_path', type=str, default='./self_attention.md', help='self_attention.md文件路径')
    parser.add_argument('--readme_path', type=str, default='./readme.md', help='readme.md文件路径')
    return parser.parse_args()


# __main__
if __name__ == '__main__':
    args = parse_args()
    organize = Organize(args)
    # organize.TallyUpNum()
    organize.WriteToMd()
    print('问题数为：', organize.Qnum)
    print('回答数为：', organize.Anum)
