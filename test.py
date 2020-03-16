import tkinter as tk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect('rdxgyms.db')

class GymApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('RDX Gym Management')
        self.configure(bg='#4834DF')
        self.geometry('825x550')
        l1 = tk.Label(self, text = 'Welcome to RDX Gym Centers', font=("Courier", 28, "bold"), bg='#4834DF').pack()
        container = tk.Frame(self, bg='#EAF0F1')
        container.pack(side="top", fill="both", expand = True, pady=10)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # for F in (Login, Menu, AddCustomer, AddPackage, ShowCustomers, ShowPackages, SearchCustomer, AddSubscription, AddPayment):
        for F in (Login, Menu, AddCustomer, AddPackage, ShowCustomers):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class Login(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self,parent)
        self.configure(bg='#4834DF')
        label = tk.Label(self, text = 'Sign In Here!', font=("Helvetica", 30, "italic"), bg='#4834DF').pack(pady=10, padx=10)
        username = tk.Label(self, text = 'Username', font=("Times", 24)).pack(pady=20)
        self.ev1 = tk.StringVar(value = 'Enter Username')
        e1 = tk.Entry(self, width = 50, textvariable = self.ev1, font=("Times", 20)).pack()
        password = tk.Label(self, text = 'Password', font=("Times", 24)).pack(pady=20)
        self.ev2 = tk.StringVar(value = 'Enter Password')
        e2 = tk.Entry(self, width = 50, textvariable = self.ev2, font=("Times", 20)).pack()
        b1 = tk.Button(self, text = 'Login', relief='raised', font=("Times", 18), width=10, command=self.authenticate).pack(pady=22)

    def authenticate(self):
        global conn
        flag = 0
        cur = conn.cursor()
        query = '''select * from managers'''
        cur.execute(query)
        r = cur.fetchall()
        for row in r:
            if self.ev1.get() == row[0] and self.ev2.get() == row[1]:
                print("Login Successful!")
                messagebox.showinfo('Login Successful', 'Welcome to RDX Gym Management System!!')
                flag = 1
                conn.commit()
                cur.close()
                return self.controller.show_frame(Menu)
        if flag == 0:
            print('Login Failed!')
            messagebox.askretrycancel('Login Failed', 'Error Authenticating, Please Try Again!!')
        conn.commit()
        cur.close()


class Menu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='#4834DF')
        label = tk.Label(self, text = 'Start Menu', font=("Helvetica", 30, "italic"), bg='#4834DF').pack(pady=2, padx=10)
        b1 = tk.Button(self, text = 'Add Customer', relief='raised', font=("Times", 18), width=20, command=lambda: controller.show_frame(AddCustomer)).pack(pady=4)
        b2 = tk.Button(self, text = 'Add Package', relief='raised', font=("Times", 18), width=20, command=lambda: controller.show_frame(AddPackage)).pack(pady=4)
        b3 = tk.Button(self, text = 'Show All Customers', relief='raised', font=("Times", 18), width=20, command=lambda: controller.show_frame(ShowCustomers)).pack(pady=4)
        b4 = tk.Button(self, text = 'Show All Packages', relief='raised', font=("Times", 18), width=20, command=lambda: controller.show_frame(Menu)).pack(pady=4)
        b5 = tk.Button(self, text = 'Search Customer', relief='raised', font=("Times", 18), width=20, command=lambda: controller.show_frame(Menu)).pack(pady=4)
        b6 = tk.Button(self, text = 'Add Subscription', relief='raised', font=("Times", 18), width=20, command=lambda: controller.show_frame(Menu)).pack(pady=4)
        b7 = tk.Button(self, text = 'Add Payment', relief='raised', font=("Times", 18), width=20, command=lambda: controller.show_frame(Menu)).pack(pady=4)


class AddCustomer(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='#4834DF')
        label = tk.Label(self, text = 'Add Customer', font=("Helvetica", 30, "italic"), bg='#4834DF').pack(pady=10, padx=10)
        self.custID = tk.IntVar(value = 'Enter Customer ID')
        customerID = tk.Entry(self, width = 50, textvariable = self.custID, font=("Times", 20)).pack(pady=12)
        self.nameVar = tk.StringVar(value = 'Enter Customer Name')
        name = tk.Entry(self, width = 50, textvariable = self.nameVar, font=("Times", 20)).pack(pady=12)
        self.phone = tk.StringVar(value = 'Enter Phone Number')
        phoneNo = tk.Entry(self, width = 50, textvariable = self.phone, font=("Times", 20)).pack(pady=12)
        self.date = tk.StringVar(value = 'Enter Joining Date')
        joiningDate = tk.Entry(self, width = 50, textvariable = self.date, font=("Times", 20)).pack(pady=12)
        b1 = tk.Button(self, text = 'Submit', relief='raised', font=("Times", 18), width=10, command=self.addCustomer).pack(pady=12)
        b2 = tk.Button(self, text = 'Menu', relief='raised', font=("Times", 18), width=10, command=lambda: controller.show_frame(Menu)).pack(pady=12)
        self.text = tk.StringVar(value = '')
        success = tk.Label(self, text = '', font=("Helvetica", 10, "italic"), bg='#4834DF', textvariable = self.text).pack(pady=6, padx=10)

    def addCustomer(self):
        global conn
        cur = conn.cursor()
        rec = (self.custID.get(), self.nameVar.get(), self.phone.get(), self.date.get())
        query = '''insert into customers values(?, ?, ?, ?)'''
        cur.execute(query, rec)
        conn.commit()
        cur.close()
        self.text.set("New Customer Added!!")

class AddPackage(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='#4834DF')
        label = tk.Label(self, text = 'Add Package', font=("Helvetica", 30, "italic"), bg='#4834DF').pack(pady=10, padx=10)
        self.packID = tk.IntVar(value = 'Enter Package ID')
        packageID = tk.Entry(self, width = 50, textvariable = self.packID, font=("Times", 20)).pack(pady=12)
        self.typeVar = tk.StringVar(value = 'Enter Package Type')
        type = tk.Entry(self, width = 50, textvariable = self.typeVar, font=("Times", 20)).pack(pady=12)
        self.facil = tk.StringVar(value = 'Enter Package Facilities')
        facilities = tk.Entry(self, width = 50, textvariable = self.facil, font=("Times", 20)).pack(pady=12)
        self.costVar = tk.IntVar(value = 'Enter Cost of Package')
        cost = tk.Entry(self, width = 50, textvariable = self.costVar, font=("Times", 20)).pack(pady=12)
        b1 = tk.Button(self, text = 'Submit', relief='raised', font=("Times", 18), width=10, command=self.addPackage).pack(pady=12)
        b2 = tk.Button(self, text = 'Menu', relief='raised', font=("Times", 18), width=10, command=lambda: controller.show_frame(Menu)).pack(pady=12)
        self.text = tk.StringVar(value = '')
        success = tk.Label(self, text = '', font=("Helvetica", 10, "italic"), bg='#4834DF', textvariable = self.text).pack(pady=6, padx=10)

    def addPackage(self):
        global conn
        cur = conn.cursor()
        rec = (self.packID.get(), self.typeVar.get(), self.facil.get(), self.costVar.get())
        query = '''insert into packages values(?, ?, ?, ?)'''
        cur.execute(query, rec)
        conn.commit()
        cur.close()
        self.text.set("New Package Added!!")

class ShowCustomers(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='#4834DF')
        label = tk.Label(self, text = 'List of Customers', font=("Helvetica", 30, "italic"), bg='#4834DF').pack(pady=16, padx=10)
        for i in range(self.countObjects()):
            self.custID = tk.IntVar(value = '')
            customerID = tk.Label(self, text = '', font=("Helvetica", 10, "italic"), bg='#4834DF', textvariable = self.custID).pack(padx=3)
            self.nameVar = tk.StringVar(value = '')
            name = tk.Label(self, text = '', font=("Helvetica", 10, "italic"), bg='#4834DF', textvariable = self.nameVar).pack(padx=3)
            self.phone = tk.StringVar(value = '')
            phoneNo = tk.Label(self, text = '', font=("Helvetica", 10, "italic"), bg='#4834DF', textvariable = self.phone).pack(padx=3)
            self.date = tk.StringVar(value = '')
            joiningDate = tk.Label(self, text = '', font=("Helvetica", 10, "italic"), bg='#4834DF', textvariable = self.date).pack(padx=3)
            self.showCustomers(i)

    def countObjects(self):
        global conn
        cur = conn.cursor()
        query = '''select * from customers'''
        cur.execute(query)
        r = cur.fetchall()
        return len(r)

    def showCustomers(self, i):
        global conn
        cur = conn.cursor()
        query = '''select * from customers'''
        cur.execute(query)
        r = cur.fetchall()
        count = len(r)
        if count > 0:
            self.custID.set(r[i][0])
            self.nameVar.set(r[i][1])
            self.phone.set(r[i][2])
            self.date.set(r[i][3])
        else:
            messagebox.showinfo("List of Customers", "No customer records found.")


app = GymApp()
app.mainloop()
conn.close()
