import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt

# Window cannot be created again if main.py had created one
window = tk.Tk()

def open_new_window():
    new_window = tk.Toplevel(window)
    new_window.title("Standard curve fitting and regression analysis")
    new_window.geometry('600x400+500+200')

    # Standard curve fitting
    def standard_fit():
        rnas = text_conc.get('1.0','end').split()
        cts = text_ct.get('1.0','end').split()
        rnas1 = [float(rna) for rna in rnas]
        cts1 = [float(ct) for ct in cts]
        log_rnas = np.log2(rnas1)

        plt.scatter(log_rnas, cts1, color='blue')
        curve_fit = np.polyfit(log_rnas, cts1, 1)
        xfit = np.linspace(min(log_rnas), max(log_rnas), 1000)
        yfit = curve_fit[0] * xfit + curve_fit[1]
        r_sq = 1 - np.sum((cts1 - (curve_fit[0] * log_rnas + curve_fit[1])) ** 2) / ((len(cts1) - 1) * np.var(cts1, ddof=1))

        plt.plot(xfit, yfit, color='red', linestyle='--')
        plt.title('Standard Curve')
        plt.xlabel('log(RNA concentration)')
        plt.ylabel('Ct Value')

        # Add the equation and R^2
        equation = f'y = {curve_fit[0]:.2f}x + {curve_fit[1]:.2f}'
        r_squared = f'R^2 = {r_sq:.2f}'
        plt.text(0.65, 0.9, equation, transform=plt.gca().transAxes)
        plt.text(0.65, 0.85, r_squared, transform=plt.gca().transAxes)
        plt.show()
        text_equation.insert(1.0,equation)
        return curve_fit

    # regression analysis
    def regression_calculate():
        curve_fit = standard_fit()
        result_list = []
        data_list = text_y.get('1.0','end').split()
        for y in data_list:
            if int(y) >= 35:
                tk.messagebox.showwarning(title='warning',message='Some Ct values exceeded the lower limit of standard curve detection!')
        for y in data_list:
            x1 = (float(y) - curve_fit[1]) / curve_fit[0]
            x2 = 2 ** x1
            result_list.append(x2)
        text1 = '\n'.join([str(round(data,3)) for data in result_list])
        text_x.insert('end', text1 + '\n\n')


    def clear5():
        text_conc.delete(1.0,'end')
        text_ct.delete(1.0,'end')
        text_equation.delete(1.0,'end')

    def clear6():
        text_y.delete(1.0,'end')
        text_x.delete(1.0,'end')

    l11 = tk.Label(new_window,text='X(conc)',font=('Arial',10),width=15,height=1)
    l11.place(x=2,y=30)
    l12 = tk.Label(new_window, text='Y(Ct value)', font=('Arial', 10), width=12, height=1)
    l12.place(x=90, y=30)
    l13 = tk.Label(new_window, text='由Y计算X', font=('Arial', 10), width=20, height=1)
    l13.place(x=255, y=30)
    text_conc = tk.Text(new_window, bd=3, width=10,height=15)
    text_conc.place(x=20,y=50)
    text_ct = tk.Text(new_window, bd=3, width=10,height=15)
    text_ct.place(x=100,y=50)
    text_y = tk.Text(new_window,bd=3,width=10,height=15)
    text_y.place(x=300,y=50)
    text_equation = tk.Text(new_window,bd=3,width=20,height=1)
    text_equation.place(x=25,y=260)
    text_x = tk.Text(new_window,bd=3,width=10,height=15)
    text_x.place(x=500,y=50)
    b1 = tk.Button(new_window,text = "Generating standard curve",command=standard_fit,width=10)
    b1.place(x=200,y=100)
    b2 = tk.Button(new_window,text = "Clear",command=clear5,width=10)
    b2.place(x=200,y=140)
    b3 = tk.Button(new_window, text="Clear", command=clear6, width=10)
    b3.place(x=400, y=140)
    b4 = tk.Button(new_window, text="Run", command=regression_calculate, width=10)
    b4.place(x=400, y=100)