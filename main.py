# coding: utf-8
import os
import random
import gi
gi.require_version('Gtk', '3.0')
from pricing_method import *
from gi.repository import Gtk
from Crypto.Cipher import DES
import struct


class PricingUI(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self,title='Product Pricing Tool(BETA)')
        self.set_default_size(720,320)
        self.set_border_width(8)
        self.set_opacity(50.0)

        #BASIC LAYOUT INIT
        #Create top Level Base Mesh
        base = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
        self.add(base)
        #Init Two Segments for UI Layout
        listbox = Gtk.ListBox()
        listbox.set_border_width(15)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.set_valign(Gtk.Align.START)
        #vbox.set_halign(Gtk.Align.START)
        base.pack_start(vbox, True, True, 0)
        base.pack_start(listbox, True, True, 0)
        #base.add(vbox)
        #base.attach_next_to(listbox, vbox, Gtk.PositionType.RIGHT, 1, 1)
        #LEFT SEGMENT OF UI
        #Adding the Buttons
        file_button = Gtk.Button.new_with_label('File')
        lib_button = Gtk.Button.new_with_label('Library')
        contact_button = Gtk.Button.new_with_label('Contact')
        about_button = Gtk.Button.new_with_label('About')

        #Packing The Buttons
        vbox.pack_start(file_button, True, True, 0)
        vbox.pack_start(lib_button, True, True, 0)
        vbox.pack_start(contact_button, True, True, 0)
        vbox.pack_end(about_button, True, True, 0)  

        #RIGHT SEGMENT OF UI
        #Preparing Tricky Layout
        row0 = Gtk.ListBoxRow()
        row0.set_halign(Gtk.Align.START)
        listbox.add(row0)
        #Adding HorizontalBox to place widgets
        hbox = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
        row0.add(hbox)
        #At Last,Adding The Widgets,whooooo!!!
        prod_name = Gtk.Label()
        stock_count = Gtk.Label()
        prod_name.set_text('Product Name')
        stock_count.set_text('Stock   ')
        self.prod_name_input = Gtk.Entry()
        self.stock_count_input = Gtk.Entry()

        #Packaging 101
        hbox.pack_start(prod_name, True, True, 0)
        hbox.pack_start(self.prod_name_input, True, True, 0)
        hbox.pack_start(stock_count, True, True, 0)
        hbox.pack_start(self.stock_count_input, True, True, 0)

        #Second Row
        row1 = Gtk.ListBoxRow()
        row1.set_halign(Gtk.Align.START)
        listbox.add(row1)
        #Adding HorizontalBox to place widgets
        hbox1 = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
        row1.add(hbox1)
        #At Last,Adding The Widgets,whooooo!!!
        prod_cost = Gtk.Label()
        method = Gtk.Label()
        prod_cost.set_text('Product Cost*')
        method.set_text('Method*')
        self.prod_cost_input = Gtk.Entry()
        self.prod_cost_input.set_width_chars(1)
        #method_input = Gtk.Entry()
        methods = Gtk.ListStore(int, str)
        methods.append([1, "Cost-Plus"])
        methods.append([2, "Cost-Plus 2"])
        methods.append([3, "Competitor Aware CostPlus"])

        self.method_input = Gtk.ComboBox.new_with_model_and_entry(methods)
        #self.method_input.connect("changed", self.get_method)
        self.method_input.set_entry_text_column(1)

        #Packaging 101
        hbox1.pack_start(prod_cost, True, True, 0)
        hbox1.pack_start(self.prod_cost_input, True, True, 0)
        hbox1.pack_start(method, True, True, 0)
        hbox1.pack_start(self.method_input, True, True, 0)

        #Third Row
        row2 = Gtk.ListBoxRow()
        row2.set_halign(Gtk.Align.START)
        listbox.add(row2)
        #Adding HorizontalBox to place widgets
        hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        row2.add(hbox2)
        #At Last,Adding The Widgets,whooooo!!!
        spacer = Gtk.Label('    ')
        space = Gtk.Label('    ')
        time_label = Gtk.Label()
        time_label.set_text('timedated')
        self.time = Gtk.CheckButton()
        self.time.set_active(False)
        #Packaging 101
        hbox2.pack_start(spacer, True, True, 0)
        hbox2.pack_start(space, True, True, 0)
        hbox2.pack_start(time_label, True, True, 0)
        hbox2.pack_start(self.time, True, True, 0)

        row3 = Gtk.ListBoxRow()
        row3.set_halign(Gtk.Align.CENTER)
        listbox.add(row3)
        hbox3 = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        row3.add(hbox3)
        #Adding HorizontalBox to place widgets
        gen = Gtk.Button.new_with_label('GENERATE')
        gen.connect('clicked', self.generate)
        sp = Gtk.Label('   ')
        sp1 = Gtk.Label('   ')
        hbox3.pack_start(sp, True, True, 0)
        hbox3.pack_start(gen, True, True, 0)
        hbox3.pack_start(sp1, True, True, 0)

        row4 = Gtk.ListBoxRow()
        row4.set_halign(Gtk.Align.CENTER)
        listbox.add(row4)
        self.tview = Gtk.TextView()
        row4.add(self.tview)

    def generate(self,widget):
        #Var Declarations
        self.textbuffer = self.tview.get_buffer()
        try:
            cost = float((self.prod_cost_input.get_text()))
            product = self.prod_name_input.get_text()
            stock = int(self.stock_count_input.get_text())
        except ValueError:
                self.textbuffer.set_text("\r\rPLEASE PROVIDE VALID VALUES BEFORE TRYING TO GENERATE")
        price = 0
        #Get Method Of Pricing
        time_status = self.time.get_active()
        tree_iter = self.method_input.get_active_iter()
        entry = self.method_input.get_child()
        if tree_iter != None:
            model = self.method_input.get_model()
            row_id, name = model[tree_iter][:2]
            if row_id is 1:
                #Start Calculations
                try:
                    if time_status is True:
                        time_combo = Gtk.Entry()
                        time_combo.set_text('Enter time left(days)')
                        h2box.pack_start(time_combo, True, True, 0)
                        time_d = time_combo.get_text()
                        dynamic_pricer(int(time_d), cost)
                    else:    
                        price = cost_plus(cost)

                except UnboundLocalError:
                    self.textbuffer.set_text("\r\rMISSING REQUIRED ENTRY : PRODUCT COST")

            elif row_id is 2:
                try:
                    if time_status is True:
                        dynamic_pricer(10,cost)
                    else:    
                        price = max_cost_plus(cost)
                except UnboundLocalError:
                    self.textbuffer.set_text("\r\rMISSING REQUIRED ENTRY : PRODUCT COST")
            elif row_id is 3:
                try:
                    price = pricebot(product)
                except UnboundLocalError:
                    self.textbuffer.set_text("\r\rMISSING REQUIRED ENTRY : PRODUCT COST")
        else:
            self.textbuffer.set_text("\r\rPLEASE CHOOSE METHOD FROM GIVEN METHOD LIST")
            #Final Results
        try:
            self.textbuffer.set_text("\r\rProduct Name: %s\nAvailable Stock: %d\n\n"                                     "Recommended Price: %3f\n" %(product,stock,price))
        except UnboundLocalError:
            pass
 
def pricingmaker():
    root = PricingUI()
    #root.set_default_size(640, 320)
    root.connect('delete-event', Gtk.main_quit)
    root.show_all()
    Gtk.main()
    
    
class loginUI(Gtk.Window):
    def __init__(self):
        if os.path.exists('usrdata.dat'):
            Gtk.Window.__init__(self,title='  LOG IN  ')
        else:
            Gtk.Window.__init__(self,title='  REGISTER  ')
        self.set_default_size(320,240)
        self.set_border_width(5)

        box = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
        box.set_halign(Gtk.Align.CENTER)
        box.set_valign(Gtk.Align.CENTER)
        box.set_border_width(15)
        self.add(box)
        self.info = Gtk.Label('Login With username and password')
        usr = Gtk.Label('Username')
        psswd = Gtk.Label('Password')
        self.usr_entry = Gtk.Entry()
        self.pass_entry = Gtk.Entry()
        self.pass_entry.set_visibility(False)
        self.submit = Gtk.Button('  SUBMIT  ')
        self.submit.connect('clicked', self.on_submit)
        #Add Widgets To Window
        box.pack_start(self.info, True, True, 0)
        box.pack_start(usr, True, True, 0)
        box.pack_start(self.usr_entry, True, True, 0)
        box.pack_start(psswd, True, True, 0)
        box.pack_start(self.pass_entry, True, True, 0)
        box.pack_start(self.submit, True, True, 0)
        self.tview = Gtk.TextView()
        box.pack_end(self.tview,True, True, 0)
        self.textbuffer = self.tview.get_buffer()
        
    def on_submit(self, submit):
            
        usr = self.usr_entry.get_text()
        pss = self.pass_entry.get_text()
        usrdata = ''
        #Password Validation
        alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        num = '1234567890'
        alpha_count = 0
        num_count = 0
        pss_test = pss + '.'
        pss_end = pss_test.find('.')
        for a in range(0,51):
            for p in range(0,pss_end):
                if alpha[a] == pss[p]:
                    alpha_count += 1
        for n in range(0,10):
            for p in range(0,pss_end):
                if num[n] == pss[p]:
                    num_count += 1
        if os.path.exists('usrdata.dat'):
            with open('usrdata.dat', 'r') as f:
                usrdata = f.readlines()
                f.close()
            credentials = usr+'\t'+pss+'\n'
            for x in usrdata:
                if x == credentials:
                    usrdata = str(x)
                    self.textbuffer.set_text("\r\rLogin Successful\n")
        
                    root.destroy()
                    pricingmaker()
                elif usr == '' or pss == '':
                    self.textbuffer.set_text('\nUserName and/or Password Cannot Be Empty\n')
                else:
                    self.textbuffer.set_text('\rInvalid Username/Password\n')
        else:
                if usr == '' or pss == '':
                    self.textbuffer.set_text('\nUserName and/or Password Cannot Be Empty\n')
                elif alpha_count == 0 or num_count == 0:
                    self.textbuffer.set_text('Password should contain *Letters*\n and *Numbers*\n')
                else:
                    with open('usrdata.dat','a') as f:
                        f.write(usr+'\t'+pss+'\n')
                        self.textbuffer.set_text("\r\rREGISTRATION SUCCESSFUL\n")
                        f.close()
                    
                        '''data = usr+'\t'+pss+'\n'
                        encrypted = self.encrypt(data)
                        f.write(str(encrypted))
                        self.textbuffer.set_text("\r\rREGISTRATION SUCCESSFUL\n")
                        f.close()'''
                    root.destroy()
                
    def encrypt(self,credentials):
        text = credentials
        key = b'superkey'
        def pad(text):
             while len(text) % 8 != 0:
                 text += ' '
             return text
        des = DES.new(key, DES.MODE_ECB)
        padded_text = pad(text)
        padded_text = bytes(padded_text.encode('utf-8'))
        return des.encrypt(padded_text)
        
    def decrypt(self,encrypted_text, key=b'superkey'):
        des = DES.new(key, DES.MODE_ECB)
        des.decrypt(encrypted_text)
            
root = loginUI()
root.connect('delete-event',Gtk.main_quit)
root.show_all()
Gtk.main()

