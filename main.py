import tkinter as tk
from tkinter import messagebox, ttk
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

        for F in (Login, Menu, AddCustomer, AddPackage, ShowCustomers, ShowPackages, SearchCustomer, AddSubscription, AddPayment):

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
        e2 = tk.Entry(self, width = 50, textvariable = self.ev2, font=("Times", 20))
        e2.pack()
        e2.config(show="*")
        b1 = tk.Button(self, text = 'Login', relief='raised', font=("Times", 18), width=10, command=self.authenticate).pack(pady=50)

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
        b4 = tk.Button(self, text = 'Show All Packages', relief='raised', font=("Times", 18), width=20, command=lambda: controller.show_frame(ShowPackages)).pack(pady=4)
        b5 = tk.Button(self, text = 'Search Customer', relief='raised', font=("Times", 18), width=20, command=lambda: controller.show_frame(SearchCustomer)).pack(pady=4)
        b6 = tk.Button(self, text = 'Add Subscription', relief='raised', font=("Times", 18), width=20, command=lambda: controller.show_frame(AddSubscription)).pack(pady=4)
        b7 = tk.Button(self, text = 'Add Payment', relief='raised', font=("Times", 18), width=20, command=lambda: controller.show_frame(AddPayment)).pack(pady=4)


class AddCustomer(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='#4834DF')
        label = tk.Label(self, text = 'Add Customer', font=("Helvetica", 30, "italic"), bg='#4834DF').pack(pady=10, padx=10)
        self.custID = tk.StringVar(value = 'Enter Customer ID')
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
        if not self.custID.get().isdigit():
            return messagebox.showwarning('Add Customer', 'Please enter valid customer ID!')
        elif self.nameVar.get() == '':
            return messagebox.showwarning('Add Customer', "Don't leave name entry blank!")
        elif len(self.phone.get()) != 10 or not self.phone.get().isdigit():
            return messagebox.showwarning('Add Customer', "Please enter valid phone number!")
        elif len(self.date.get()) != 11 or self.date.get().isdigit() or self.date.get().isalpha():
            return messagebox.showwarning('Add Customer', 'Please enter valid date in this format DD-MMM-YYYY!')
        else:
            rec = (int(self.custID.get()), self.nameVar.get(), self.phone.get(), self.date.get())
            query = '''insert into customers values(?, ?, ?, ?)'''
            cur.execute(query, rec)
            self.text.set("New Customer Added!!")
            conn.commit()
            cur.close()

class AddPackage(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='#4834DF')
        label = tk.Label(self, text = 'Add Package', font=("Helvetica", 30, "italic"), bg='#4834DF').pack(pady=10, padx=10)
        self.packID = tk.StringVar(value = 'Enter Package ID')
        packageID = tk.Entry(self, width = 50, textvariable = self.packID, font=("Times", 20)).pack(pady=12)
        self.typeVar = tk.StringVar(value = 'Enter Package Type')
        type = tk.Entry(self, width = 50, textvariable = self.typeVar, font=("Times", 20)).pack(pady=12)
        self.facil = tk.StringVar(value = 'Enter Package Facilities')
        facilities = tk.Entry(self, width = 50, textvariable = self.facil, font=("Times", 20)).pack(pady=12)
        self.costVar = tk.StringVar(value = 'Enter Cost of Package')
        cost = tk.Entry(self, width = 50, textvariable = self.costVar, font=("Times", 20)).pack(pady=12)
        b1 = tk.Button(self, text = 'Submit', relief='raised', font=("Times", 18), width=10, command=self.addPackage).pack(pady=12)
        b2 = tk.Button(self, text = 'Menu', relief='raised', font=("Times", 18), width=10, command=lambda: controller.show_frame(Menu)).pack(pady=12)
        self.text = tk.StringVar(value = '')
        success = tk.Label(self, text = '', font=("Helvetica", 10, "italic"), bg='#4834DF', textvariable = self.text).pack(pady=6, padx=10)

    def addPackage(self):
        global conn
        cur = conn.cursor()
        if not self.packID.get().isdigit():
            return messagebox.showwarning('Add Package', 'Please enter valid package ID!')
        elif self.typeVar.get() == '':
            return messagebox.showwarning('Add Package', "Don't leave type entry blank!")
        elif self.facil.get() == '':
            return messagebox.showwarning('Add Package', "Don't leave facilities entry blank!")
        elif not self.costVar.get().isdigit():
            return messagebox.showwarning('Add Package', 'Please enter valid cost!')
        else:
            rec = (int(self.packID.get()), self.typeVar.get(), self.facil.get(), int(self.costVar.get()))
            query = '''insert into packages values(?, ?, ?, ?)'''
            cur.execute(query, rec)
            self.text.set("New Package Added!!")
            conn.commit()
            cur.close()

class ShowCustomers(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='#4834DF')
        label = tk.Label(self, text = 'List of Customers', font=("Helvetica", 30, "italic"), bg='#4834DF').pack(padx=10)

        list1 = tk.Listbox(self, height=8, width=160, font=("Times", 28), bd = 6, relief='raised', bg='#1BCA9B', fg='#2C3335')
        list1.pack(padx=25, pady=8)
        b2 = tk.Button(self, text = 'Menu', relief='raised', font=("Times", 18), width=10, command=lambda: controller.show_frame(Menu)).pack(pady=8)
        self.view_command(list1)

    def showCustomers(self):
        global conn
        cur = conn.cursor()
        query = '''select * from customers'''
        cur.execute(query)
        r = cur.fetchall()
        count = len(r)
        if count > 0:
            return r
        else:
            messagebox.showinfo("List of Customers", "No customer records found.")

    def view_command(self, list1):
        list1.delete(0,tk.END)
        for row in self.showCustomers():
            list1.insert(tk.END,row)

class ShowPackages(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='#4834DF')
        label = tk.Label(self, text = 'List of Packages', font=("Helvetica", 30, "italic"), bg='#4834DF').pack(padx=10)

        list1 = tk.Listbox(self, height=8, width=160, font=("Times", 28), bd = 6, relief='raised', bg='#1BCA9B', fg='#2C3335')
        list1.pack(padx=25, pady=8)
        b2 = tk.Button(self, text = 'Menu', relief='raised', font=("Times", 18), width=10, command=lambda: controller.show_frame(Menu)).pack(pady=8)
        self.view_command(list1)

    def showPackages(self):
        global conn
        cur = conn.cursor()
        query = '''select * from packages'''
        cur.execute(query)
        r = cur.fetchall()
        count = len(r)
        if count > 0:
            return r
        else:
            messagebox.showinfo("List of Packages", "No package records found.")

    def view_command(self, list1):
        list1.delete(0,tk.END)
        for row in self.showPackages():
            list1.insert(tk.END,row)

class SearchCustomer(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='#4834DF')
        label = tk.Label(self, text = 'Search Customer by Name', font=("Helvetica", 30, "italic"), bg='#4834DF').pack(padx=10)
        self.custName = tk.StringVar(value = 'Enter Customer Name')
        customerName = tk.Entry(self, width = 50, textvariable = self.custName, font=("Times", 20)).pack(pady=12)
        list1 = tk.Listbox(self, height=5, width=160, font=("Times", 28), bd = 6, relief='raised', bg='#1BCA9B', fg='#2C3335')
        list1.pack(padx=25, pady=8)
        b1 = tk.Button(self, text = 'Search', relief='raised', font=("Times", 18), width=10, command=lambda: self.view_command(list1)).pack(pady=10)
        b2 = tk.Button(self, text = 'Menu', relief='raised', font=("Times", 18), width=10, command=lambda: controller.show_frame(Menu)).pack(pady=10)

    def searchCustomer(self):
        global conn
        cur = conn.cursor()
        q1 = '''select * from customers where name = ?'''
        cur.execute(q1, (self.custName.get(),))
        r1 = cur.fetchall()
        if len(r1) == 0:
            return messagebox.showinfo("Search Customer", "Customer not found!")
        elif len(r1) != 0:
            q2 = '''select * from subscriptions where custName = ?'''
            cur.execute(q2, (self.custName.get(),))
            r2 = cur.fetchall()
            if len(r2) == 0:
                return messagebox.showinfo("Search Customer", "Customer Found but not subscribed to any package!")
            else:
                messagebox.showinfo("Search Customer", "Subscribed Customer Found!")
                conn.commit()
                cur.close()
                return r2

    def view_command(self, list1):
        list1.delete(0,tk.END)
        for row in self.searchCustomer():
            list1.insert(tk.END,row)

class AddSubscription(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='#4834DF')
        months = ['01 Month', '03 Months', '06 Months', '12 Months', '24 Months']
        label = tk.Label(self, text = 'Add Subscription', font=("Helvetica", 30, "italic"), bg='#4834DF').pack(padx=10, pady=15)
        self.subsID = tk.StringVar(value = 'Enter Subscription ID')
        subscriptionID = tk.Entry(self, width = 50, textvariable = self.subsID, font=("Times", 20)).pack(pady=12)
        self.custName = tk.StringVar(value = 'Enter Customer Name')
        customerName = tk.Entry(self, width = 50, textvariable = self.custName, font=("Times", 20)).pack(pady=12)
        self.packID = tk.StringVar(value = 'Enter Package ID')
        packageID = tk.Entry(self, width = 50, textvariable = self.packID, font=("Times", 20)).pack(pady=12)
        self.monthVar = tk.StringVar(value = 'Select No. of Months')
        month = ttk.Combobox(self, width = 49, textvariable = self.monthVar, font=("Times", 20), values=months).pack(pady=18)
        b1 = tk.Button(self, text = 'Submit', relief='raised', font=("Times", 18), width=10, command=self.addSubscription).pack(pady=8)
        b2 = tk.Button(self, text = 'Menu', relief='raised', font=("Times", 18), width=10, command=lambda: controller.show_frame(Menu)).pack(pady=8)
        self.text = tk.StringVar(value = '')
        success = tk.Label(self, text = '', font=("Helvetica", 10, "italic"), bg='#4834DF', textvariable = self.text).pack(pady=6, padx=10)

    def addSubscription(self):
        global conn
        cur = conn.cursor()
        q1 = '''select * from customers where name = ?'''
        cur.execute(q1, (self.custName.get(),))
        r1 = cur.fetchall()
        q2 = '''select * from packages where packageID = ?'''

        if not self.subsID.get().isdigit():
            return messagebox.showwarning('Add Subscription', 'Please enter valid subscription ID!')
        elif len(r1) == 0:
            return messagebox.showwarning('Add Subscription', 'Customer Not Found!')
        elif not self.packID.get().isdigit():
            return messagebox.showwarning('Add Subscription', 'Please enter valid package ID!')
        elif self.monthVar.get() == 'Select No. of Months':
            return messagebox.showwarning('Add Subscription', 'Please select a option from dropdown menu!')
        else:
            cur.execute(q2, (int(self.packID.get()),))
            r2 = cur.fetchall()
            if len(r2) == 0:
                return messagebox.showwarning('Add Subscription', 'Package Not Found!')
            rec = (int(self.subsID.get()), self.custName.get(), int(self.packID.get()), int(self.monthVar.get()[0:2]))
            query = '''insert into subscriptions values(?, ?, ?, ?)'''
            cur.execute(query, rec)
            self.text.set("New Subscription Added!!")
            conn.commit()
            cur.close()

class AddPayment(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.configure(bg='#4834DF')
        label = tk.Label(self, text = 'Add Payment', font=("Helvetica", 30, "italic"), bg='#4834DF').pack(padx=10, pady=15)
        self.payID = tk.StringVar(value = 'Enter Payment ID')
        paymentID = tk.Entry(self, width = 50, textvariable = self.payID, font=("Times", 20)).pack(pady=12)
        self.custName = tk.StringVar(value = 'Enter Customer Name')
        customerName = tk.Entry(self, width = 50, textvariable = self.custName, font=("Times", 20)).pack(pady=12)
        self.invoice = tk.StringVar(value = '')
        invoiceBill = tk.Label(self, text = '', font=("Helvetica", 20, "italic"), bg='#4834DF', textvariable = self.invoice).pack(pady=12, padx=10)
        b1 = tk.Button(self, text = 'Submit', relief='raised', font=("Times", 18), width=10, command=self.addPayment).pack(pady=10)
        b2 = tk.Button(self, text = 'Menu', relief='raised', font=("Times", 18), width=10, command=lambda: controller.show_frame(Menu)).pack(pady=10)
        self.text = tk.StringVar(value = '')
        success = tk.Label(self, text = '', font=("Helvetica", 10, "italic"), bg='#4834DF', textvariable = self.text).pack(pady=4, padx=16)

    def addPayment(self):
        global conn
        cur = conn.cursor()
        q1 = '''select * from customers where name = ?'''
        cur.execute(q1, (self.custName.get(),))
        r1 = cur.fetchall()
        if not self.payID.get().isdigit():
            return messagebox.showwarning('Add Payment', 'Please enter valid payment ID!')
        elif len(r1) == 0:
            return messagebox.showwarning('Add Payment', 'Customer Not Found!')
        else:
            q2 = '''select * from subscriptions where custName = ?'''
            cur.execute(q2, (self.custName.get(),))
            r2 = cur.fetchall()
            if len(r2) == 0:
                return messagebox.showwarning('Add Payment', 'Customer Found But Not Yet Subscribed To Any Packages!')
            else:
                q3 = '''select * from packages where packageID = ?'''
                cur.execute(q3, (r2[0][2],))
                r3 = cur.fetchall()
                bill = r2[0][3] * r3[0][3]
                self.text.set("New Payment Added!!")
                conn.commit()
                cur.close()
                return self.invoice.set('Payment ID : {}\nCustomer Name : {}\nBill Amount : ₹ {}'.format(int(self.payID.get()), self.custName.get(), bill))


app = GymApp()
app.mainloop()
conn.close()
