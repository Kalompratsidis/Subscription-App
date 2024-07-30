from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pickle

class GymSubscriptionApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Πρόγραμμα συνδρομών")
        self.root.iconbitmap('aboutbody.ico')
        self.customer_list = []

        self.my_tree = ttk.Treeview(root, selectmode='extended')
        self.month_list = ["Όνομα", "Ημ Πληρωμής", "Λήξη", "Ιανουάριος", "Φεβρουάριος", "Μάρτιος", "Απρίλιος", 
                           "Μάϊος", "Ιούνιος", "Ιούλιος", "Αύγουστος", "Σεπτέμβριος", "Οκτώβριος", "Νοέμβριος", "Δεκέμβριος"]

        self.create_widgets()

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=10)
        self.root.grid_rowconfigure(3, weight=1)
        
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        self.root.grid_columnconfigure(4, weight=1)
        
        self.load_customers()
        self.reset_monthly_payments_if_new_year()  # Κλήση της συνάρτησης κατά την εκκίνηση

    def add_customer(self):
        edit_window = Toplevel(self.root)
        edit_window.title("Πρόγραμμα συνδρομών")
        edit_window.iconbitmap('aboutbody.ico')

        edit_window.grid_rowconfigure(0, weight=0)
        edit_window.grid_rowconfigure(1, weight=0)
        edit_window.grid_rowconfigure(2, weight=1)
        edit_window.grid_rowconfigure(3, weight=1)
        
        
        
        
        edit_window.grid_columnconfigure(0, weight=0)
        edit_window.grid_columnconfigure(1, weight=1)
        edit_window.grid_columnconfigure(2, weight=1)
        edit_window.grid_columnconfigure(3, weight=1)

        Label(edit_window, text="Πληρωμένοι Μήνες").grid(row=0, column=0, columnspan=2, pady=2,sticky="nsew")
        Label(edit_window, text="Πελάτης").grid(row=1, column=0, columnspan=1, pady=2,sticky="nsew")
        
        self.customer_entry = Entry(edit_window)
        self.customer_entry.grid(column=1, row=1, columnspan=1,sticky="ew", padx=10)

        month_list = Listbox(edit_window, selectmode=MULTIPLE)
        month_list.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        my_list = ["Ιανουάριος", "Φεβρουάριος", "Μάρτιος", "Απρίλιος", "Μάϊος", "Ιούνιος", "Ιούλιος", "Αύγουστος", 
                   "Σεπτέμβριος", "Οκτώβριος", "Νοέμβριος", "Δεκέμβριος"]
        
        registration_month = datetime.now().month
        
        for i, item in enumerate(my_list):
            if i+1 >= registration_month:
                month_list.insert(END, item)

        def select():
            selected_indices = month_list.curselection()
            print(selected_indices)
            

            paid_months = 0
            selected_months = []
            customer_name = self.customer_entry.get().strip()
            
            if len(selected_indices)>1:
                if selected_indices[0]!=0:
                    messagebox.showwarning("ΣΦΑΛΜΑ", "Επιλέξτε τον τρέχων μήμα.")
                    return

                elif selected_indices[0]==0:

                    for i in range(len(selected_indices) - 1):
                        if selected_indices[i + 1] != selected_indices[i] + 1:
                            messagebox.showwarning("ΣΦΑΛΜΑ", "Επιλέξτε συνεχόμενους μήνες.")
                            
                            return
                        else:
                            print("Hi")
                            for i in selected_indices :
                                selected_months.append(my_list[registration_month + i - 1])
                                paid_months = len(selected_months) 
            
            elif len(selected_indices)==0:
                print("Zero")             
                selected_months.append(selected_indices)
                paid_months = 0
            
            elif len(selected_indices)==1:
                if selected_indices[0]==0:
                    paid_months = 1
                    selected_months.append(my_list[registration_month - 1])
                    print(f"paid={paid_months}")
                else:
                    messagebox.showwarning("ΣΦΑΛΜΑ", "Επιλέξτε τον τρέχων μήμα.")
                    return
                        
                

            
            if customer_name:
                registration_date = datetime.now().strftime("%d/%m/%Y")
                end_date = (datetime.now() + relativedelta(months=paid_months)).strftime("%d/%m/%Y")

                payment_status = ["Ναι" if month in selected_months else "Όχι" for month in my_list]

                new_entry = [customer_name, registration_date, end_date] + payment_status
                self.customer_list.append(new_entry)
                self.my_tree.insert('', 'end', values=new_entry)
                self.customer_entry.delete(0, END)
                self.check_expiry()

                self.save_customers()

                edit_window.destroy()

        add_button = Button(edit_window, text="Επέλεξε",highlightthickness=10,borderwidth=10, command=select)
        add_button.grid(row=1, column=2,columnspan=1, sticky="w", padx=10,pady=10)

    def check_expiry(self):
        date_format = "%d/%m/%Y"
        for item in self.my_tree.get_children():
            expiry_date = self.my_tree.item(item, 'values')[2]
            expiry_date = datetime.strptime(expiry_date, date_format)
            if expiry_date < datetime.now():
                self.my_tree.item(item, tags=('expired',))
            else:
                self.my_tree.item(item, tags=())

        self.my_tree.tag_configure('expired', background='red')

    def delete_customer(self):
        selected_items = self.my_tree.selection()
        for selected_item in selected_items:
            item_values = self.my_tree.item(selected_item, 'values')
            self.customer_list = [customer for customer in self.customer_list if customer[0] != item_values[0]]
            self.my_tree.delete(selected_item)
        self.save_customers()

    def customer_data_processing(self):
        # Επιλογή του επιλεγμένου στοιχείου στο Treeview
        selected_item = self.my_tree.selection()
        if selected_item:
            selected_item = selected_item[0]  # Επιλέγει το πρώτο επιλεγμένο στοιχείο
            item_values = self.my_tree.item(selected_item, 'values')  # Παίρνει τις τιμές του επιλεγμένου στοιχείου

            # Δημιουργία παραθύρου επεξεργασίας
            edit_window = Toplevel(self.root)
            edit_window.title("Επεξεργασία Πελάτη")  # Τίτλος του παραθύρου
            edit_window.iconbitmap('images/aboutbody.ico')  # Εικονίδιο παραθύρου

            # Δημιουργία και τοποθέτηση ετικέτας και πεδίου κειμένου για το όνομα
            Label(edit_window, text="Όνομα").grid(row=0, column=0, padx=10, pady=5)  # Ετικέτα "Όνομα"
            name_entry = Entry(edit_window)  # Πεδίο κειμένου για το όνομα
            name_entry.grid(row=0, column=1, padx=10, pady=5)  # Τοποθέτηση του πεδίου κειμένου
            name_entry.insert(0, item_values[0])  # Εισάγει το τρέχον όνομα στο πεδίο κειμένου

            # Δημιουργία και τοποθέτηση ετικέτας και λίστας για τους πληρωμένους μήνες
            Label(edit_window, text="Πληρωμένοι Μήνες").grid(row=1, column=0, columnspan=2, padx=10, pady=5)  # Ετικέτα "Πληρωμένοι Μήνες"
            month_list = Listbox(edit_window, selectmode=MULTIPLE)  # Δημιουργία λίστας πολλαπλής επιλογής για μήνες
            month_list.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)  # Τοποθέτηση της λίστας
            my_list = ["Ιανουάριος", "Φεβρουάριος", "Μάρτιος", "Απρίλιος", "Μάϊος", "Ιούνιος", "Ιούλιος", "Αύγουστος", 
                    "Σεπτέμβριος", "Οκτώβριος", "Νοέμβριος", "Δεκέμβριος"]  # Λίστα μηνών






            
            # Γέμισμα της λίστας με τους μήνες και επιλογή των πληρωμένων μηνών
            for i, item in enumerate(my_list):
                month_list.insert(END, item)  # Εισαγωγή του μήνα στη λίστα
                if item_values[i+3] == "Ναι":  # Εάν ο μήνας είναι πληρωμένος, επιλέγεται στη λίστα
                    month_list.select_set(i)






            def save():
                # Συνάρτηση για την αποθήκευση των αλλαγών
                new_name = name_entry.get().strip()  # Παίρνει το νέο όνομα από το πεδίο κειμένου
                selected_indices = month_list.curselection()  # Παίρνει τις επιλεγμένες θέσεις στη λίστα
                selected_months = []
                paid_months = 0
                
                # Παίρνει την τρέχουσα ημερομηνία
                today_month =  datetime.now().month

                for i in selected_indices:
                    month_name = my_list[i]
                    month_index = my_list.index(month_name) + 1  # Παίρνει τον μήνα ως αριθμό (1-12)
                    selected_months.append(month_name)  # Δημιουργεί λίστα με τους επιλεγμένους μήνες

                    # Υπολογίζει την ημερομηνία του μήνα (χρησιμοποιούμε την πρώτη μέρα του μήνα για την σύγκριση)
                    if month_index >= today_month:
                        paid_months = len(selected_months)  # Υπολογίζει τον αριθμό των πληρωμένων μηνών

                if new_name:  # Εάν το νέο όνομα δεν είναι κενό
                    # Υπολογισμός της νέας ημερομηνίας λήξης
                    new_registration_date = item_values[1]  # Διατηρεί την αρχική ημερομηνία εγγραφής
                    new_end_date = (datetime.strptime(new_registration_date, "%d/%m/%Y") + relativedelta(months=paid_months)).strftime("%d/%m/%Y")

                    # Δημιουργία νέας κατάστασης πληρωμής
                    new_payment_status = ["Ναι" if month in selected_months else "Όχι" for month in my_list]
                    new_entry = [new_name, new_registration_date, new_end_date] + new_payment_status  # Δημιουργία της νέας εγγραφής

                    # Ενημέρωση της λίστας πελατών με τη νέα εγγραφή
                    self.customer_list = [new_entry if customer[0] == item_values[0] else customer for customer in self.customer_list]
                    self.my_tree.item(selected_item, values=new_entry)  # Ενημέρωση του Treeview με τις νέες τιμές
                    self.check_expiry()  # Ενημέρωση του χρώματος για την λήξη

                    self.save_customers()  # Αποθήκευση των αλλαγών

                    edit_window.destroy()  # Κλείσιμο του παραθύρου επεξεργασίας


            # Δημιουργία και τοποθέτηση κουμπιού αποθήκευσης
            save_button = Button(edit_window, text="Αποθήκευση", command=save)  # Κουμπί αποθήκευσης
            save_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)  # Τοποθέτηση του κουμπιού

    def save_customers(self):
        with open('customers.pkl', 'wb') as f:
            pickle.dump(self.customer_list, f)

    def load_customers(self):
        try:
            with open('customers.pkl', 'rb') as f:
                self.customer_list = pickle.load(f)
                for customer in self.customer_list:
                    self.my_tree.insert('', 'end', values=customer)
                self.check_expiry()
        except (FileNotFoundError, EOFError):
            self.customer_list = []

    def sort_customers(self, selection):

        # Καθαρισμός του Treeview
        for item in self.my_tree.get_children():
            self.my_tree.delete(item)
        
        # Ταξινόμηση πελατών ανάλογα με την επιλογή
        if selection == "Αλφαβητικά":
            sorted_list = sorted(self.customer_list, key=lambda x: x[0])
        elif selection == "Ημερομηνία Πληρωμής":
            sorted_list = sorted(self.customer_list, key=lambda x: datetime.strptime(x[1], "%d/%m/%Y"))
        elif selection == "Ημερομηνία Λήξης":
            sorted_list = sorted(self.customer_list, key=lambda  x: datetime.strptime(x[2], "%d/%m/%Y"))
        
        # Εισαγωγή των ταξινομημένων πελατών στο Treeview
        for customer in sorted_list:
            self.my_tree.insert('', 'end', values=customer)
            self.check_expiry()#Ελέγχει για ληγμένους πελάτες

    def search_customer(self, *args):
            query = self.search_var.get().strip().lower()
            for item in self.my_tree.get_children():
                self.my_tree.delete(item)

            filtered_customers = [customer for customer in self.customer_list if query in customer[0].lower()]
            for customer in filtered_customers:
                self.my_tree.insert('', 'end', values=customer)
                self.check_expiry()#Ελέγχει για ληγμένους πελάτες

    def refresh_treeview(self):
        for item in self.my_tree.get_children():
            self.my_tree.delete(item)
        for customer in self.customer_list:
            self.my_tree.insert('', 'end', values=customer)
        self.check_expiry()

    def reset_monthly_payments_if_new_year(self):
        current_year = datetime.now().year

        for customer in self.customer_list:
            registration_date = datetime.strptime(customer[1], "%d/%m/%Y")
            payment_year = registration_date.year
            if current_year > payment_year:
                # Set all monthly payments to "Όχι"
                for i in range(3, len(customer)):
                    customer[i] = "Όχι"
                
        
        self.save_customers()
        self.refresh_treeview()

    def create_widgets(self):
        customer_label = Label(root, text="Πελάτης")
        customer_label.grid(column=0, row=0, sticky="ew", padx=10)

        self.my_tree['columns'] = self.month_list
        self.my_tree.column("#0", width=0, stretch=NO)

        for month in self.month_list:
            self.my_tree.column(month, anchor=W, width=80, stretch=YES)
            self.my_tree.heading(month, text=month, anchor=W)

        self.my_tree.grid(row=2, column=0, columnspan=12, sticky='nsew')

        add_button = Button(self.root, text="Προσθήκη", command=self.add_customer)
        add_button.grid(row=0, column=2, sticky="ew", padx=10)

        delete_button = Button(self.root, text="Διαγραφή", command=self.delete_customer)
        delete_button.grid(row=0, column=3, sticky="ew", padx=10)

        processing_button = Button(self.root, text="Επεξεργασία", command=self.customer_data_processing)
        processing_button.grid(row=0, column=4, sticky="ew", padx=10)

        clicked = StringVar()
        options = ["Αλφαβητικά", "Ημερομηνία Πληρωμής", "Ημερομηνία Λήξης"]
        clicked.set(options[0])
        drop = OptionMenu(root, clicked, *options, command=self.sort_customers)
        drop.grid(row=1, column=0)

        self.search_var = StringVar()
        self.search_var.trace_add('write', self.search_customer)
        search_entry = Entry(root, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, padx=10, pady=10)

if __name__ == "__main__":
    root = Tk()
    app = GymSubscriptionApp(root)
    root.mainloop()