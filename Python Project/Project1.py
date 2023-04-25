from tkinter import*
from PIL import Image,ImageTk
import time
from tkinter import messagebox

import sqlite3
con=sqlite3.connect(database='banking.sqlite')
cur=con.cursor()

table1='''create table account
(acn integer primary key autoincrement,name text,pass text,mob text,email text,bal float,acnopendate text,acntype text)'''

table2='''create table txn(acn integer,txndate text,txntype text,updatedbal float)'''

try:
    cur.execute(table1)
    cur.execute(table2)
    con.commit()
    print('tables created')
except Exception as e:
    print(e)

win=Tk()
win.state('zoomed')
win.configure(bg='powder blue')

title=Label(win,fg='blue', text='Banking Automation', bg='powder blue',font=('Arial',25,'bold','underline'))
title.pack()

img = Image.open('logo.jpeg')
img1 = Image.open('logo.jpeg')

img= img.resize((200,80))
img1= img.resize((200,80))

imgtk= ImageTk.PhotoImage(img,master=win)
imgtk1= ImageTk.PhotoImage(img1,master=win)

logolbl= Label(win,image=imgtk)
logolbl1= Label(win,image=imgtk1)

logolbl.place(relx=0,rely=0)
logolbl1.place(relx=.87,rely=0)

def home_screen():
    frm=Frame(win)
    frm.place(relx=0,rely=.1,relwidth=1,relheight=.9)
    frm.configure(bg='orange')

    def openacc():
        frm.destroy()
        openacc_screen()

    def forget():
        frm.destroy()
        forget_screen()

    def login():
        acnno=acnentry.get()
        pwd=passentry.get()
        if(len(acnno)==0 or len(pwd)==0 ):
            messagebox.showwarning('validation',"Fields can't be Empty")
            return
        else:
            con=sqlite3.connect(database='banking.sqlite')
            cur=con.cursor()
            query='''select * from account where acn=? and pass=?'''
            cur.execute(query,(acnno,pwd))
            global usertup
            usertup=cur.fetchone()
            if(usertup==None):
                messagebox.showerror('Failed','Invalid Account Number or Password')
                return

            else:
                frm.destroy()
                welcome_frame()

    def reset():
        acnentry.delete(0,'end')
        passentry.delete(0,'end')
        acnentry.focus()

    acnlbl=Label(frm,text='Account Number :',bg='orange',font=('Arial',15,'bold'))
    acnlbl.place(relx=.35,rely=.2)

    acnentry= Entry(frm,font=('Arial',15,'bold'),bd=3)
    acnentry.place(relx=.5,rely=.2)
    acnentry.focus()

    passlbl=Label(frm,text='Password :',bg='orange',font=('Arial',15,'bold'))
    passlbl.place(relx=.35,rely=.3)

    passentry= Entry(frm,font=('Arial',15,'bold'),bd=3,show='*')
    passentry.place(relx=.5,rely=.3)

    loginbtn=Button(frm,text='Login',font=('Arial',15,'bold'),bd=3,width=7,command=login)
    loginbtn.place(relx=.5,rely=.36)

    resetbtn=Button(frm,text='Reset',font=('Arial',15,'bold'),bd=3,width=7,command=reset)
    resetbtn.place(relx=.57,rely=.36)

    fpbtn=Button(frm,text='Forget Password',font=('Arial',15,'bold'),bd=3,width=16,command=forget)
    fpbtn.place(relx=.5,rely=.44)

    openbtn=Button(frm,text='Open New Account',font=('Arial',15,'bold'),bd=3,width=16,command=openacc)
    openbtn.place(relx=.5,rely=.52)

def openacc_screen():
    frm=Frame(win)
    frm.place(relx=0,rely=.1,relwidth=1,relheight=.9)
    frm.configure(bg='orange')

    def back():
        frm.destroy()
        home_screen()

    def reset():
        nameentry.delete(0,'end')
        passentry.delete(0,'end')
        mobentry.delete(0,'end')
        emailentry.delete(0,'end')
        nameentry.focus()

    def accountopen():
        name=nameentry.get()
        pwd=passentry.get()
        mob=mobentry.get()
        email=emailentry.get()
        acntype='Saving'
        opendate=time.ctime()
        bal=0
        if(len(name)==0 or len(pwd)==0 or len(mob)==0 or len(email)==0):
            messagebox.showwarning('validation',"Fields can't be Empty")
            return
        else:
            con=sqlite3.connect(database='banking.sqlite')
            cur=con.cursor()
            query='''insert into account(name,pass,mob,email,bal,acnopendate,acntype) values(?,?,?,?,?,?,?)'''
            cur.execute(query,(name,pwd,mob,email,bal,opendate,acntype))
            con.commit()
            
            cur=con.cursor()
            cur.execute('select max(acn) from account')
            tup=cur.fetchone()
            con.close()
            messagebox.showinfo("Success",f"Your Account No is : {tup[0]}")
            frm.destroy()
            home_screen()

    backbtn=Button(frm,text='Back',font=('Arial',15,'bold'),bd=3,width=7,command=back)
    backbtn.place(relx=0,rely=0)

    frmtitle=Label(frm,text='Open New Account',font=('Arial',20,'bold','underline'),bg='orange',)
    frmtitle.pack()

    namelbl=Label(frm,text='Full Name :',bg='orange',font=('Arial',15,'bold'))
    namelbl.place(relx=.35,rely=.2)

    nameentry= Entry(frm,font=('Arial',15,'bold'),bd=3)
    nameentry.place(relx=.5,rely=.2)
    nameentry.focus()

    passlbl=Label(frm,text='Password :',bg='orange',font=('Arial',15,'bold'))
    passlbl.place(relx=.35,rely=.3)

    passentry= Entry(frm,font=('Arial',15,'bold'),bd=3,show='*')
    passentry.place(relx=.5,rely=.3)

    moblbl=Label(frm,text='Mobile No. :',bg='orange',font=('Arial',15,'bold'))
    moblbl.place(relx=.35,rely=.4)

    mobentry= Entry(frm,font=('Arial',15,'bold'),bd=3)
    mobentry.place(relx=.5,rely=.4)

    emaillbl=Label(frm,text='Email ID :',bg='orange',font=('Arial',15,'bold'))
    emaillbl.place(relx=.35,rely=.5)

    emailentry= Entry(frm,font=('Arial',15,'bold'),bd=3)
    emailentry.place(relx=.5,rely=.5)
    
    openbtn=Button(frm,text='Open',font=('Arial',15,'bold'),bd=3,width=7,command=accountopen)
    openbtn.place(relx=.5,rely=.56)

    resetbtn=Button(frm,text='Reset',font=('Arial',15,'bold'),bd=3,width=7,command=reset)
    resetbtn.place(relx=.57,rely=.56)


def forget_screen():
    frm=Frame(win)
    frm.place(relx=0,rely=.1,relwidth=1,relheight=.9)
    frm.configure(bg='orange')

    def back():
        frm.destroy()
        home_screen()

    def reset():
        acnentry.delete(0,'end')
        mobentry.delete(0,'end')
        emailentry.delete(0,'end')
        acnentry.focus()

    def getpass():
        a=acnentry.get()
        m=mobentry.get()
        e=emailentry.get()

        con=sqlite3.connect(database='banking.sqlite')
        cur=con.cursor()
        query='select pass from account where acn=? and mob=? and email=?'
        cur.execute(query,(a,m,e))
        tup=cur.fetchone()
        if(tup==None):
            messagebox.showerror('Incorrect','Details not Found')
        else:
            messagebox.showinfo('Success',f'Your Password is : {tup[0]}')
            frm.destroy()
            home_screen()

    backbtn=Button(frm,text='Back',font=('Arial',15,'bold'),bd=3,width=7,command=back)
    backbtn.place(relx=0,rely=0)

    frmtitle=Label(frm,text='Forget Password',font=('Arial',20,'bold','underline'),bg='orange',)
    frmtitle.pack()

    acnlbl=Label(frm,text='Account No. :',bg='orange',font=('Arial',15,'bold'))
    acnlbl.place(relx=.35,rely=.3)

    acnentry= Entry(frm,font=('Arial',15,'bold'),bd=3)
    acnentry.place(relx=.5,rely=.3)
    acnentry.focus()

    moblbl=Label(frm,text='Mobile No. :',bg='orange',font=('Arial',15,'bold'))
    moblbl.place(relx=.35,rely=.4)

    mobentry= Entry(frm,font=('Arial',15,'bold'),bd=3)
    mobentry.place(relx=.5,rely=.4)

    emaillbl=Label(frm,text='Email Address :',bg='orange',font=('Arial',15,'bold'))
    emaillbl.place(relx=.35,rely=.5)

    emailentry= Entry(frm,font=('Arial',15,'bold'),bd=3)
    emailentry.place(relx=.5,rely=.5)
    
    submitbtn=Button(frm,text='Submit',font=('Arial',15,'bold'),bd=3,width=7,command=getpass)
    submitbtn.place(relx=.5,rely=.56)

    resetbtn=Button(frm,text='Reset',font=('Arial',15,'bold'),bd=3,width=7,command=reset)
    resetbtn.place(relx=.57,rely=.56)


def welcome_frame():
    frm=Frame(win)
    frm.place(relx=0,rely=.1,relwidth=1,relheight=.9)
    frm.configure(bg='orange')

    def logout():
        frm.destroy()
        home_screen()

    def details():
        nestedfrm=Frame(frm,highlightthickness=2,highlightbackground='black',)
        nestedfrm.configure(bg='powder blue')
        nestedfrm.place(relx=.3,rely=.15,relwidth=.5,relheight=.5)

        frmtitle=Label(nestedfrm,text='Account Details',font=('Arial',15,'bold','underline'),bg='powder blue',)
        frmtitle.pack()

        con=sqlite3.connect(database='banking.sqlite')
        cur=con.cursor()
        query='select * from account where acn=?'
        cur.execute(query,(usertup[0],))
        tup=cur.fetchone()
        con.close()
        acclbl=Label(nestedfrm,text= f'Account Number : {tup[0]}',bg='powder blue',font=('Arial',15,))
        acclbl.place(relx=.2,rely=.2)

        ballbl=Label(nestedfrm,text= f'Account Balance : {tup[5]}',bg='powder blue',font=('Arial',15,))
        ballbl.place(relx=.2,rely=.3)

        datelbl=Label(nestedfrm,text= f'Account Open Date : {tup[6]}',bg='powder blue',font=('Arial',15,))
        datelbl.place(relx=.2,rely=.4)

    def update():
        nestedfrm=Frame(frm,highlightthickness=2,highlightbackground='black',)
        nestedfrm.configure(bg='powder blue')
        nestedfrm.place(relx=.3,rely=.15,relwidth=.5,relheight=.5)

        frmtitle=Label(nestedfrm,text='Update Profile',font=('Arial',15,'bold','underline'),bg='powder blue',)
        frmtitle.pack()

    def deposite():
        nestedfrm=Frame(frm,highlightthickness=2,highlightbackground='black',)
        nestedfrm.configure(bg='powder blue')
        nestedfrm.place(relx=.3,rely=.15,relwidth=.5,relheight=.5)

        def amtdep():
            amt=float(depentry.get())
            con=sqlite3.connect(database='banking.sqlite')
            cur=con.cursor()
            query='update account set bal=bal+? where acn=?'
            cur.execute(query,(amt,usertup[0]))
            con.commit()

            cur=con.cursor()
            cur.execute('select bal from account where acn=?',(usertup[0],))
            bal=cur.fetchone()[0]

            cur=con.cursor()
            query='insert into txn values(?,?,?,?)'
            cur.execute(query,(usertup[0],time.ctime(),'cr.',bal))
            con.commit()
            con.close()

            messagebox.showinfo('Success','Amount Deposited')
            return

        frmtitle=Label(nestedfrm,text='Deposite Balance',font=('Arial',15,'bold','underline'),bg='powder blue',)
        frmtitle.pack()

        deplbl=Label(nestedfrm,text='Amount : ',font=('Arial',15,'bold',),bg='powder blue',)
        deplbl.place(relx=.2,rely=.2)

        depentry=Entry(nestedfrm,font=('Arial',15,'bold',),bd=3)
        depentry.place(relx=.4,rely=.2)

        depbtn=Button(nestedfrm,text='Deposit',font=('Arial',15,'bold',),bd=3,command=amtdep)
        depbtn.place(relx=.58,rely=.35)

    def withdraw():
        nestedfrm=Frame(frm,highlightthickness=2,highlightbackground='black',)
        nestedfrm.configure(bg='powder blue')
        nestedfrm.place(relx=.3,rely=.15,relwidth=.5,relheight=.5)

        def amtwith():
            amt=float(withentry.get())
            con=sqlite3.connect(database='banking.sqlite')
            cur=con.cursor()

            cur=con.cursor()
            cur.execute('select bal from account where acn=?',(usertup[0],))
            bal=cur.fetchone()[0]

            if(bal>=amt):
                query='update account set bal=bal-? where acn=?'
                cur.execute(query,(amt,usertup[0]))
                con.commit()

                cur=con.cursor()
                query='insert into txn values(?,?,?,?)'
                cur.execute(query,(usertup[0],time.ctime(),'wd.',bal-amt))
                con.commit()
                con.close()

                messagebox.showinfo('Success','Amount Withdraw')
                return
            else:
                messagebox.showwarning('Error','Insufficient Balance')

        frmtitle=Label(nestedfrm,text='Withdraw Balance',font=('Arial',15,'bold','underline'),bg='powder blue',)
        frmtitle.pack()

        withlbl=Label(nestedfrm,text='Amount : ',font=('Arial',15,'bold',),bg='powder blue',)
        withlbl.place(relx=.2,rely=.2)

        withentry=Entry(nestedfrm,font=('Arial',15,'bold',),bd=3)
        withentry.place(relx=.4,rely=.2)

        withbtn=Button(nestedfrm,text='Withdraw',font=('Arial',15,'bold',),bd=3,command=amtwith)
        withbtn.place(relx=.55,rely=.35)

    def txn():
        nestedfrm=Frame(frm,highlightthickness=2,highlightbackground='black',)
        nestedfrm.configure(bg='powder blue')
        nestedfrm.place(relx=.3,rely=.15,relwidth=.5,relheight=.5)

        frmtitle=Label(nestedfrm,text='Transaction Details',font=('Arial',15,'bold','underline'),bg='powder blue',)
        frmtitle.pack()

    logoutbtn=Button(frm,text='Logout',font=('Arial',15,'bold'),bd=3,width=7,command=logout)
    logoutbtn.place(relx=.94,rely=.0)

    wellbl=Label(frm,text=f'Welcome,{usertup[1]}',bg='orange',font=('Arial',10,'bold'),fg='green')
    wellbl.place(relx=0,rely=0)

    timelbl=Label(frm,text='login time : '+time.ctime(),bg='orange',font=('Arial',10,'bold'),)
    timelbl.pack()

    detailsbtn=Button(frm,text='Details',font=('Arial',15,'bold'),bd=3,width=12,command=details)
    detailsbtn.place(relx=0,rely=.15)

    updatebtn=Button(frm,text='Update Profile',font=('Arial',15,'bold'),bd=3,width=12,command=update)
    updatebtn.place(relx=0,rely=.25)

    depbtn=Button(frm,text='Deposit',font=('Arial',15,'bold'),bd=3,width=12,command=deposite)
    depbtn.place(relx=0,rely=.35)

    withbtn=Button(frm,text='Withdraw',font=('Arial',15,'bold'),bd=3,width=12,command=withdraw)
    withbtn.place(relx=0,rely=.45)

    txnbtn=Button(frm,text='Tran-History',font=('Arial',15,'bold'),bd=3,width=12,command=txn)
    txnbtn.place(relx=0,rely=.55)


home_screen()
win=mainloop()