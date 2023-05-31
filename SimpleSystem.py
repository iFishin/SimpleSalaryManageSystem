import tkinter as tk
import tkinter.ttk as ttk
import  tkinter.messagebox as messagebox
import pymysql
import re

#使用的数据库地址
global em_host, em_user, em_password, em_database
em_host = 'localhost'
em_user = 'root'
em_password = 'fish'
em_database = 'employees'

class main_win():

    #重载数据
    def data_reload(self):
        #清空表
        for data in self.table.get_children():
            self.table.delete(data)
        # 载入数据
        con = pymysql.connect(host=em_host, user=em_user, password=em_password, database=em_database)
        cur = con.cursor()
        sql = """select a.employee_id,name,sex,age,unit,position,b.salary,basical_salary,welfare,award,unemployment_insurance,housing_provident_fund
                    from employee_info a inner join salary_info b 
                    on a.employee_id = b.employee_id"""
        cur.execute(sql)
        for data in cur.fetchall():
            # 将获取数据为None转化为空
            list_data =[]
            for index in range(len(data)):
                if data[index] == None:
                    list_data.append('')
                else:
                    list_data.append(data[index])
            print(list_data)
            self.table.insert('', 'end', values=list_data)

        cur.close()
        con.close()

    def __init__(self):
        self.window = tk.Tk()
        self.window.resizable(0,1)
        self.window.title("SimpleSalaryManageSystem")
        self.window.config(bg="#9DC8C8")
        # 设置窗口大小变量
        width = 800
        height = 400
        # 窗口居中，获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()
        size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.window.geometry(size_geo)

        main_menu = tk.Menu(self.window,selectcolor='#9DC8C8')
        main_menu.add_command(label="About?",command=lambda :messagebox.showinfo('About','数据库实践作业😆'))
        text = '右键可以调出辅助菜单'
        main_menu.add_command(label="Help?",command=lambda :messagebox.showinfo('Help',text))
        self.window.config(menu=main_menu)

        def pop(event):
            menuBar.post(event.x_root, event.y_root)
            print("Using subMenu!")
        def data_hide():
            str = ''
            for str in self.table.selection():
                item = self.table.item(str)
            self.table.delete(str)
        def data_fresh():
            self.data_reload()
            # 提示所有数据总数
            con = pymysql.connect(host=em_host, user=em_user, password=em_password, database=em_database)
            cur = con.cursor()
            cur.execute("select total_em()")
            total_em = cur.fetchall()[0][0]
            messagebox.showinfo('提示', '当前数据总人数为：{}'.format(total_em))

        # 右键菜单
        menuBar = tk.Menu(self.window, tearoff=False)
        menuBar.add_command(label="命令①：初始化主列表", command=lambda :data_fresh())
        menuBar.add_command(label="命令②：隐藏所选信息", command=lambda :data_hide())
        self.window.bind('<Button-3>',pop)

        self.query_btn = tk.Button(self.window, text="Query",command=lambda :self.fun_query())
        self.edit_btn = tk.Button(self.window, text="Edit",command=lambda :self.fun_edit())
        self.delete_btn = tk.Button(self.window, text="Delete",command=lambda :self.fun_delete())
        self.add_btn = tk.Button(self.window, text="Add",command=lambda :self.fun_add())

        self.query_btn.place(x=40, y=40, width=120)
        self.edit_btn.place(x=240, y=40, width=120)
        self.delete_btn.place(x=440, y=40, width=120)
        self.add_btn.place(x=640, y=40, width=120)
        # 滚动条
        xscrollbar = tk.Scrollbar(self.window, orient=tk.HORIZONTAL)
        xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        yscrollbar = tk.Scrollbar(self.window)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 表格控件
        heads = [['0', '工号'],
                 ['1', '姓名'],
                 ['2', '性别'],
                 ['3', '年龄'],
                 ['4', '单位'],
                 ['5', '职业'],
                 ['6', '薪水'],
                 ['7', '基本工资'],
                 ['8', '福利补贴'],
                 ['9', '奖励工资'],
                 ['10', '失业保险'],
                 ['11', '住房公积金']]
        self.table = ttk.Treeview(self.window,
                                  columns=heads,
                                  show="headings",
                                  xscrollcommand=xscrollbar.set,
                                  yscrollcommand=yscrollbar.set)
        for head in heads:
            self.table.heading(head[0], text=head[1], command=lambda _col=head[0]:sort_column(self.table,_col,False))

        # 表头点击排序事件
        def sort_column(tv,col,reverse):
            list_data = [(tv.set(k, col), k) for k in tv.get_children()]
            list_data.sort(reverse=reverse)
            for index, (val, k) in enumerate(list_data):
                tv.move(k, '', index)


        for column in heads:
            self.table.column(column[0], width=50, minwidth=50)

        self.table.place(x=0, y=120, width=782.6, height=280)
        #载入数据
        self.data_reload()

        def item_selected(event):
            item = ''
            for str in self.table.selection():
                item = self.table.item(str)
                print("select :",end="")
                print(item["values"])
        #双击查看详细信息
        def item_double_click(event):
            print("double click!")
            info_em = Employee_info()
            info_em.btn_0.destroy()
            item = ''
            for str in self.table.selection():
                item = self.table.item(str)
            print("edit:", end='')
            print(item["values"])
            item = item["values"]
            # 将获取数据为None转化为空
            for index in range(len(item)):
                if item[index] == "None":
                    item[index] = ""
                else:
                    pass

            info_em.combobox_sex.destroy()
            info_em.combobox_unit.destroy()
            info_em.combobox_position.destroy()

            info_em.entry_sex = tk.Entry(info_em.window, width=15, font=('楷体', 18), bg="#519D9E")
            info_em.entry_sex.place(x=160, y=60)
            info_em.entry_unit = tk.Entry(info_em.window, width=15, font=('楷体', 18), bg="#519D9E")
            info_em.entry_unit.place(x=160, y=140)
            info_em.entry_position = tk.Entry(info_em.window, width=15, font=('楷体', 18), bg="#519D9E")
            info_em.entry_position.place(x=160, y=180)

            info_em.entry_name.insert(0, item[1])
            info_em.entry_name["state"] = "disable"
            info_em.entry_sex.insert(0, item[2])
            info_em.entry_sex["state"] = "disable"
            info_em.entry_age.insert(0, item[3])
            info_em.entry_age["state"] = "disable"
            info_em.entry_unit.insert(0, item[4])
            info_em.entry_unit["state"] = "disable"
            info_em.entry_position.insert(0, item[5])
            info_em.entry_position["state"] = "disable"
            info_em.entry_salary.insert(0, item[6])
            info_em.entry_salary["state"] = "disable"
            info_em.entry_subsalary_basis.insert(0, item[7])
            info_em.entry_subsalary_basis["state"] = "disable"
            info_em.entry_subsalary_welfare.insert(0, item[8])
            info_em.entry_subsalary_welfare["state"] = "disable"
            info_em.entry_subsalary_award.insert(0, item[9])
            info_em.entry_subsalary_award["state"] = "disable"
            info_em.entry_subsalary_insurance.insert(0, item[10])
            info_em.entry_subsalary_insurance["state"] = "disable"
            info_em.entry_subsalary_fund.insert(0, item[11])
            info_em.entry_subsalary_fund["state"] = "disable"

        self.table.bind('<<TreeviewSelect>>', item_selected)
        self.table.bind('<Double-Button-1>', item_double_click)

        self.window.mainloop()

    #主页 删除按钮事件
    def fun_delete(self):
        print("delete employee")
        item = ''
        str = ''
        for str in self.table.selection():
            item = self.table.item(str)
            print(item["values"])
        print("delete id:")
        print(item["values"][0])
        result_ack = messagebox.askyesno(title="确认",message="是否删除 {} 所有信息？".format(item["values"][1]))
        if result_ack == True:
            con = pymysql.connect(host=em_host, user=em_user, password=em_password, database=em_database)
            cur = con.cursor()
            sql = "delete from employee_info where employee_id = {}".format(item["values"][0])
            cur.execute(sql)
            con.commit()
            cur.close()
            con.close()
            messagebox.showinfo(title="提示",message="删除成功！")
            self.table.delete(str)
        else :
            pass

    #主页 编辑按钮事件 注意薪水总和的计算 这里 注意将None转化为空
    def fun_edit(self):
        print("edit employee")
        self.window.state('iconic')
        item = ''
        for str in self.table.selection():
            item = self.table.item(str)
        print("edit:",end='')
        print(item["values"])
        item = item["values"]
        #将获取数据为None转化为空
        for index in range(len(item)):
            if item[index] == "None":
                item[index] = ""
            else :
                pass
        print(item)
        edit_em = Employee_info()
        edit_em.entry_name.insert(0,item[1])
        edit_em.combobox_sex.set(item[2])
        edit_em.entry_age.insert(0,item[3])
        edit_em.combobox_unit.set(item[4])
        edit_em.combobox_position.set(item[5])
        edit_em.entry_salary.insert(0,item[6])
        edit_em.entry_subsalary_basis.insert(0,item[7])
        edit_em.entry_subsalary_welfare.insert(0,item[8])
        edit_em.entry_subsalary_award.insert(0,item[9])
        edit_em.entry_subsalary_insurance.insert(0,item[10])
        edit_em.entry_subsalary_fund.insert(0,item[11])
        edit_em.btn_0["command"] = lambda: fun_edit_button_confirm()
        def fun_cancel_button():
            edit_em.window.destroy()
            self.window.state("normal")
        edit_em.btn_1["command"] = lambda:fun_cancel_button()

        #编辑页 菜单 帮助
        edit_em.main_menu.delete(2)
        text = '● 下拉框右键可以添加新的栏目\n● 某些下拉框点按鼠标滚轮可以置空\n● salary栏会自动计算并覆盖\n● 含数字项置空无法添加'
        edit_em.main_menu.add_command(label="help?",command=lambda :messagebox.showinfo('帮助',text))

        #详情页 确认按钮
        def fun_edit_button():

            edit_data = []
            edit_data.append(edit_em.entry_name.get())
            edit_data.append(edit_em.combobox_sex.get())
            edit_data.append(edit_em.entry_age.get())
            edit_data.append(edit_em.combobox_unit.get())
            edit_data.append(edit_em.combobox_position.get())
            edit_data.append(edit_em.entry_subsalary_basis.get())
            edit_data.append(edit_em.entry_subsalary_welfare.get())
            edit_data.append(edit_em.entry_subsalary_award.get())
            edit_data.append(edit_em.entry_subsalary_insurance.get())
            edit_data.append(edit_em.entry_subsalary_fund.get())
            # edit_data.append(add_em.entry_salary.get())

            #数字项为空置0
            cnt = 5
            if edit_data[2] == '':
                edit_data[2]='0'
            while True:
                if cnt>9:
                    break
                if edit_data[cnt] == '':
                    edit_data[cnt]='0'
                cnt += 1

            # 判断salary合法性，直接计算salary覆盖
            temp = eval(edit_data[5]) + eval(edit_data[6]) + eval(edit_data[7]) - eval(edit_data[8]) - eval(
                edit_data[9])
            print(type(temp))
            edit_data.append(temp)
            edit_em.entry_salary.delete(0, 'end')
            edit_em.entry_salary.insert(0, edit_data[10])

            con = pymysql.connect(host=em_host, user=em_user, password=em_password, database=em_database)
            cur = con.cursor()

            sql = """update employee_info set name="{}",sex="{}",age={},unit="{}",position="{}",salary={} where employee_id={};""".format(
                edit_data[0],\
                edit_data[1],\
                edit_data[2],\
                edit_data[3],\
                edit_data[4],\
                edit_data[10],\
                item[0])
            # ----
            print(sql)
            cur.execute(sql)
            sql = """update salary_info 
                    set basical_salary={},welfare={},award={},unemployment_insurance={},housing_provident_fund={},salary={} where employee_id={};""".format(\
                edit_data[5],\
                edit_data[6],\
                edit_data[7],\
                edit_data[8],\
                edit_data[9],\
                edit_data[10],\
                item[0])
            # ---
            cur.execute(sql)
            con.commit()
            print(sql)
            # all = cur.fetchall()
            # print(all)
            cur.close()
            con.close()

        def fun_edit_button_confirm():
            result = messagebox.askyesno(title="提示",message="确认修改 {} 信息？".format(item[1]))
            if result == True:
                fun_edit_button()
                self.data_reload()
                edit_em.window.destroy()
                self.window.state('normal')
            else:
                pass

    #主页 添加按钮事件  为空则无法插入（解决）
    def fun_add(self):
        self.window.state('iconic')
        add_em = Employee_info()
        def fun_cancel_button():
            add_em.window.destroy()
            self.window.state('normal')
        add_em.btn_0["command"] = lambda :fun_add_button_confirm()
        add_em.btn_1["command"] = lambda :fun_cancel_button()

        #添加页 菜单 帮助
        add_em.main_menu.delete(2)
        text = '● 下拉框右键可添加新栏目\n● 某些下拉框点按鼠标滚轮可以置空\n● salary栏会自动计算并覆盖\n● 含数字项无法添加'
        add_em.main_menu.add_command(label="help?",command=lambda :messagebox.showinfo('提示',text))

        def fun_add_button():
            print("add employee")
            con = pymysql.connect(host=em_host, user=em_user, password=em_password, database=em_database)
            cur = con.cursor()

            add_data = []
            add_data.append(add_em.entry_name.get())
            add_data.append(add_em.combobox_sex.get())
            add_data.append(add_em.entry_age.get())
            add_data.append(add_em.combobox_unit.get())
            add_data.append(add_em.combobox_position.get())
            add_data.append(add_em.entry_subsalary_basis.get())
            add_data.append(add_em.entry_subsalary_welfare.get())
            add_data.append(add_em.entry_subsalary_award.get())
            add_data.append(add_em.entry_subsalary_insurance.get())
            add_data.append(add_em.entry_subsalary_fund.get())
            #add_data.append(add_em.entry_salary.get())

            #数字项为空置0
            cnt = 5
            if add_data[2] == '':
                add_data[2]='0'
            while True:
                if cnt>9:
                    break
                if add_data[cnt] == '':
                    add_data[cnt]='0'
                cnt += 1

            #判断salary合法性，直接计算salary覆盖
            temp = eval(add_data[5])+eval(add_data[6])+eval(add_data[7])-eval(add_data[8])-eval(add_data[9])
            add_data.append(temp)
            add_em.entry_salary.delete(0,'end')
            add_em.entry_salary.insert(0,add_data[10])

            sql = "select employee_id from employee_info order by employee_id desc limit 1;"
            cur.execute(sql)
            final_id = cur.fetchall()[0][0]
            print(type(final_id))
            final_id += 1

            sql = """insert into employee_info(employee_id,name,sex,age,unit,position,salary) values({},"{}","{}",{},"{}","{}",{});""".format(
                final_id,\
                add_data[0], \
                add_data[1], \
                add_data[2], \
                add_data[3], \
                add_data[4], \
                add_data[10])
            print(sql)
            cur.execute(sql)
            sql = """update salary_info 
                    set basical_salary={},welfare={},award={},unemployment_insurance={},housing_provident_fund={},salary={} where employee_id={};""".format(
                add_data[5], \
                add_data[6], \
                add_data[7], \
                add_data[8], \
                add_data[9], \
                add_data[10],\
                final_id)
            cur.execute(sql)
            con.commit()
            print(sql)
            cur.close()
            con.close()

        def fun_add_button_confirm():
            result = messagebox.askyesno(title="提示", message="确认添加 {} 信息？".format(add_em.entry_name.get()))
            if result == True:
                fun_add_button()
                self.data_reload()
                add_em.window.destroy()
                self.window.state('normal')
            else:
                pass

    #主页查询按钮
    def fun_query(self):
        print("query employee")
        self.window.state('iconic')
        query_em = Employee_info()
        query_em.btn_0["command"] = lambda :fun_query_button()
        query_em.btn_0["text"] = "Query"
        def fun_cancel_button():
            query_em.window.destroy()
            self.window.state("normal")
        query_em.btn_1["command"] = lambda :fun_cancel_button()
        query_em.entry_salary.bind('<FocusIn>',lambda a:print('focusin'))
        query_em.combobox_sex.bind('<Button-2>',lambda e:query_em.combobox_sex.set(''))

        #查询页 菜单 帮助
        query_em.main_menu.delete(2)
        text = '● 下拉框右键可添加新栏目\n● 某些下拉框点按鼠标滚轮可以置空\n● salary栏会自动计算并覆盖\n● 含数字项无法添加'
        query_em.main_menu.add_command(label="help?",command=lambda :messagebox.showinfo('提示',text))

        #更新组件
        temp = query_em.geo_win(450,600)
        temp = re.findall('\d+',temp)
        temp[2] = str(eval(temp[2])+400)
        temp = temp[0]+"x"+temp[1]+"+"+temp[2]+"+"+temp[3]
        query_em.window.geometry(temp)
        temp = query_em.geo_win(800, 400)
        temp = re.findall('\d+', temp)
        temp[2] = str(eval(temp[2]) - 200)
        temp = temp[0] + "x" + temp[1] + "+" + temp[2] + "+" + temp[3]
        self.window.geometry(temp)
        #无法更新窗口位置
        self.window.update()


        query_em.combobox_cmd_age = ttk.Combobox(query_em.window,width=2,values=['=','-','>','≥','<','≤','≠'], state='readonly', font=('楷体', 15), background="#519D9E")
        query_em.combobox_cmd_age.place(x=160, y=100)
        query_em.entry_age.place(x=210, y=100)
        query_em.combobox_cmd_age.current(0)
        query_em.combobox_cmd_salary = ttk.Combobox(query_em.window,width=2,values=['=','-','>','≥','<','≤','≠'], state='readonly', font=('楷体', 15), background="#519D9E")
        query_em.combobox_cmd_salary.place(x=160, y=440)
        query_em.entry_salary.place(x=210, y=440)
        query_em.combobox_cmd_salary.current(0)
        query_em.combobox_cmd_basis = ttk.Combobox(query_em.window,width=2,values=['=','-','>','≥','<','≤','≠'], state='readonly', font=('楷体', 10), background="#519D9E")
        query_em.combobox_cmd_basis.place(x=285, y=240)
        query_em.entry_subsalary_basis.place(x=325, y=240)
        query_em.combobox_cmd_basis.current(0)
        query_em.combobox_cmd_welfare = ttk.Combobox(query_em.window,width=2,values=['=','-','>','≥','<','≤','≠'], state='readonly', font=('楷体', 10), background="#519D9E")
        query_em.combobox_cmd_welfare.place(x=285, y=280)
        query_em.entry_subsalary_welfare.place(x=325, y=280)
        query_em.combobox_cmd_welfare.current(0)
        query_em.combobox_cmd_award = ttk.Combobox(query_em.window,width=2,values=['=','-','>','≥','<','≤','≠'], state='readonly', font=('楷体', 10), background="#519D9E")
        query_em.combobox_cmd_award.place(x=285, y=320)
        query_em.entry_subsalary_award.place(x=325, y=320)
        query_em.combobox_cmd_award.current(0)
        query_em.combobox_cmd_insurance = ttk.Combobox(query_em.window,width=2,values=['=','-','>','≥','<','≤','≠'], state='readonly', font=('楷体', 10), background="#519D9E")
        query_em.combobox_cmd_insurance.place(x=285, y=360)
        query_em.entry_subsalary_insurance.place(x=325, y=360)
        query_em.combobox_cmd_insurance.current(0)
        query_em.combobox_cmd_fund = ttk.Combobox(query_em.window,width=2,values=['=','-','>','≥','<','≤','≠'], state='readonly', font=('楷体', 10), background="#519D9E")
        query_em.combobox_cmd_fund.current(0)
        query_em.combobox_cmd_fund.place(x=285, y=400)
        query_em.entry_subsalary_fund.place(x=325, y=400)
        query_em.btn_0.place(x=70, y=500)
        query_em.btn_1.place(x=250, y=500)

        def fun_query_button():
            sql = "select employee_id,name,sex,age,unit,position,salary,basical_salary,welfare,award,unemployment_insurance,housing_provident_fund from em_info where "

            query_data = []
            query_data.append(query_em.entry_name.get())
            query_data.append(query_em.combobox_sex.get())
            query_data.append(query_em.entry_age.get())
            query_data.append(query_em.combobox_unit.get())
            query_data.append(query_em.combobox_position.get())
            query_data.append(query_em.entry_subsalary_basis.get())
            query_data.append(query_em.entry_subsalary_welfare.get())
            query_data.append(query_em.entry_subsalary_award.get())
            query_data.append(query_em.entry_subsalary_insurance.get())
            query_data.append(query_em.entry_subsalary_fund.get())
            query_data.append(query_em.entry_salary.get())

            #解析下拉框符号
            def get_cmd(cmd_combobox):
                cmd = cmd_combobox.get()
                if cmd=='=':
                    return '='
                elif cmd=='-':
                    return '-'
                elif cmd=='>':
                    return '>'
                elif cmd=='≥':
                    return '>='
                elif cmd=='<':
                    return '<'
                elif cmd=='≤':
                    return '<='
                elif cmd=='≠':
                    return '!='


            #根据输入内容修改sql语句  解析输入框内容
            cnt = 0
            if query_data[0] != '':
                cnt+=1
                sql = sql + 'name="{}" and '.format(query_data[0])
            if query_data[1] != '':
                cnt += 1
                sql = sql + 'sex="{}" and '.format(query_data[1])
            if query_data[2] != '':
                cnt += 1
                cmd = get_cmd(query_em.combobox_cmd_age)
                if cmd != '-':
                    sql = sql + 'age{}{} and '.format(cmd,query_data[2])
                else:
                    num = query_data[2].split('-')
                    sql = sql + 'age between {} and {} and '.format(num[0],num[1])
            if query_data[3] != '':
                cnt += 1
                sql = sql + 'unit="{}" and '.format(query_data[3])
            if query_data[4] != '':
                cnt += 1
                sql = sql + 'position="{}" and '.format(query_data[4])
            if query_data[5] != '':
                cnt += 1
                cmd = get_cmd(query_em.combobox_cmd_basis)
                if cmd != '-':
                    sql = sql + 'basical_salary{}{} and '.format(cmd,query_data[5])
                else:
                    num = query_data[5].split('-')
                    sql = sql + 'basical_salary between {} and {} and '.format(num[0], num[1])
            if query_data[6] != '':
                cnt += 1
                cmd = get_cmd(query_em.combobox_cmd_welfare)
                if cmd != '-':
                    sql = sql + 'welfare{}{} and '.format(cmd,query_data[6])
                else:
                    num = query_data[6].split('-')
                    sql = sql + 'welfare between {} and {} and '.format(num[0], num[1])
            if query_data[7] != '':
                cnt += 1
                cmd = get_cmd(query_em.combobox_cmd_award)
                if cmd != '-':
                    sql = sql + 'award{}{} and '.format(cmd, query_data[7])
                else:
                    num = query_data[7].split('-')
                    sql = sql + 'award between {} and {} and '.format(num[0], num[1])
            if query_data[8] != '':
                cnt += 1
                cmd = get_cmd(query_em.combobox_cmd_insurance)
                if cmd != '-':
                    sql = sql + 'unemployment_insurance{}{} and '.format(cmd, query_data[8])
                else:
                    num = query_data[8].split('-')
                    sql = sql + 'unemployment_insurance between {} and {} and '.format(num[0], num[1])
            if query_data[9] != '':
                cnt += 1
                cmd = get_cmd(query_em.combobox_cmd_fund)
                if cmd != '-':
                    sql = sql + 'housing_provident_fund{}{} and '.format(cmd, query_data[9])
                else:
                    num = query_data[9].split('-')
                    sql = sql + 'housing_provident_fund between {} and {} and '.format(num[0], num[1])
            if query_data[10] != '':
                cnt += 1
                cmd = get_cmd(query_em.combobox_cmd_salary)
                if cmd != '-':
                    sql = sql + 'salary{}{} and '.format(cmd, query_data[10])
                else:
                    num = query_data[10].split('-')
                    sql = sql + 'salary between {} and {} and '.format(num[0], num[1])

            if cnt==0:
                sql = sql.rstrip(' where ')
                sql = sql + ';'
                print(sql)
            else:
                sql = sql.rstrip(' and ')
                sql = sql + ';'
                print(sql)

            #清空主页表格
            for data in self.table.get_children():
                self.table.delete(data)
            con = pymysql.connect(host=em_host, user=em_user, password=em_password, database=em_database)
            cur = con.cursor()
            cur.execute(sql)
            for data in cur.fetchall():
                self.table.insert('','end',values=data)

            #恢复窗口
            self.window.state('normal')

            cur.close()
            con.close()

#员工信息窗口
class Employee_info():

    def geo_win(self,width,height):
        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()
        size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        return size_geo

    def __init__(self):
        self.window = tk.Tk()
        self.window.resizable(0,0)
        self.window.geometry(self.geo_win(400,600))
        self.window.title("SimpleSalaryMangeSystem")
        self.window.config(bg="#9DC8C8")

        self.main_menu = tk.Menu(self.window,selectcolor="#9DC8C8")
        self.main_menu.add_command(label="About?",command=lambda: messagebox.showinfo('About', '数据库实践作业😆'))
        self.window.config(menu=self.main_menu)

        lab_name = tk.Label(self.window, text="Name: ", font=('楷体', 15), bg="#519D9E", width=10)
        lab_name.place(x=50, y=20)

        self.entry_name = tk.Entry(self.window, width=15, font=('楷体', 18), bg="#519D9E")
        self.entry_name.place(x=160, y=20)

        lab_sex = tk.Label(self.window, text="Sex: ", font=('楷体', 15), bg="#519D9E", width=10)
        lab_sex.place(x=50, y=60)
        self.combobox_sex = ttk.Combobox(self.window,width=14,values=['male','female'], state='readonly', font=('楷体', 18), background="#519D9E")
        self.combobox_sex.place(x=160,y=60)
        #self.entry_sex = tk.Entry(self.window, width=15, font=('楷体', 18), bg="#519D9E")
        #self.entry_sex.place(x=160, y=60)

        lab_age = tk.Label(self.window, text="Age: ", font=('楷体', 15), bg="#519D9E", width=10)
        lab_age.place(x=50, y=100)
        self.entry_age = tk.Entry(self.window, width=15, font=('楷体', 18), bg="#519D9E")
        self.entry_age.place(x=160, y=100)

        lab_unit = tk.Label(self.window, text="Unit: ", font=('楷体', 15), bg="#519D9E", width=10)
        lab_unit.place(x=50, y=140)
        self.combobox_unit = ttk.Combobox(self.window,width=14,values=['经理室','财务科','技术科','销售科'], state='readonly', font=('楷体', 18), background="#519D9E")
        self.combobox_unit.place(x=160, y=140)
        #self.entry_unit = tk.Entry(self.window, width=15, font=('楷体', 18), bg="#519D9E")
        #self.entry_unit.place(x=160, y=140)

        lab_position = tk.Label(self.window, text="Position: ", font=('楷体', 15), bg="#519D9E", width=10)
        lab_position.place(x=50, y=180)
        self.combobox_position = ttk.Combobox(self.window,width=14,values=['管理员工','财务员工','技术员工','销售员工'], state='readonly', font=('楷体', 18), background="#519D9E")
        self.combobox_position.place(x=160, y=180)
        #self.entry_position = tk.Entry(self.window, width=15, font=('楷体', 18), bg="#519D9E")
        #self.entry_position.place(x=160, y=180)

        # 其他工资来源
        lab_subsalary_basis = tk.Label(self.window, text="Basical Salary: ", font=('楷体', 10), bg="#519D9E", width=25)
        lab_subsalary_basis.place(x=100, y=240)
        self.entry_subsalary_basis = tk.Entry(self.window, width=10, font=('楷体', 13), bg="#519D9E")
        self.entry_subsalary_basis.place(x=285, y=240)

        lab_subsalary_welfare = tk.Label(self.window, text="Welfare: ", font=('楷体', 10), bg="#519D9E", width=25)
        lab_subsalary_welfare.place(x=100, y=280)
        self.entry_subsalary_welfare = tk.Entry(self.window, width=10, font=('楷体', 13), bg="#519D9E")
        self.entry_subsalary_welfare.place(x=285, y=280)

        lab_subsalary_award = tk.Label(self.window, text="Award: ", font=('楷体', 10), bg="#519D9E", width=25)
        lab_subsalary_award.place(x=100, y=320)
        self.entry_subsalary_award = tk.Entry(self.window, width=10, font=('楷体', 13), bg="#519D9E")
        self.entry_subsalary_award.place(x=285, y=320)

        lab_subsalary_insurance = tk.Label(self.window, text="Unemployment Insurance: ", font=('楷体', 10), bg="#519D9E",
                                           width=25)
        lab_subsalary_insurance.place(x=100, y=360)
        self.entry_subsalary_insurance = tk.Entry(self.window, width=10, font=('楷体', 13), bg="#519D9E")
        self.entry_subsalary_insurance.place(x=285, y=360)

        lab_subsalary_fund = tk.Label(self.window, text="Housing Provident Fund: ", font=('楷体', 10), bg="#519D9E", width=25)
        lab_subsalary_fund.place(x=100, y=400)
        self.entry_subsalary_fund = tk.Entry(self.window, width=10, font=('楷体', 13), bg="#519D9E")
        self.entry_subsalary_fund.place(x=285, y=400)

        # ~~~
        lab_salary = tk.Label(self.window, text="Salary: ", font=('楷体', 15), bg="#519D9E", width=10)
        lab_salary.place(x=50, y=440)
        self.entry_salary = tk.Entry(self.window, width=15, font=('楷体', 18), bg="#519D9E")
        self.entry_salary.place(x=160, y=440)

        def fun_focusin(event):
            result_salary = eval(self.entry_subsalary_basis.get()) + \
                            eval(self.entry_subsalary_award.get()) + \
                            eval(self.entry_subsalary_welfare.get()) - \
                            eval(self.entry_subsalary_insurance.get()) - \
                            eval(self.entry_subsalary_fund.get())
            self.entry_salary.delete(0,'end')
            self.entry_salary.insert(0,result_salary)
            self.entry_salary['state'] = 'disable'

        def fun_double_click(event):
            self.entry_salary['state'] = 'normal'

        self.entry_salary.bind("<Button-3>",fun_double_click)
        self.entry_salary.bind("<FocusIn>",fun_focusin)

        self.btn_0 = tk.Button(self.window, text="Confirm", font=('楷体', 15), bg="#519D9E", activebackground="#9DC8C8", width=13)
        self.btn_0.place(x=50, y=500)

        self.btn_1 = tk.Button(self.window, text="Cancel", font=('楷体', 15), bg="#519D9E", activebackground="#9DC8C8", width=13,
                          command=lambda :self.window.destroy())
        self.btn_1.place(x=210, y=500)

        #添加单位下拉框
        def add_unit(event):
            print("inserting")
            sub_add = Tiny_win()
            sub_add.window.title("添加单位")
            temp_add = ''
            def comfirm_btn():
                data = []
                temp_add = sub_add.entry.get()
                result = messagebox.askyesno('提示','确认添加单位：{}？'.format(temp_add))
                if result == True:
                    for temp in self.combobox_unit["value"]:
                        data.append(temp)
                    data.append(temp_add)
                self.combobox_unit["value"] = data
                sub_add.window.destroy()
            sub_add.btn["command"] = lambda :comfirm_btn()

        #添加职位下拉框
        def add_position(event):
            print("inserting")
            sub_add = Tiny_win()
            sub_add.window.title("添加单位")
            temp_add = ''
            def comfirm_btn():
                data = []
                temp_add = sub_add.entry.get()
                result = messagebox.askyesno('提示','确认添加职位：{}？'.format(temp_add))
                if result == True:
                    for temp in self.combobox_position["value"]:
                        data.append(temp)
                    data.append(temp_add)
                self.combobox_position["value"] = data
                sub_add.window.destroy()
            sub_add.btn["command"] = lambda :comfirm_btn()

        self.combobox_unit.bind('<Button-3>', add_unit)
        self.combobox_position.bind('<Button-3>', add_position)

        #双击下拉框置空
        def set_unit_none(event):
            self.combobox_unit.set('')
        def set_position_none(event):
            self.combobox_position.set('')

        self.combobox_unit.bind('<Button-2>', set_unit_none)
        self.combobox_position.bind('<Button-2>', set_position_none)

#小窗口
class Tiny_win():

    def __init__(self):
        self.window = tk.Tk()
        self.window.resizable(0, 0)
        width = 300
        height = 200
        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()
        size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.window.geometry(size_geo)
        self.window.config(bg="#9DC8C8")

        self.lab = tk.Label(self.window,text="输入：",font=('楷体', 15),bg="#519D9E",width=5)
        self.lab.place(x=60,y=50)
        self.entry = tk.Entry(self.window,width=10,font=('楷体', 18),bg="#519D9E")
        self.entry.place(x=120,y=50)
        self.btn = tk.Button(self.window,text="Comfirm",width=8,height=1,font=('楷体', 15),bg="#519D9E",activebackground="#9DC8C8")
        self.btn.place(x=110,y=120)

#登录窗口（粗）
class LoginWin():

    #登录验证
    def login_active(self):
        # loginwin.destroy()
        input_account = self.entry_account.get()
        input_password = self.entry_password.get()

        con = pymysql.connect(host=em_host, user=em_user, password=em_password, database=em_database)
        cur = con.cursor()
        cur.execute("""call account_judge("{}","{}")""".format(input_account,input_password))
        if cur.fetchall()[0][0] == 1:
            loginwin.destroy()
            main_win()
        else:
            tk.messagebox.showerror(title="Error", message="Not invalidate!")

    def __init__(self):
        global loginwin
        loginwin = tk.Tk()
        loginwin.title("SimpleSalaryManageSystem")
        loginwin.config(bg="#9dc8c8")
        loginwin.resizable(0, 0)
        # 设置窗口大小变量
        width = 400
        height = 300
        # 窗口居中，获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        screenwidth = loginwin.winfo_screenwidth()
        screenheight = loginwin.winfo_screenheight()
        size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        loginwin.geometry(size_geo)

        lab_title = tk.Label(loginwin, text="SimpleSalaryManageSystem", font=('楷体', 18, 'bold'), bg="#9DC8C8")
        lab_title.place(x=30, y=20, width=350, height=30)

        lab_account = tk.Label(loginwin, text="Account:  ", font=('楷体', 15), bg="#519D9E")
        lab_account.place(x=50, y=100)
        lab_password = tk.Label(loginwin, text="Password: ", font=('楷体', 15), bg="#519D9E")
        lab_password.place(x=50, y=150)

        self.entry_account = tk.Entry(loginwin, width=15, font=('楷体', 17), bg="#519D9E")
        self.entry_account.insert(0,"Administor")
        self.entry_account.place(x=160, y=100)
        self.entry_password = tk.Entry(loginwin, width=15, font=('楷体', 17), bg="#519D9E", show="●")
        self.entry_password.place(x=160, y=150)

        login_btn = tk.Button(loginwin, text="Login",
                              font=('楷体', 15),
                              bg="#519D9E",
                              activebackground="#9DC8C8",
                              command=self.login_active,
                              width=10,
                              height=2, )
        login_btn.place(x=150, y=200)

        self.entry_password.bind('<Return>',lambda e:self.login_active())

        loginwin.mainloop()


#程序入口
if __name__ == "__main__":
    global main_func
    LoginWin()





