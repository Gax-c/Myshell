# utf-8 
import os 
import sys 
import time 
import multiprocessing 

tmp_file = '/tmp/myshell_tmpfile.txt'
help_file = 'help.txt'

class func :
    # 执行pwd命令
    def do_pwd(para = []) : 
        print(os.getcwd()) # 使用getpwd命令 

    # 执行clr/clear命令
    def do_clrclear(para = []) :
        if not para :
            # 清屏并将光标移动到左上角
            print("\033[1;1H\033[2J", end = "") 
        else :
            return -1 

    # 执行cd命令
    def do_cd(para = []) :
        # 如果没有参数就直接退出
        if not para : 
            return 
        # 如果参数数量正确
        elif len(para) == 1 :
            # 判断路径是否存在
            if os.path.exists(para[0]) :
                # 进入该路径
                os.chdir(para[0]) 
            else :
                print("该目录不存在！")
        # 如果参数数量过多
        else :
            return -1 

    # 执行time命令 
    def do_time(para = []) :
        if not para :
            t = time.time() # 得到当前的时间
            date = time.ctime(t) # 时间转化 
            print(date)
        else :
            return -1 

    # 执行umask命令
    def do_umask(para = []) :
        old_umask = 0 
        new_umask = 0
        # 设置new_umask为0来得到当前的umask
        old_umask = os.umask(new_umask) 
        # 将umask设置成原来的
        os.umask(old_umask) 
        if not para :
            # 前补0，输出3个八进制数 
            print("{:03o}".format(old_umask)) 
        elif len(para) == 1 : # 设置新的umask
            # 转化为八进制
            new_umask = int(para[0], 8) 
            os.umask(new_umask) 
        else :
            return -1 

    # 执行dir/ls命令
    def do_dirls(para = []) :
        # 没有参数就将参数设置为当前目录
        if not para : 
            para.append(os.getcwd()) 
        # 若在更新参数后只有一个参数，说明可以正确执行
        if len(para) == 1 :
            try:
                handler = os.listdir(para[0])
            except OSError:
                return -1 
            else :
                # 对每个文件进行遍历，从而去除隐藏文件 
                for elm in handler :
                    if not elm.startswith('.') : 
                        print(elm, end = ' ')
                print() 
        else :
            return -1 

    # 执行set命令
    def do_set(para = []) :
        if not para : 
            # 遍历所有的环境变量，加上等号输出
            for key, value in os.environ.items():
                print(key + "=" + value) 
        else :
            return -1 

    # 执行echo命令
    def do_echo(para = []) :
        # 每个字符串之间加入一个空格输出
        print(*para) 

    # 执行exec命令
    # 该函数需要在linux系统下执行，windows下会报错
    def do_exec(para = []) :
        try :
            # 用execvp来创建子进程进行执行
            os.execvp(para[0], para) 
        except FileNotFoundError: 
            return -1 

    # 执行test命令, 成立输出1，不成立输出0，-1表示出错
    def do_test(para = []) :
        res = 0 
        try :
            # 去除字符串可能存在的单引号或双引号
            para[0] = para[0].strip('"') 
            para[2] = para[2].strip('"') 
            para[0] = para[0].strip("'") 
            para[2] = para[2].strip("'") 
            # 判断是否是整数，是的话就转化成整数判断大小
            if para[0].isdigit() :
                para[0] = int(para[0]) 
                para[2] = int(para[2]) 
            # 根据-eq = 等符号完成判断
            if para[1] == '-eq' or para[1] == '=' or para[1] == '==' :
                res = 1 if para[0] == para[2] else 0 
            elif para[1] == '-ne' or para[1] == '!=' :
                res = 1 if para[0] != para[2] else 0 
            elif para[1] == '-gt' :
                res = 1 if para[0] > para[2] else 0  
            elif para[1] == '-lt' :
                res = 1 if para[0] < para[2] else 0  
            elif para[1] == '-ge' :
                res = 1 if para[0] >= para[2] else 0
            elif para[1] == '-le':
                res = 1 if para[0] <= para[2] else 0 
            print(res)
        except :
            # 若出现异常，则返回-1
            return -1 

    # 执行exit命令
    def do_exit(para = []) :
        if not para :
            quit() # 退出python程序
        else :
            return -1 

    # 执行fg命令
    def do_fg(para = []) :
        if para :
            return -1 
        # 找到最近的后台指令
        pos = -1 
        for i, elm in enumerate(process_list) :
            if not elm.fg and elm.pid != 0:
                pos = i
        if pos == -1 :
            print('没有可调度的后台进程！') 
            return 
        process_list[pos].fg = 1
        # 更新后续的后台进程编号
        for i in range(pos, len(process_list) - 1) :
            if not process_list[i+1].fg :
                process_list[i+1].bgid -= 1 
        bg_cnt.value -= 1 
        # 等待后台进程完成
        while find_process(process_list[pos].pid) != -1 :
            pass  
        
    # 执行bg命令
    def do_bg(para = []) :
        if para :
            return -1 
        # 找到最近的后台指令
        pos = -1 
        for i, elm in enumerate(process_list) :
            if not elm.fg and elm.pid != 0:
                pos = i
        if pos == -1 :
            print('没有可调度的后台进程！') 
            return 
        process_list[pos].fg = 1
        # 更新后续的后台进程编号
        for i in range(pos, len(process_list) - 1) :
            if not process_list[i+1].fg :
                process_list[i+1].bgid -= 1 
        bg_cnt.value -= 1
        # 等待后台进程完成
        while find_process(process_list[pos].pid) != -1 :
            pass  

    # 执行jobs命令
    def do_jobs(para = []) :
        # 遍历进程列表输出所有进程
        for elm in process_list :
            print('[{}] {}'.format(elm.pid, elm.name)) 

class process :
    def __init__(self) :
        self.pid = 0 # 进程号 
        self.name = '' # 进程名
        self.fg = 0 # 是否是前台进程
        self.bgid = 0 # 后台进程号

class command :
    def __init__(self) :
        self.para = [] # 命令的参数
        self.bg = 0 # 命令是否后台运行
        self.pipein = 0 # 命令是否有管道输入
        self.pipeout = 0 # 命令是否有管道输出
        self.rein = 0 # 命令是否有重定向输入
        self.reout = 0 # 命令是否有重定向输出
        self.reappend = 0 # 命令是否有重定向追加输出
        self.pathin = '' # 重定向的输入路径
        self.pathout = '' # 重定向的输出路径

# 进程初始化，创建root进程
def init_process() :
    root = process() 
    root.pid = 0 # pid号设置为0 
    root.name = 'myshell' 
    root.fg = 0 
    root.bgid = 0 
    root.pro = 0 
    process_list.append(root) # 将进程加入进程列表

# 查找特定pid号的进程
def find_process(pid) :
    for pos, elm in enumerate(process_list) :
        if elm.pid == pid : # pid相同则返回
            return pos 
    return -1 # 找不到相应的pid则返回-1

# 删除特定pid号的进程
def del_process(pid) :
    # 找到相应进程的编号
    k = find_process(pid) 
    if k != -1 :
        # 判断该进程是否是后台进程
        bg = 1 - process_list[k].fg 
        # 为之后的所有进程更新后台进程号
        for i in range(k, len(process_list) - 1) :
            if bg and process_list[i+1].fg == 0 :
                process_list[i+1].bgid -= 1 
            process_list[i] = process_list[i + 1] 
        process_list.pop() 
        # 更新后台进程总数
        if bg :
            bg_cnt.value -= 1 

def analysis(line) :
    com = command() 
    line = line.split() 
    for i, elm in enumerate(line) :
        # 若是'<'，则下一个元素为文件名
        if elm == '<' :
            com.rein = 1 
            com.pathin = line[i+1] 
            # 将'<'与文件名都删除
            del line[i] 
            del line[i] 
    for i, elm in enumerate(line) :
        # 若是'>'，则下一个元素为文件名
        if elm == '>' :
            com.reout = 1 
            com.pathout = line[i+1] 
            # 将'>'与文件名都删除
            del line[i] 
            del line[i] 
    for i, elm in enumerate(line) :
        # 若是'>>'，则下一个元素为文件名
        if elm == '>>' :
            com.reappend = 1 
            com.pathout = line[i+1] 
            # 将'>>'与文件名都删除
            del line[i] 
            del line[i] 
    for i, elm in enumerate(line) :
        # 若是'&'，则要置于后台运行
        if elm == '&' :
            com.bg = 1
            # 将'&'删除
            del line[i] 
    com.para = line.copy()  
    return com 

def execute_sys(para) :
    try :
        os.execvp(para[0], para) 
    except :
        print('命令错误！')

def execute(para) :
    if para[0] == 'pwd' :
        if func.do_pwd(para[1:]) == -1 :
            p = multiprocessing.Process(target = execute_sys, args = (para, )) 
            p.start() 
            p.join() 
    elif para[0] == 'clr' or para[0] == 'clear':
        if func.do_clrclear(para[1:]) == -1 :
            p = multiprocessing.Process(target = execute_sys, args = (para, )) 
            p.start() 
            p.join() 
    elif para[0] == 'cd' :
        if func.do_cd(para[1:]) == -1 :
            p = multiprocessing.Process(target = execute_sys, args = (para, )) 
            p.start() 
            p.join() 
    elif para[0] == 'time' :
        if func.do_time(para[1:]) == -1 :
            p = multiprocessing.Process(target = execute_sys, args = (para, )) 
            p.start() 
            p.join() 
    elif para[0] == 'umask' :
        if func.do_umask(para[1:]) == -1 :
            p = multiprocessing.Process(target = execute_sys, args = (para, )) 
            p.start() 
            p.join() 
    elif para[0] == 'dir' or para[0] == 'ls':
        if func.do_dirls(para[1:]) == -1 :
            p = multiprocessing.Process(target = execute_sys, args = (para, )) 
            p.start() 
            p.join() 
    elif para[0] == 'set' :
        if func.do_set(para[1:]) == -1 :
            p = multiprocessing.Process(target = execute_sys, args = (para, )) 
            p.start() 
            p.join() 
    elif para[0] == 'echo' :
        if func.do_echo(para[1:]) == -1 :
            p = multiprocessing.Process(target = execute_sys, args = (para, )) 
            p.start() 
            p.join() 
    elif para[0] == 'exec' :
        if func.do_exec(para[1:]) == -1 :
            os.execvp(para[0], para) 
    elif para[0] == 'test' :
        if func.do_test(para[1:]) == -1 :
            p = multiprocessing.Process(target = execute_sys, args = (para, )) 
            p.start() 
            p.join() 
    elif para[0] == 'exit' :
        if func.do_exit(para[1:]) == -1 :
            p = multiprocessing.Process(target = execute_sys, args = (para, )) 
            p.start() 
            p.join() 
    elif para[0] == 'fg' :
        if func.do_fg(para[1:]) == -1 :
            p = multiprocessing.Process(target = execute_sys, args = (para, )) 
            p.start() 
            p.join() 
    elif para[0] == 'bg' :
        if func.do_bg(para[1:]) == -1 :
            p = multiprocessing.Process(target = execute_sys, args = (para, )) 
            p.start() 
            p.join() 
    elif para[0] == 'jobs' :
        if func.do_jobs(para[1:]) == -1 :
            p = multiprocessing.Process(target = execute_sys, args = (para, )) 
            p.start() 
            p.join() 
    else :
        p = multiprocessing.Process(target = execute_sys, args = (para, )) 
        p.start() 
        p.join() 

def execute_back(com_list, bg_cnt) :
    pro = process() 
    bg_cnt.value += 1 
    pro.bgid = bg_cnt.value 
    pro.fg = 0 
    pro.name = com_list[0].para[0] 
    pro.pid = os.getpid()  
    process_list.append(pro) 
    for i, elm in enumerate(com_list) :
        file_out = None 
        # 重定向会覆盖管道输出 
        if elm.reout :
            # 打开文件并将其作为新的标准输出
            file_out = open(elm.pathout, 'w') 
            sys.stdout = file_out 
        elif elm.reappend :
            file_out = open(elm.pathout, 'a')  
            sys.stdout = file_out 
        elif elm.pipeout :
            # 打开临时文件并将其作为新的标准输出
            file_out = open(tmp_file, 'w') 
            sys.stdout = file_out 
        execute(elm.para) 
        if file_out != None :
            file_out.close() 
        sys.stdin = sys.__stdin__ 
        sys.stdout = sys.__stdout__ 
    pid = os.getpid() 
    if find_process(pid) != -1 :
        del_process(pid) 

def RUN(com_list) :
    # 没有任何参数则直接退出
    if len(com_list[0].para) == 0:
        return 
    if com_list[0].para[0] == 'help' :
        com_list[0].para[0] = 'more' 
        com_list[0].para.append(help_file) 
    # 如果某条指令存在管道输入，则为其添加上共享文件的参数
    for i, elm in enumerate(com_list) :
        # 重定向会覆盖管道输入 
        if elm.rein :
            com_list[i].para.append(elm.pathin) 
        elif elm.pipein :
            com_list[i].para.append(tmp_file) 
    # 如果需要前台运行 
    if not com_list[0].bg :
        for i, elm in enumerate(com_list) : 
            file_out = None 
            # 重定向会覆盖管道输出 
            if elm.reout :
                # 打开文件并将其作为新的标准输出
                file_out = open(elm.pathout, 'w') 
                sys.stdout = file_out 
            elif elm.reappend :
                file_out = open(elm.pathout, 'a')  
                sys.stdout = file_out 
            elif elm.pipeout :
                # 打开临时文件并将其作为新的标准输出
                file_out = open(tmp_file, 'w') 
                sys.stdout = file_out 
            execute(elm.para) 
            if file_out != None :
                file_out.close() 
            sys.stdin = sys.__stdin__ 
            sys.stdout = sys.__stdout__ 
    # 如果需要后台执行
    else :
        p = multiprocessing.Process(target = execute_back, args = (com_list, bg_cnt)) 
        p.start() 

def handle_command(line) :
    # 根据管道进行划分
    line = line.split('|') 
    com_list = [] 
    # 对管道中的每一部分进行处理
    for elm in line :
        com_list.append(analysis(elm.strip())) 
    if com_list[-1].bg :    
        for i, elm in enumerate(com_list) : 
            com_list[i].bg = 1 
    for i, elm in enumerate(com_list) :
        # 只有第一个没有管道输入
        if i > 0 :
            com_list[i].pipein = 1 
        # 只有最后一个没有管道输出
        if i != len(com_list) - 1 :
            com_list[i].pipeout = 1 
    RUN(com_list) 

if __name__ == '__main__' : 
    manager = multiprocessing.Manager() 
    process_list = manager.list([]) # 进程列表 
    bg_cnt = multiprocessing.Value('i', 0) # 后台进程数
    # 进行进程与信号初始化
    init_process() 
    # init_signal() 
    # 取出参数
    args = sys.argv[1:] 
    # 如果只有一个参数，即执行脚本
    if len(args) == 1 :
        # 打开文件
        with open(args[0], 'r') as file:
            lines = file.readlines() 
        for line in lines :
            # 去除换行符 
            line = line.rstrip('\n') 
            # 逐行显示执行了的命令 
            print('[root@myshell:{}]$ {}'.format(os.getcwd(), line)) 
            # 处理指令
            handle_command(line) 
    elif not args :
        # 无限循环读取指令
        while 1 :
            # 显示提示符
            promt = '[root@myshell:{}]$ '.format(os.getcwd()) 
            line = input(promt) 
            # 处理指令
            handle_command(line) 
    else :
        print('参数错误！') 