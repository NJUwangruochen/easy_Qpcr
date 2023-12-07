import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt

window = tk.Tk()
window.title("Roche lightcycler 96 Programer v1.1")
window.geometry('800x700+350+50')

training_text = tk.Text(window,bd=3,width=15,height=48)
training_text.place(x=218,y=40)
label1 = tk.Label(window,text='Means',background='white',font=('Arial',12),width=8,height=1)
label1.place(x=235,y=10)
label1.configure(relief='solid')
label2 = tk.Label(window,text='Reference gene',font=('Arial',12),width=13,height=1)
label2.place(x=340,y=10)
label2.configure(relief='raised')
label3 = tk.Label(window,text='Interest gene',font=('Arial',12),width=12,height=1)
label3.place(x=470,y=10)
label3.configure(relief='raised')
label4 = tk.Label(window,text='Result',background='white',font=('Arial',12),width=10,height=1)
label4.place(x=590,y=10)
label4.configure(relief='solid')
label5 = tk.Label(window,text='number of control groups',font=('Arial',10),width=20,height=1)
label5.place(x=15,y=280)
label6 = tk.Label(window,text='repeat loading',font=('Arial',10),width=12,height=1)
label6.place(x=60,y=250)
text2 = tk.Text(window,bd=2,width=15,height=30)
text2.place(x=340,y=40)
text3 = tk.Text(window,bd=2,width=15,height=30)
text3.place(x=470,y=40)
text4 = tk.Text(window,bd=2,width=3,height=1)
text4.place(x=170,y=280)
text5 = tk.Text(window,bd=2,width=3,height=1)
text5.place(x=170,y=250)
analyzed_text = tk.Text(window,bd=3,width=13,height=30)
analyzed_text.place(x=588,y=40)
l1 = tk.Label(window,text='1',foreground='blue')
l1.place(x=202,y=39)
l2 = tk.Label(window,text='12',foreground='blue')
l2.place(x=197,y=182)
l3 = tk.Label(window,text='24',foreground='blue')
l3.place(x=197,y=338)
l4 = tk.Label(window,text='36',foreground='blue')
l4.place(x=197,y=494)
l5 = tk.Label(window,text='48',foreground='blue')
l5.place(x=197,y=650)

def open_file():
    file_path = filedialog.askopenfilename(initialdir="C:/Users/kolento/Desktop")
    data_list = []
    with open(file_path, "r", encoding='utf = 8') as file_objective:
        for line in file_objective:
            a = line.split()
            x = a[5]
            if x != 'Name':
                if x == '-':
                    data_list.append(0)
                elif x != '-':
                    data_list.append(x)
    return data_list


def data_training(list1):
    data_newlist = []
    n = 0
    judge = 0
    sum1 = 0
    str_n = text5.get('1.0', 'end').strip()
    if str_n:
        repeat_number = int(str_n)
    else:
        repeat_number = 2
    for data in list1:
        if data == 0:
            judge += 1
        sum1 += float(data)
        n = n + 1
        if n % repeat_number == 0 and n > 1:
            if repeat_number - judge != 0:
                x = round(float(sum1 / (repeat_number-judge)),3)
                data_newlist.append(x)
                sum1 = 0
                judge = 0
            elif repeat_number - judge == 0:
                data_newlist.append(0)
                sum1 = 0
                judge = 0
    return data_newlist


def show_data():
    list1 = open_file()
    list2 = data_training(list1)
    mean_text = '\n'.join([str(data) for data in list2])
    training_text.insert('end',mean_text)


def clear1():
    training_text.delete(1.0,'end')
    text4.delete(1.0,'end')
    text5.delete(1.0,'end')

def clear2():
    text2.delete(1.0,'end')
def clear3():
    text3.delete(1.0, 'end')
def clear4():
    analyzed_text.delete(1.0, 'end')

def distribute_value():
    ref_gene = text2.get('1.0', 'end').split()
    interest_gene = text3.get('1.0', 'end').split()
    gene_dict = {}
    if len(ref_gene) != len(interest_gene):
        tk.messagebox.showwarning(title='warning',message='Check whether the data in the two lists match!')
        return gene_dict
    else:
        for i in range(len(ref_gene)):
            gene_dict[ref_gene[i]] = interest_gene[i]
    return gene_dict


import math
# calculate delta Ct value
def delta(datalist):
    ct_delta = []
    for key,value in datalist.items():
        minus = float(value) -float(key)
        ct_delta.append(minus)
    return ct_delta


# calculate delta Ct value of control group
def average_control_group(ct_list,n):
    sum1 = 0
    for ct in ct_list[:n]:
        sum1 += ct
    ct_average = float(sum1 / n)
    return ct_average


# calculate delta—delta Ct value
def ddelta(ct_inter,ct_list,n):
    ct_ddelta = []
    for ct in ct_list[n:]:
        x = float(ct) - float(ct_inter)
        ct_ddelta.append(x)
    return ct_ddelta


# calculate relative expression level
def relative_calculate(ct_list):
    result_list= []
    for data in ct_list:
        x = math.pow(2,-float(data))
        result_list.append(x)
    return result_list

def result_output():
    origin_data = distribute_value()
    list1 = delta(origin_data)
    str_n = text4.get('1.0', 'end').strip()
    if str_n:
        n = int(str_n)
    else:
        n = 3
    ct_inter = average_control_group(list1,n=n)
    ct_ddelta = ddelta(ct_inter,list1,n=n)
    final = relative_calculate(ct_ddelta)
    final_mod = [round(data_n, 3) if abs(data_n) <= 1000 else 'NA' for data_n in final]
    text1 = '\n'.join([str(data) for data in final_mod])
    analyzed_text.insert('end', text1 + '\n\n')


button1 = tk.Button(window, text="Select file", command=show_data,width=10)
button1.place(x=65,y=150)
button2 = tk.Button(window,text="Clear",command=clear1,width=10)
button2.place(x=65,y=200)
button3 = tk.Button(window, text='Run',command=result_output,width=10)
button3.place(x=65,y=320)
button4 = tk.Button(window,text="Clear",command=clear2,width=10)
button4.place(x=355,y=440)
button5 = tk.Button(window,text="Clear",command=clear3,width=10)
button5.place(x=485,y=440)
button6 = tk.Button(window,text="Clear",command=clear4,width=10)
button6.place(x=598,y=440)
# button7 = tk.Button(window, text="regression analysis", command=open_new_window, width=10)
# button7.place(x=65, y=370)

window.mainloop()