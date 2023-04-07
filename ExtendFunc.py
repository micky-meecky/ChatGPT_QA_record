import os
import argparse
import shutil
import time
import datetime

class ExceptAIandEnglishSentenceMaker:
    def __init__(self, config):
        self.lines = None
        self.file = None
        self.path = config.path
        self.Md_path = config.Md_path
        self.readme_path = config.readme_path
        self.readme_flag = config.readme_flag
        self.task_type = config.task_type

        self.Promptnum = 0
        self.history_path = config.history_path

        self.Prompts = []
        self.Articles = []
        self.QLines = []
        self.WordsLines = []
        self.PhrasesLines = []

        self.Articlenum = 0
        self.QLinesnum = 0
        self.WordsLinesnum = 0
        self.PhrasesLinesnum = 0

        self.lines_shape = 0

 # 读取文件
    def ReadFile(self):
        self.file = open(self.path, 'r')
        # 获取文件内容的编码格式类型
        # q: 为什么要获取文件内容的编码格式类型？ a: 为了解决编码问题。
        print('文件编码格式为：', self.file.encoding)
        # q: 这一步是什么意思？ a: 读取文件中的所有行，存储在一个列表中。
        self.lines = self.file.readlines()
        self.lines_shape = len(self.lines)
        # 输出lines的形状大小
        print('lines的形状大小为：', len(self.lines))
        # q: lines是什么类型？ a: list类型。
        self.file.close()


# 统计问题回答数
    def TallyUpNum(self):
        self.ReadFile()
        Articledigits = 0
        Promptdigits = 0
        Qdigits = 0

        idx = 0
        for line in self.lines:
            # 如果改行开头是以Q+数字开头的，并它的前两行是空行，那么该行就是问题行，问题数加1
            if idx == 0:
                foreline1 = ''
                foreline2 = ''
            elif idx == 1:
                foreline1 = ''
                foreline2 = self.lines[idx - 1]
            else:
                foreline1 = self.lines[idx - 1]
                foreline2 = self.lines[idx - 2]

            idx += 1
            if self.task_type == 'English_reading':
                if line.startswith('Article') and foreline1 == '\n' and foreline2 == '\n':
                    self.Articlenum += 1
                    # 获取Article后面的数字, 一般形式为Article+空格+数字+:+空格+内容
                    Articledigits = line.split('Article')[1].split(':')[0]
                    # 将数字转换为int类型
                    Articledigits = int(Articledigits)

                if line.startswith('Prompt') and foreline1 == '\n' and foreline2 == '\n':
                    self.Promptnum += 1
                    # 获取Prompt后面的数字, 一般形式为Prompt+空格+数字+:+空格+内容
                    Promptdigits = line.split('Prompt')[1].split(':')[0]
                    # 将数字转换为int类型
                    Promptdigits = int(Promptdigits)

                if line.startswith('Q') and foreline1 == '\n' and foreline2 == '\n':
                    self.QLinesnum += 1
                    # 获取Q后面的数字, 一般形式为Q+空格+数字+:+空格+内容
                    Qdigits = line.split('Q')[1].split(':')[0]
                    # 将数字转换为int类型
                    Qdigits = int(Qdigits)


                if line.startswith('Words') and foreline1 == '\n' and foreline2 == '\n':
                    self.WordsLinesnum += 1

                if line.startswith('Phrases') and foreline1 == '\n' and foreline2 == '\n':
                    self.PhrasesLinesnum += 1


        # 打印文本内容中的Article数
        print('Article\'s digits数为：', Articledigits)
        if Articledigits == self.Articlenum:  # 如果Article数和Article后面的数字相等，那么就是正确的Article数
            self.Articlenum = Articledigits
        else:
            print('Article数和Article后面的数字不相等，请检查！')

        # 打印文本内容中的Prompt数
        print('Prompt\'s digits数为：', self.Promptnum)
        if self.Promptnum == Promptdigits:  # 如果Prompt数和Prompt后面的数字相等，那么就是正确的Prompt数
            self.Promptnum = Promptdigits
        else:
            print('Prompt数和Prompt后面的数字不相等，请检查！')

        # 打印文本内容中的问题数
        print('Q\'s digits数为：', self.QLinesnum)
        if self.QLinesnum == Qdigits:  # 如果问题数和问题后面的数字相等，那么就是正确的问题数
            self.QLinesnum = Qdigits
        else:
            print('问题数和问题后面的数字不相等，请检查！')

        # 打印文本内容中的Words数
        print('Words\'s digits数为：', self.WordsLinesnum)

        # 打印文本内容中的Phrases数
        print('Phrases\'s digits数为：', self.PhrasesLinesnum)






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
        subQ = []  # 用于存储问题i中的行
        subprompt = []  # 用于存储prompt中的行
        subarticle = []  # 用于存储Article中的行
        subwords = []  # 用于存储words中的行
        subphrases = []  # 用于存储phrases中的行

        idx = 0  # 用于记录当前行的索引
        q_idx = 0  # 用于记录当前问题的索引
        prompt_idx = 0  # 用于记录当前prompt的索引
        Article_idx = 0  # 用于记录当前Article的索引
        words_idx = 0  # 用于记录当前words的索引
        phrases_idx = 0  # 用于记录当前phrases的索引

        digits = 0  # 用于记录当前行的数字
        in_prompt = False  # 用于判断当前行是不是在prompt中
        in_article = False  # 用于判断当前行是不是在article中
        in_Q = False  # 用于判断当前行是不是在问题中
        in_words = False  # 用于判断当前行是不是在words中
        in_phrases = False  # 用于判断当前行是不是在phrases中

        idx = 0  # 用于记录当前行的索引
        for line in self.lines:
            if idx >= 1:
                foreline1 = self.lines[idx - 1]
                if idx >= 2:
                    foreline2 = self.lines[idx - 2]
                else:
                    foreline2 = None
            else:
                foreline1 = None
                foreline2 = None

            # 获取后三行的内容
            if idx < self.lines_shape - 3:
                backline1 = self.lines[idx + 1]
                backline2 = self.lines[idx + 2]
                backline3 = self.lines[idx + 3]
            elif idx < self.lines_shape - 2:
                backline1 = self.lines[idx + 1]
                backline2 = self.lines[idx + 2]
                backline3 = ' '
            elif idx < self.lines_shape - 1:
                backline1 = self.lines[idx + 1]
                backline2 = ' '
                backline3 = ' '
            else:
                backline1 = ' '
                backline2 = ' '
                backline3 = ' '


            idx += 1

            # 开始检测prompt行
            if line.startswith('Prompt'):
                # 去除开头的Prompt
                line = line.split(':', 1)[1]
                # 获取prompt后面的数字, 一般形式为prompt+‘ ’+数字+:+空格+问题内容
                digits = line.split(' ')[1].split(':')[0]
                # 在line的开头加三个空格，作为缩进
                line = '  ' + line
                # 检测line中是否含有'{}', 如果有，那么就将其替换为'[]'
                if '{' in line:
                    line = line.replace('{', '%')
                if '}' in line:
                    line = line.replace('}', '%')
                if ':' in line:
                    line = line.replace(':', '. ')
                if '](' in line:
                    line = line.replace('](', '] (')

                if backline2.startswith('\n') and backline1.startswith('\n'):   # 如果后面两行都是空行, 那么就是prompt的第一行，也是最后一行
                    # 把这行加入到subprompt列表中
                    subprompt.append(line)
                    in_prompt = False   # 退出prompt中
                    if backline3.startswith('Q'):
                        # 如果下下下行是以Q+数字开头的，那么就把subprompt列表中的内容加入到subQ列表中
                        self.Prompts.append(subprompt)
                        # 清空subprompt列表
                        subprompt = []
                        prompt_idx += 1
                    else:
                        # 如果下下下行不是以Q+数字开头的，那么就把subprompt列表中的内容加到self.Prompts列表中
                        self.Prompts.append(subprompt)
                        # 清空subprompt列表
                        subprompt = []
                        prompt_idx += 1
                    continue
                else:
                    # 如果后面两行有任意一行不是空行，说明这行不是prompt的最后一行
                    # 把这行加入到subprompt列表中
                    subprompt.append(line)
                    in_prompt = True    # 设置为在prompt中
                    continue

            if in_prompt:   # 如果在prompt中，那么就把prompt中的行加入到subprompt列表中
                # 检测line中是否含有'{}', 如果有，那么就将其替换为'[]'
                if ':' in line:
                    line = line.replace(':', '. ')
                if '](' in line:
                    line = line.replace('](', '] (')
                if backline2.startswith('\n') and backline1.startswith('\n'):   # 若后面联行是空行，说明这行是这个prompt的最后一行
                    # 把这行加入到subprompt列表中
                    subprompt.append(line)
                    in_prompt = False   # 退出prompt中
                    # 如果下下下行是以Q+数字开头的，那么就把subprompt列表中的内容加入到subQ列表中
                    self.Prompts.append(subprompt)
                    # 清空subprompt列表
                    subprompt = []
                    prompt_idx += 1
                    continue
                else:
                    # 如果后面两行有任意一行不是空行，说明这行不是prompt的最后一行
                    # 把这行加入到subprompt列表中
                    subprompt.append(line)
                    in_prompt = True
                    continue

            # 开始检测article行
            if line.startswith('Article'):
                # 去除开头的Article
                line = line.split(':', 1)[1]
                # 获取article后面的数字, 一般形式为article+‘ ’+数字+:+空格+问题内容
                digits = line.split(' ')[1].split(':')[0]
                # 在line的开头加三个空格，作为缩进
                line = '  ' + line
                if '](' in line:
                    line = line.replace('](', '] (')

                in_article = True  # 设置为在article中

            if in_article:  # 如果在article中，那么就把article中的行加入到subarticle列表中
                if '](' in line:
                    line = line.replace('](', '] (')
                if backline2.startswith('\n') and backline1.startswith('\n'):   # 若后面联行是空行，说明这行是这个article的最后一行
                    # 把这行加入到subarticle列表中
                    subarticle.append(line)
                    in_article = False   # 退出article中
                    self.Articles.append(subarticle)
                    # 清空subarticle列表
                    subarticle = []
                    Article_idx += 1
                    continue
                else:
                    # 如果后面两行有任意一行不是空行，说明这行不是article的最后一行
                    # 把这行加入到subarticle列表中
                    subarticle.append(line)
                    in_article = True
                    continue

            # 开始检测Q&A行
            if line.startswith('Q'):
                digits = line.split('Q')[1].split(':')[0]  # 获取Q后面的数字, 一般形式为Q+数字+;+空格+问题内容
                # 去除开头的Q/A+数字+;
                line = line.split(':', 1)[1]
                # 在line的开头加三个空格，作为缩进
                line = '  ' + line
                if ':' in line:
                    line = line.replace(':', '. ')

                # Q 下面一行肯定是选项A，所以不用条件判断
                subQ.append(line)  # 将问题行添加到subQ中
                in_Q = True  # 设置为在问题中
                q_idx += 1  # 问题索引加1
                continue

            if in_Q:  # 如果在问题中，那么就把问题中的行加入到subQ列表中
                if ':' in line:
                    line = line.replace(':', '. ')
                if backline2.startswith('\n') and backline1.startswith('\n'):   # 若后面联行是空行，说明这行是这个问题的最后一行
                    # 把这行加入到subQ列表中
                    subQ.append(line)
                    in_Q = False   # 退出问题中
                    self.QLines.append(subQ)
                    # 清空subQ列表
                    subQ = []
                    q_idx += 1
                    continue
                else:
                    # 如果后面两行有任意一行不是空行，说明这行不是问题的最后一行
                    # 把这行加入到subQ列表中
                    subQ.append(line)
                    in_Q = True
                    continue

            # 开始检测Words summary行
            if line.startswith('Words summary'):
                # 去除开头的Words summary
                line = line.split(':', 1)[1].strip()
                # 在line的开头加三个空格，作为缩进
                line = '  ' + line
                if ':' in line:
                    line = line.replace(':', '. ')

                in_words = True  # 设置为在words中
                words_idx += 1  # words索引加1


            if in_words:  # 如果在words中，那么就把words中的行加入到subwords列表中
                if ':' in line:
                    line = line.replace(':', '. ')
                if backline2.startswith('\n') and backline1.startswith('\n'):   # 若后面联行是空行，说明这行是这个words的最后一行
                    # 把这行加入到subwords列表中
                    subwords.append(line)
                    in_words = False   # 退出words中
                    self.WordsLines.append(subwords)
                    # 清空subwords列表
                    subwords = []
                    words_idx += 1
                    continue
                else:
                    # 如果后面两行有任意一行不是空行，说明这行不是words的最后一行
                    # 把这行加入到subwords列表中
                    subwords.append(line)
                    in_words = True
                    continue

            # 开始检测Phrases summary行
            if line.startswith('Phrases summary'):
                # 去除开头的Phrases summary
                line = line.split(':', 1)[1]
                # 在line的开头加三个空格，作为缩进
                line = '  ' + line
                if ':' in line:
                    line = line.replace(':', '. ')

                in_phrases = True
                phrases_idx += 1

            if in_phrases:  # 如果在phrases中，那么就把phrases中的行加入到subphrases列表中
                if ':' in line:
                    line = line.replace(':', '. ')
                if backline2.startswith('\n') and backline1.startswith('\n'):   # 若后面联行是空行，说明这行是这个phrases的最后一行
                    # 把这行加入到subphrases列表中
                    subphrases.append(line)
                    in_phrases = False   # 退出phrases中
                    self.PhrasesLines.append(subphrases)
                    # 清空subphrases列表
                    subphrases = []
                    phrases_idx += 1
                    continue
                else:
                    # 如果后面两行有任意一行不是空行，说明这行不是phrases的最后一行
                    # 把这行加入到subphrases列表中
                    subphrases.append(line)
                    in_phrases = True
                    continue

    # 用函数实现写入md文件
    def WriteToMd(self):
        self.EmbeddingList()

        # 如果self.Md_path存在，那么先将其移动到history文件夹中
        if not os.path.exists(self.Md_path):
            # 如果self.Md_path不存在，那么直接创建
            if self.task_type == 'English_reading':
                # 创建一个新的md文件
                with open(self.Md_path, 'w', encoding='utf-8') as f:
                # 向文件中写入标题
                    f.write('# English Reading\n\n')
                    # 写入小标题
                    f.write('## 1. Introduction\n\n')
                    f.write('The purpose of this document is to make a comprehensive English reading which have to '
                            'involve an article which is give by user, some multiple-choice questions which are '
                            'made by ChatGPT, and some advanced words and phrase in the article as well as made by '
                            'ChatGPT. \n\n')
            else:
                print("task_type error")
                return None

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
                        'questions and answers on the ChatGPT. \nThe document is structured as follows: Section 1'
                        ' provides a summary of the questions and answers.Section 2 provides the specific questions '
                        'and answers. The document concludes with a list of references used to prepare this summary.'
                        '\n\n')
                # 写入一些必要的提示词，给CHatGPT使用
                f.write('## 2. Prompts\n\n')
                for i in range(len(self.Prompts)):
                    f.write('### Promp' + str(i + 1) + ': \n')
                    for j in range(len(self.Prompts[i])):
                        f.write(self.Prompts[i][j])  # 写入提示内容
                    f.write('\n\n')

                f.write('## 3. Q\n\n')
                for i in range(len(self.QLines)):
                    # 写入问题
                    f.write('### Q' + str(i + 1) + ': \n')
                    for j in range(len(self.QLines[i])):
                        f.write(self.QLines[i][j])  # 写入问题内容
                        f.write('\n')
                    f.write('\n\n')

                f.write('## 4. Words summary\n\n')
                for i in range(len(self.WordsLines)):
                    # 写入words行
                    f.write('### Words' + str(i + 1) + ': \n')
                    for j in range(len(self.WordsLines[i])):
                        f.write(self.WordsLines[i][j])
                        f.write('\n')
                    f.write('\n\n')

                f.write('## 5. Phrases summary\n\n')
                for i in range(len(self.PhrasesLines)):
                    # 写入phrases行
                    f.write('### Phrases' + str(i + 1) + ': \n')
                    for j in range(len(self.PhrasesLines[i])):
                        f.write(self.PhrasesLines[i][j])
                        f.write('\n')
                    f.write('\n\n')













