import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

# Modern color scheme
COLORS = {
    'primary': '#2962ff',      # Main brand color
    'secondary': '#455a64',    # Secondary color
    'success': '#00c853',      # Success actions
    'danger': '#d50000',       # Dangerous actions
    'warning': '#ffd600',      # Warning actions
    'background': '#f5f5f5',   # Main background
    'surface': '#ffffff',      # Surface color
    'text': '#263238',        # Main text color
    'text_light': '#ffffff'    # Light text color
}

print("Starting application...")

class LibraryManagementApp:
    def __init__(self, root):
        print("Initializing application...")
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1200x700")
        
        # Configure the root window
        self.root.configure(bg=COLORS['background'])
        
        # Configure styles
        self.setup_styles()

        try:
            print("Connecting to database...")
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="shahd2352004",
                database="LibraryManagement"
            )
            print("Database connected successfully!")
            self.cursor = self.db.cursor(dictionary=True)
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")
            messagebox.showerror("Database Error", f"Failed to connect to database: {err}")
            self.root.quit()

        # Create main navigation with modern styling
        self.navbar = tk.Frame(self.root, bg=COLORS['primary'], height=60)
        self.navbar.pack(side=tk.TOP, fill=tk.X)
        self.navbar.pack_propagate(False)  # Force the height

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Members", self.manage_members),
            ("Books", self.manage_books),
            ("Transactions", self.show_transactions),
            ("Events", self.show_events),
            ("Staff", self.show_staff),
            ("Reports", self.show_reports)
        ]

        for btn_text, command in buttons:
            btn = tk.Button(self.navbar, text=btn_text, 
                          font=('Segoe UI', 11),
                          bg=COLORS['primary'],
                          fg=COLORS['text_light'],
                          bd=0,  # No border
                          padx=20,
                          activebackground=COLORS['secondary'],
                          activeforeground=COLORS['text_light'],
                          command=command)
            btn.pack(side=tk.LEFT, pady=10)
            # Add hover effect
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg=COLORS['secondary']))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(bg=COLORS['primary']))

        # Create main content area
        self.main_frame = tk.Frame(self.root, bg=COLORS['background'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.show_dashboard()

    def setup_styles(self):
        # Configure ttk styles
        style = ttk.Style()
        
        # Configure Treeview
        style.configure("Treeview",
                      background=COLORS['surface'],
                      foreground=COLORS['text'],
                      rowheight=25,
                      fieldbackground=COLORS['surface'])
        
        style.configure("Treeview.Heading",
                       background=COLORS['primary'],
                       foreground=COLORS['text_light'],
                       relief="flat")
        
        style.map("Treeview.Heading",
                 background=[('active', COLORS['secondary'])])
        
        # Configure ttk buttons
        style.configure("Primary.TButton",
                       background=COLORS['primary'],
                       foreground=COLORS['text_light'],
                       padding=(20, 10),
                       font=('Segoe UI', 10))
        
        # Configure ttk entry
        style.configure("Custom.TEntry",
                       padding=(5, 5),
                       relief="flat")

    def create_custom_button(self, parent, text, command, color=COLORS['primary']):
        btn = tk.Button(parent, text=text,
                       font=('Segoe UI', 10),
                       bg=color,
                       fg=COLORS['text_light'],
                       bd=0,
                       padx=20, pady=8,
                       activebackground=COLORS['secondary'],
                       activeforeground=COLORS['text_light'],
                       cursor="hand2",
                       command=command)
        btn.bind('<Enter>', lambda e: btn.configure(bg=COLORS['secondary']))
        btn.bind('<Leave>', lambda e: btn.configure(bg=color))
        return btn

    def create_section_header(self, parent, text):
        frame = tk.Frame(parent, bg=COLORS['background'])
        frame.pack(fill=tk.X, pady=(20, 10))
        
        label = tk.Label(frame, text=text,
                        font=('Segoe UI', 24, 'bold'),
                        fg=COLORS['primary'],
                        bg=COLORS['background'])
        label.pack(side=tk.LEFT)
        
        # Add a separator
        separator = ttk.Separator(frame, orient='horizontal')
        separator.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(20, 0), pady=20)
        
        return frame

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_main_frame()
        
        # Create header
        self.create_section_header(self.main_frame, "Dashboard")
        
        # Create cards frame
        cards_frame = tk.Frame(self.main_frame, bg=COLORS['background'])
        cards_frame.pack(fill=tk.X, pady=20)
        
        try:
            # Create stat cards
            # Members count
            self.cursor.execute("SELECT COUNT(*) as count FROM Members")
            total_members = self.cursor.fetchone()['count']
            self.create_stat_card(cards_frame, "Total Members", total_members, "👥")

            # Books count
            self.cursor.execute("SELECT COUNT(*) as count FROM Books")
            total_books = self.cursor.fetchone()['count']
            self.create_stat_card(cards_frame, "Total Books", total_books, "📚")

            # Unpaid fines
            self.cursor.execute("SELECT SUM(fine_total) as total FROM Fines WHERE Paid_Status = 'Unpaid'")
            total_fines = self.cursor.fetchone()['total'] or 0
            self.create_stat_card(cards_frame, "Unpaid Fines", f"${total_fines:.2f}", "💰")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch dashboard data: {err}")

    def create_stat_card(self, parent, title, value, icon):
        # Create a card frame
        card = tk.Frame(parent, bg=COLORS['surface'], padx=20, pady=15)
        card.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        
        # Add icon
        tk.Label(card, text=icon, font=('Segoe UI', 36), bg=COLORS['surface']).pack()
        
        # Add value
        tk.Label(card, text=str(value), 
                font=('Segoe UI', 24, 'bold'), 
                fg=COLORS['primary'],
                bg=COLORS['surface']).pack()
        
        # Add title
        tk.Label(card, text=title,
                font=('Segoe UI', 12),
                fg=COLORS['secondary'],
                bg=COLORS['surface']).pack()

    def manage_members(self):
        self.clear_main_frame()
        
        # Create header
        self.create_section_header(self.main_frame, "Manage Members")

        # Create main container with padding
        container = tk.Frame(self.main_frame, bg=COLORS['background'])
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create form frame with modern styling
        form_frame = tk.Frame(container, bg=COLORS['surface'], padx=20, pady=20)
        form_frame.pack(fill=tk.X, pady=(0, 20))

        # Form fields with better layout
        fields = [
            ("Details:", "details_entry"),
            ("Registration Date (YYYY-MM-DD):", "reg_date_entry"),
            ("History:", "history_entry")
        ]

        entries = {}
        for i, (label_text, entry_name) in enumerate(fields):
            field_frame = tk.Frame(form_frame, bg=COLORS['surface'])
            field_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(field_frame, text=label_text,
                    font=('Segoe UI', 10),
                    bg=COLORS['surface'],
                    fg=COLORS['text']).pack(side=tk.LEFT)
            
            entry = tk.Entry(field_frame, font=('Segoe UI', 10),
                           relief="solid", bd=1)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
            entries[entry_name] = entry

        # Button frame
        button_frame = tk.Frame(form_frame, bg=COLORS['surface'])
        button_frame.pack(fill=tk.X, pady=(20, 0))

        # Create Treeview with modern styling
        tree = ttk.Treeview(container, columns=("ID", "Details", "Date", "History"), show="headings")
        tree.heading("ID", text="Member ID")
        tree.heading("Details", text="Details")
        tree.heading("Date", text="Registration Date")
        tree.heading("History", text="Loan History")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def refresh_tree():
            for item in tree.get_children():
                tree.delete(item)
            try:
                self.cursor.callproc('sp_select_members', ('',))
                for result in self.cursor.stored_results():
                    for row in result.fetchall():
                        tree.insert("", "end", values=(
                            row['MemberID'],
                            row['MemberDetails'],
                            row['RegistrationDate'],
                            row['Loan_History']
                        ))
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Failed to fetch members: {err}")

        def insert_member():
            details = entries['details_entry'].get().strip()
            reg_date = entries['reg_date_entry'].get().strip()
            history = entries['history_entry'].get().strip()

            if not details or not reg_date:
                messagebox.showerror("Input Error", "Details and Registration Date are required!")
                return

            try:
                # Validate date format
                datetime.strptime(reg_date, "%Y-%m-%d")
                
                self.cursor.callproc('sp_insert_member', (details, reg_date, history if history else None))
                self.db.commit()
                
                messagebox.showinfo("Success", "Member added successfully!")
                
                # Clear entries
                for entry in entries.values():
                    entry.delete(0, tk.END)
                
                refresh_tree()
            except ValueError:
                messagebox.showerror("Input Error", "Invalid date format! Use YYYY-MM-DD")
            except mysql.connector.Error as err:
                self.db.rollback()
                messagebox.showerror("Database Error", f"Failed to add member: {err}")

        def delete_member():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Selection Required", "Please select a member to delete!")
                return

            if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this member?"):
                return

            member_id = tree.item(selected[0])['values'][0]
            
            try:
                self.cursor.callproc('sp_delete_member', (member_id,))
                self.db.commit()
                messagebox.showinfo("Success", "Member deleted successfully!")
                refresh_tree()
            except mysql.connector.Error as err:
                self.db.rollback()
                messagebox.showerror("Database Error", f"Failed to delete member: {err}")

        def update_member():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Selection Required", "Please select a member to update!")
                return

            member_id = tree.item(selected[0])['values'][0]
            details = entries['details_entry'].get().strip()
            reg_date = entries['reg_date_entry'].get().strip()
            history = entries['history_entry'].get().strip()

            if not details or not reg_date:
                messagebox.showerror("Input Error", "Details and Registration Date are required!")
                return

            try:
                # Validate date format
                datetime.strptime(reg_date, "%Y-%m-%d")
                
                self.cursor.callproc('sp_update_member', 
                                   (member_id, details, reg_date, history if history else None))
                self.db.commit()
                messagebox.showinfo("Success", "Member updated successfully!")
                
                # Clear entries
                for entry in entries.values():
                    entry.delete(0, tk.END)
                
                refresh_tree()
            except ValueError:
                messagebox.showerror("Input Error", "Invalid date format! Use YYYY-MM-DD")
            except mysql.connector.Error as err:
                self.db.rollback()
                messagebox.showerror("Database Error", f"Failed to update member: {err}")

        # Add buttons with modern styling
        self.create_custom_button(button_frame, "Add Member", insert_member, 
                                color=COLORS['success']).pack(side=tk.LEFT, padx=5)
        self.create_custom_button(button_frame, "Delete Member", delete_member,
                                color=COLORS['danger']).pack(side=tk.LEFT, padx=5)
        self.create_custom_button(button_frame, "Update Member", update_member,
                                color=COLORS['warning']).pack(side=tk.LEFT, padx=5)

        # Initial load
        refresh_tree()

    def manage_books(self):
        self.clear_main_frame()
        
        # Create header
        self.create_section_header(self.main_frame, "Manage Books")

        # Create main container
        container = tk.Frame(self.main_frame, bg=COLORS['background'])
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create form frame with modern styling
        form_frame = tk.Frame(container, bg=COLORS['surface'], padx=20, pady=20)
        form_frame.pack(fill=tk.X, pady=(0, 20))

        # Form fields with better layout
        fields = [
            ("Title:", "title"),
            ("ISBN:", "isbn"),
            ("Status:", "status")
        ]

        entries = {}
        for label_text, entry_name in fields:
            field_frame = tk.Frame(form_frame, bg=COLORS['surface'])
            field_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(field_frame, text=label_text,
                    font=('Segoe UI', 10),
                    bg=COLORS['surface'],
                    fg=COLORS['text']).pack(side=tk.LEFT, padx=(0, 10))
            
            entry = tk.Entry(field_frame, font=('Segoe UI', 10),
                           relief="solid", bd=1)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            entries[entry_name] = entry

        # Button frame
        button_frame = tk.Frame(form_frame, bg=COLORS['surface'])
        button_frame.pack(fill=tk.X, pady=(20, 0))

        # Create Treeview with modern styling
        tree_frame = tk.Frame(container, bg=COLORS['surface'])
        tree_frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(tree_frame, columns=("ID", "Title", "ISBN", "Status"), show="headings")
        tree.heading("ID", text="Book ID")
        tree.heading("Title", text="Title")
        tree.heading("ISBN", text="ISBN")
        tree.heading("Status", text="Availability")

        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        x_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Pack tree and scrollbars
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        def refresh_books():
            for item in tree.get_children():
                tree.delete(item)
            try:
                self.cursor.callproc('sp_select_books', (None,))
                for result in self.cursor.stored_results():
                    for row in result.fetchall():
                        tree.insert("", "end", values=(
                            row['Books_ID'],
                            row['Title'],
                            row['ISBN'],
                            row['AvailabilityStatus']
                        ))
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Failed to fetch books: {err}")

        def insert_book():
            title_val = entries['title'].get().strip()
            isbn_val = entries['isbn'].get().strip()
            status_val = entries['status'].get().strip()

            if not title_val or not isbn_val or not status_val:
                messagebox.showerror("Input Error", "All fields are required!")
                return

            try:
                self.cursor.callproc('sp_insert_book', 
                                   (title_val, isbn_val, None, status_val))
                self.db.commit()
                messagebox.showinfo("Success", "Book added successfully!")
                
                # Clear entries
                for entry in entries.values():
                    entry.delete(0, tk.END)
                
                refresh_books()
            except mysql.connector.Error as err:
                self.db.rollback()
                messagebox.showerror("Database Error", f"Failed to add book: {err}")

        def delete_book():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Selection Required", "Please select a book to delete!")
                return

            if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this book?"):
                return

            book_id = tree.item(selected[0])['values'][0]
            
            try:
                self.cursor.callproc('sp_delete_book', (book_id,))
                self.db.commit()
                messagebox.showinfo("Success", "Book deleted successfully!")
                refresh_books()
            except mysql.connector.Error as err:
                self.db.rollback()
                messagebox.showerror("Database Error", f"Failed to delete book: {err}")

        def update_book():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Selection Required", "Please select a book to update!")
                return

            book_id = tree.item(selected[0])['values'][0]
            title = entries['title'].get().strip()
            isbn = entries['isbn'].get().strip()
            status = entries['status'].get().strip()

            if not title or not isbn or not status:
                messagebox.showerror("Input Error", "All fields are required!")
                return

            try:
                self.cursor.callproc('sp_update_book', 
                                   (book_id, title, isbn, None, status))
                self.db.commit()
                messagebox.showinfo("Success", "Book updated successfully!")
                
                # Clear entries
                for entry in entries.values():
                    entry.delete(0, tk.END)
                
                refresh_books()
            except mysql.connector.Error as err:
                self.db.rollback()
                messagebox.showerror("Database Error", f"Failed to update book: {err}")

        # Add buttons with modern styling
        self.create_custom_button(button_frame, "Add Book", insert_book,
                                color=COLORS['success']).pack(side=tk.LEFT, padx=5)
        self.create_custom_button(button_frame, "Delete Book", delete_book,
                                color=COLORS['danger']).pack(side=tk.LEFT, padx=5)
        self.create_custom_button(button_frame, "Update Book", update_book,
                                color=COLORS['warning']).pack(side=tk.LEFT, padx=5)

        # Initial load
        refresh_books()

    def show_transactions(self):
        self.clear_main_frame()
        
        # Create header
        self.create_section_header(self.main_frame, "Transactions")

        # Create main container
        container = tk.Frame(self.main_frame, bg=COLORS['background'])
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create form frame for fine entry
        form_frame = tk.Frame(container, bg=COLORS['surface'], padx=20, pady=20)
        form_frame.pack(fill=tk.X, pady=(0, 20))

        # Fine entry fields
        fields_frame = tk.Frame(form_frame, bg=COLORS['surface'])
        fields_frame.pack(fill=tk.X, pady=5)

        # Transaction ID field
        tk.Label(fields_frame, text="Transaction ID:", 
                bg=COLORS['surface']).pack(side=tk.LEFT, padx=5)
        transaction_id_var = tk.StringVar()
        transaction_id_entry = tk.Entry(fields_frame, textvariable=transaction_id_var)
        transaction_id_entry.pack(side=tk.LEFT, padx=5)

        # Fine amount field
        tk.Label(fields_frame, text="Fine Amount ($):", 
                bg=COLORS['surface']).pack(side=tk.LEFT, padx=5)
        fine_amount_var = tk.StringVar()
        fine_amount_entry = tk.Entry(fields_frame, textvariable=fine_amount_var)
        fine_amount_entry.pack(side=tk.LEFT, padx=5)

        # Status dropdown
        tk.Label(fields_frame, text="Status:", 
                bg=COLORS['surface']).pack(side=tk.LEFT, padx=5)
        status_var = tk.StringVar(value="Unpaid")
        status_menu = ttk.Combobox(fields_frame, textvariable=status_var, 
                                 values=["Paid", "Unpaid"], state="readonly")
        status_menu.pack(side=tk.LEFT, padx=5)

        # Create Treeview frame
        tree_frame = tk.Frame(container, bg=COLORS['surface'], padx=20, pady=20)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Create Treeview with modern styling
        tree = ttk.Treeview(tree_frame, 
                           columns=("ID", "Date", "Due", "Type", "Member", "Fine", "Status"), 
                           show="headings")
        tree.heading("ID", text="Transaction ID")
        tree.heading("Date", text="Date")
        tree.heading("Due", text="Due Date")
        tree.heading("Type", text="Type")
        tree.heading("Member", text="Member ID")
        tree.heading("Fine", text="Fine Amount")
        tree.heading("Status", text="Fine Status")

        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        x_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Pack tree and scrollbars
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        def refresh_transactions():
            for item in tree.get_children():
                tree.delete(item)
            try:
                self.cursor.execute("""
                    SELECT t.*, COALESCE(f.fine_total, 0) as fine_amount, 
                           COALESCE(f.Paid_Status, 'No Fine') as fine_status
                    FROM Transactions t
                    LEFT JOIN Fines f ON t.Transactions_ID = f.Transactions_ID
                    ORDER BY t.Transactions_Date DESC
                """)
                for row in self.cursor.fetchall():
                    tree.insert("", "end", values=(
                        row['Transactions_ID'],
                        row['Transactions_Date'],
                        row['Due_date'],
                        row['Transaction_type'],
                        row['MemberID'],
                        f"${row['fine_amount']:.2f}",
                        row['fine_status']
                    ))
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Failed to fetch transactions: {err}")

        def add_or_update_fine():
            if not transaction_id_var.get() or not fine_amount_var.get():
                messagebox.showwarning("Input Error", "Please enter both Transaction ID and Fine Amount!")
                return

            try:
                transaction_id = int(transaction_id_var.get())
                fine_amount = float(fine_amount_var.get())

                # Check if transaction exists
                self.cursor.execute("SELECT * FROM Transactions WHERE Transactions_ID = %s", 
                                  (transaction_id,))
                if not self.cursor.fetchone():
                    messagebox.showerror("Error", "Transaction ID does not exist!")
                    return

                # Check if fine already exists for this transaction
                self.cursor.execute("SELECT * FROM Fines WHERE Transactions_ID = %s", 
                                  (transaction_id,))
                existing_fine = self.cursor.fetchone()

                if existing_fine:
                    # Update existing fine
                    self.cursor.execute("""
                        UPDATE Fines 
                        SET fine_total = %s, Paid_Status = %s, 
                            payment_date = CASE WHEN %s = 'Paid' THEN CURDATE() ELSE NULL END
                        WHERE Transactions_ID = %s
                    """, (fine_amount, status_var.get(), status_var.get(), transaction_id))
                else:
                    # Insert new fine
                    self.cursor.execute("""
                        INSERT INTO Fines (fine_total, Paid_Status, Transactions_ID, 
                                         payment_date, OverDue_Days)
                        VALUES (%s, %s, %s, 
                               CASE WHEN %s = 'Paid' THEN CURDATE() ELSE NULL END,
                               DATEDIFF(CURDATE(), (SELECT Due_date FROM Transactions 
                                                  WHERE Transactions_ID = %s)))
                    """, (fine_amount, status_var.get(), transaction_id, 
                          status_var.get(), transaction_id))

                self.db.commit()
                messagebox.showinfo("Success", "Fine has been recorded successfully!")
                
                # Clear entries
                transaction_id_var.set("")
                fine_amount_var.set("")
                status_var.set("Unpaid")
                
                # Refresh the display
                refresh_transactions()

            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numeric values!")
            except mysql.connector.Error as err:
                self.db.rollback()
                messagebox.showerror("Database Error", f"Failed to record fine: {err}")

        def on_tree_select(event):
            selected = tree.selection()
            if selected:
                item = tree.item(selected[0])
                values = item['values']
                transaction_id_var.set(values[0])  # Set Transaction ID
                if values[5].startswith('$'):  # Fine amount
                    fine_amount_var.set(values[5][1:])  # Remove $ symbol
                status_var.set(values[6])  # Status

        # Bind tree selection event
        tree.bind('<<TreeviewSelect>>', on_tree_select)

        # Add buttons frame
        button_frame = tk.Frame(form_frame, bg=COLORS['surface'])
        button_frame.pack(fill=tk.X, pady=(10, 0))

        # Add buttons with modern styling
        self.create_custom_button(button_frame, "Add/Update Fine", add_or_update_fine,
                                color=COLORS['primary']).pack(side=tk.LEFT, padx=5)
        self.create_custom_button(button_frame, "Clear", lambda: [
            transaction_id_var.set(""),
            fine_amount_var.set(""),
            status_var.set("Unpaid")
        ], color=COLORS['secondary']).pack(side=tk.LEFT, padx=5)

        # Initial load of transactions
        refresh_transactions()

    def show_events(self):
        self.clear_main_frame()
        
        # Create header
        self.create_section_header(self.main_frame, "Library Events")

        # Create main container
        container = tk.Frame(self.main_frame, bg=COLORS['background'])
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create Treeview frame
        tree_frame = tk.Frame(container, bg=COLORS['surface'], padx=20, pady=20)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Create Treeview with modern styling
        tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Location", "Date"), show="headings")
        tree.heading("ID", text="Event ID")
        tree.heading("Name", text="Event Name")
        tree.heading("Location", text="Location")
        tree.heading("Date", text="Date")

        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        x_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Pack tree and scrollbars
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        try:
            self.cursor.execute("SELECT * FROM Library_Events")
            for row in self.cursor.fetchall():
                tree.insert("", "end", values=(
                    row['event_id'],
                    row['event_name'],
                    row['location'],
                    row['date']
                ))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch events: {err}")

    def show_staff(self):
        self.clear_main_frame()
        
        # Create header
        self.create_section_header(self.main_frame, "Staff Management")

        # Create main container
        container = tk.Frame(self.main_frame, bg=COLORS['background'])
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create form frame for staff entry
        form_frame = tk.Frame(container, bg=COLORS['surface'], padx=20, pady=20)
        form_frame.pack(fill=tk.X, pady=(0, 20))

        # Staff entry fields
        fields_frame = tk.Frame(form_frame, bg=COLORS['surface'])
        fields_frame.pack(fill=tk.X, pady=5)

        # Email field
        tk.Label(fields_frame, text="Email:", 
                bg=COLORS['surface'],
                font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=5)
        email_var = tk.StringVar()
        email_entry = tk.Entry(fields_frame, textvariable=email_var,
                             font=('Segoe UI', 10))
        email_entry.pack(side=tk.LEFT, padx=5)

        # Address field
        tk.Label(fields_frame, text="Address:", 
                bg=COLORS['surface'],
                font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=5)
        address_var = tk.StringVar()
        address_entry = tk.Entry(fields_frame, textvariable=address_var,
                               font=('Segoe UI', 10))
        address_entry.pack(side=tk.LEFT, padx=5)

        # Phone field
        tk.Label(fields_frame, text="Phone:", 
                bg=COLORS['surface'],
                font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=5)
        phone_var = tk.StringVar()
        phone_entry = tk.Entry(fields_frame, textvariable=phone_var,
                             font=('Segoe UI', 10))
        phone_entry.pack(side=tk.LEFT, padx=5)

        # Create Treeview frame
        tree_frame = tk.Frame(container, bg=COLORS['surface'], padx=20, pady=20)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Create Treeview with modern styling
        tree = ttk.Treeview(tree_frame, columns=("ID", "Email", "Address", "Phone"), show="headings")
        tree.heading("ID", text="Staff ID")
        tree.heading("Email", text="Email")
        tree.heading("Address", text="Address")
        tree.heading("Phone", text="Phone")

        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        x_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Pack tree and scrollbars
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        def refresh_staff():
            for item in tree.get_children():
                tree.delete(item)
            try:
                self.cursor.callproc('sp_select_staff', ('',))
                for result in self.cursor.stored_results():
                    for row in result.fetchall():
                        tree.insert("", "end", values=(
                            row['Staff_ID'],
                            row['Email'],
                            row['address'],
                            row['phone_no']
                        ))
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Failed to fetch staff data: {err}")

        def add_staff():
            if not email_var.get() or not address_var.get() or not phone_var.get():
                messagebox.showwarning("Input Error", "All fields are required!")
                return

            try:
                self.cursor.callproc('sp_insert_staff', 
                                   (email_var.get(), address_var.get(), phone_var.get()))
                self.db.commit()
                messagebox.showinfo("Success", "Staff member added successfully!")
                
                # Clear entries
                email_var.set("")
                address_var.set("")
                phone_var.set("")
                
                refresh_staff()
            except mysql.connector.Error as err:
                self.db.rollback()
                messagebox.showerror("Database Error", f"Failed to add staff member: {err}")

        def delete_staff():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Selection Required", "Please select a staff member to delete!")
                return

            if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this staff member?"):
                return

            staff_id = tree.item(selected[0])['values'][0]
            
            try:
                self.cursor.callproc('sp_delete_staff', (staff_id,))
                self.db.commit()
                messagebox.showinfo("Success", "Staff member deleted successfully!")
                refresh_staff()
            except mysql.connector.Error as err:
                self.db.rollback()
                messagebox.showerror("Database Error", f"Failed to delete staff member: {err}")

        def update_staff():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Selection Required", "Please select a staff member to update!")
                return

            staff_id = tree.item(selected[0])['values'][0]
            email = email_var.get().strip()
            address = address_var.get().strip()
            phone = phone_var.get().strip()

            if not email or not address or not phone:
                messagebox.showerror("Input Error", "All fields are required!")
                return

            try:
                self.cursor.callproc('sp_update_staff', 
                                   (staff_id, email, address, phone))
                self.db.commit()
                messagebox.showinfo("Success", "Staff member updated successfully!")
                
                # Clear entries
                email_var.set("")
                address_var.set("")
                phone_var.set("")
                
                refresh_staff()
            except mysql.connector.Error as err:
                self.db.rollback()
                messagebox.showerror("Database Error", f"Failed to update staff member: {err}")

        def on_tree_select(event):
            selected = tree.selection()
            if selected:
                item = tree.item(selected[0])
                values = item['values']
                email_var.set(values[1])
                address_var.set(values[2])
                phone_var.set(values[3])

        # Bind tree selection event
        tree.bind('<<TreeviewSelect>>', on_tree_select)

        # Add buttons frame
        button_frame = tk.Frame(form_frame, bg=COLORS['surface'])
        button_frame.pack(fill=tk.X, pady=(10, 0))

        # Add buttons with modern styling
        self.create_custom_button(button_frame, "Add Staff", add_staff,
                                color=COLORS['success']).pack(side=tk.LEFT, padx=5)
        self.create_custom_button(button_frame, "Delete Staff", delete_staff,
                                color=COLORS['danger']).pack(side=tk.LEFT, padx=5)
        self.create_custom_button(button_frame, "Update Staff", update_staff,
                                color=COLORS['warning']).pack(side=tk.LEFT, padx=5)
        self.create_custom_button(button_frame, "Clear", lambda: [
            email_var.set(""),
            address_var.set(""),
            phone_var.set("")
        ], color=COLORS['secondary']).pack(side=tk.LEFT, padx=5)

        # Initial load of staff
        refresh_staff()

    def show_reports(self):
        self.clear_main_frame()
        
        # Create header
        self.create_section_header(self.main_frame, "Library Reports")
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Add Change History Tab
        changes_frame = ttk.Frame(notebook)
        notebook.add(changes_frame, text="📝 Change History")
        
        # Create filter frame
        filter_frame = tk.Frame(changes_frame, bg=COLORS['surface'])
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Entity type filter
        tk.Label(filter_frame, text="Entity Type:", 
                bg=COLORS['surface']).pack(side=tk.LEFT, padx=5)
        entity_var = tk.StringVar(value="All")
        entity_menu = ttk.Combobox(filter_frame, 
                                 values=["All", "Member", "Book", "Staff"],
                                 textvariable=entity_var,
                                 state="readonly")
        entity_menu.pack(side=tk.LEFT, padx=5)
        
        # Create Treeview for changes
        changes_tree = ttk.Treeview(changes_frame, 
                                  columns=("Type", "ID", "Action", "Date", "Details"),
                                  show="headings")
        changes_tree.heading("Type", text="Entity Type")
        changes_tree.heading("ID", text="ID")
        changes_tree.heading("Action", text="Action")
        changes_tree.heading("Date", text="Date")
        changes_tree.heading("Details", text="Details")
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(changes_frame, orient="vertical", 
                                  command=changes_tree.yview)
        x_scrollbar = ttk.Scrollbar(changes_frame, orient="horizontal", 
                                  command=changes_tree.xview)
        changes_tree.configure(yscrollcommand=y_scrollbar.set, 
                             xscrollcommand=x_scrollbar.set)
        
        # Pack tree and scrollbars
        changes_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        def refresh_changes(*args):
            for item in changes_tree.get_children():
                changes_tree.delete(item)
            try:
                if entity_var.get() == "All":
                    self.cursor.execute("""
                        SELECT * FROM vw_recent_changes
                        ORDER BY ChangeDate DESC
                        LIMIT 100
                    """)
                else:
                    self.cursor.execute("""
                        SELECT * FROM vw_recent_changes
                        WHERE EntityType = %s
                        ORDER BY ChangeDate DESC
                        LIMIT 100
                    """, (entity_var.get(),))
                
                for row in self.cursor.fetchall():
                    changes_tree.insert("", "end", values=(
                        row['EntityType'],
                        row['EntityID'],
                        row['Action'],
                        row['ChangeDate'],
                        row['Details']
                    ))
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", 
                                   f"Failed to fetch change history: {err}")

        def show_audit_history():
            selected = changes_tree.selection()
            if not selected:
                messagebox.showwarning("Selection Required", 
                                     "Please select an item to view its history!")
                return

            item = changes_tree.item(selected[0])
            entity_type = item['values'][0]
            entity_id = item['values'][1]

            try:
                self.cursor.execute("""
                    SELECT get_audit_history(%s, %s) as history
                """, (entity_type, entity_id))
                
                history = self.cursor.fetchone()['history']
                
                # Create popup window
                popup = tk.Toplevel(self.root)
                popup.title(f"Audit History - {entity_type} #{entity_id}")
                popup.geometry("600x400")
                
                # Add text widget
                text = tk.Text(popup, wrap=tk.WORD, padx=10, pady=10)
                text.pack(fill=tk.BOTH, expand=True)
                text.insert("1.0", history)
                text.config(state="disabled")
                
                # Add close button
                tk.Button(popup, text="Close", 
                         command=popup.destroy).pack(pady=10)
                
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", 
                                   f"Failed to fetch audit history: {err}")

        # Bind events
        entity_menu.bind('<<ComboboxSelected>>', refresh_changes)
        changes_tree.bind('<Double-1>', lambda e: show_audit_history())
        
        # Add View History button
        tk.Button(filter_frame, text="View Full History",
                 command=show_audit_history).pack(side=tk.LEFT, padx=20)
        
        # Initial load
        refresh_changes()

        # Tab 1: Book Statistics
        book_stats_frame = ttk.Frame(notebook)
        notebook.add(book_stats_frame, text="📚 Book Statistics")
        
        # Add filter frame
        filter_frame = tk.Frame(book_stats_frame, bg=COLORS['surface'])
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(filter_frame, text="Filter by Category:", 
                bg=COLORS['surface']).pack(side=tk.LEFT, padx=5)
        category_var = tk.StringVar(value="All")
        category_menu = ttk.Combobox(filter_frame, textvariable=category_var)
        category_menu.pack(side=tk.LEFT, padx=5)
        
        # Populate category dropdown
        try:
            self.cursor.execute("SELECT DISTINCT book_category FROM Books WHERE book_category IS NOT NULL")
            categories = ["All"] + [row['book_category'] for row in self.cursor.fetchall()]
            category_menu['values'] = categories
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch categories: {err}")
        
        book_tree = ttk.Treeview(book_stats_frame, columns=("Title", "Category", "Borrowed", "Status", "Authors", "ISBN"), show="headings")
        book_tree.heading("Title", text="Book Title")
        book_tree.heading("Category", text="Category")
        book_tree.heading("Borrowed", text="Times Borrowed")
        book_tree.heading("Status", text="Status")
        book_tree.heading("Authors", text="Authors")
        book_tree.heading("ISBN", text="ISBN")
        book_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        def update_book_stats(*args):
            for item in book_tree.get_children():
                book_tree.delete(item)
            try:
                if category_var.get() == "All":
                    self.cursor.execute("SELECT * FROM vw_book_statistics ORDER BY times_borrowed DESC")
                else:
                    self.cursor.execute("""
                        SELECT * FROM vw_book_statistics 
                        WHERE book_category = %s 
                        ORDER BY times_borrowed DESC
                    """, (category_var.get(),))
                
                for row in self.cursor.fetchall():
                    book_tree.insert("", "end", values=(
                        row['Title'],
                        row['book_category'],
                        row['times_borrowed'],
                        row['AvailabilityStatus'],
                        row['authors'],
                        row['ISBN']
                    ))
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Failed to fetch book statistics: {err}")

        category_menu.bind('<<ComboboxSelected>>', update_book_stats)
        update_book_stats()  # Initial load

        # Tab 2: Member Activity
        member_frame = ttk.Frame(notebook)
        notebook.add(member_frame, text="👥 Member Activity")
        
        # Add search frame
        search_frame = tk.Frame(member_frame, bg=COLORS['surface'])
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(search_frame, text="Search Member:", 
                bg=COLORS['surface']).pack(side=tk.LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        member_tree = ttk.Treeview(member_frame, columns=("Member", "Transactions", "Fines", "Amount", "Events", "LastActivity"), show="headings")
        member_tree.heading("Member", text="Member Details")
        member_tree.heading("Transactions", text="Total Transactions")
        member_tree.heading("Fines", text="Total Fines")
        member_tree.heading("Amount", text="Fine Amount")
        member_tree.heading("Events", text="Events Attended")
        member_tree.heading("LastActivity", text="Last Activity")
        member_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        def search_members(*args):
            for item in member_tree.get_children():
                member_tree.delete(item)
            try:
                search_term = f"%{search_var.get()}%"
                self.cursor.execute("""
                    SELECT m.*, 
                           COALESCE(MAX(t.Transactions_Date), 'Never') as last_activity
                    FROM vw_member_activity m
                    LEFT JOIN Transactions t ON m.MemberID = t.MemberID
                    WHERE m.MemberDetails LIKE %s
                    GROUP BY m.MemberID, m.MemberDetails, m.total_transactions, 
                             m.total_fines, m.total_fine_amount, m.events_attended
                    ORDER BY total_transactions DESC
                """, (search_term,))
                
                for row in self.cursor.fetchall():
                    member_tree.insert("", "end", values=(
                        row['MemberDetails'],
                        row['total_transactions'],
                        row['total_fines'],
                        f"${row['total_fine_amount'] or 0:.2f}",
                        row['events_attended'],
                        row['last_activity']
                    ))
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Failed to fetch member activity: {err}")

        search_var.trace('w', search_members)
        search_members()  # Initial load

        # Tab 3: Overdue Books
        overdue_frame = ttk.Frame(notebook)
        notebook.add(overdue_frame, text="⚠️ Overdue Books")
        
        # Add filter frame
        overdue_filter_frame = tk.Frame(overdue_frame, bg=COLORS['surface'])
        overdue_filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(overdue_filter_frame, text="Days Overdue:", 
                bg=COLORS['surface']).pack(side=tk.LEFT, padx=5)
        days_var = tk.StringVar(value="All")
        days_menu = ttk.Combobox(overdue_filter_frame, 
                                values=["All", "7+ days", "14+ days", "30+ days"],
                                textvariable=days_var)
        days_menu.pack(side=tk.LEFT, padx=5)
        
        overdue_tree = ttk.Treeview(overdue_frame, 
                                   columns=("Title", "Member", "DueDate", "DaysOverdue", "Fine", "Contact"), 
                                   show="headings")
        overdue_tree.heading("Title", text="Book Title")
        overdue_tree.heading("Member", text="Member")
        overdue_tree.heading("DueDate", text="Due Date")
        overdue_tree.heading("DaysOverdue", text="Days Overdue")
        overdue_tree.heading("Fine", text="Fine Amount")
        overdue_tree.heading("Contact", text="Contact Info")
        overdue_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        def update_overdue(*args):
            for item in overdue_tree.get_children():
                overdue_tree.delete(item)
            try:
                days_filter = days_var.get()
                if days_filter == "All":
                    self.cursor.execute("""
                        SELECT * FROM vw_overdue_books
                        ORDER BY days_overdue DESC
                    """)
                else:
                    min_days = int(days_filter.split("+")[0])
                    self.cursor.execute("""
                        SELECT * FROM vw_overdue_books
                        WHERE days_overdue >= %s
                        ORDER BY days_overdue DESC
                    """, (min_days,))
                
                for row in self.cursor.fetchall():
                    overdue_tree.insert("", "end", values=(
                        row['Title'],
                        row['MemberDetails'],
                        row['Due_date'],
                        row['days_overdue'],
                        f"${row['fine_total'] or 0:.2f}",
                        row['contact_number'] or "No contact info"
                    ))
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Failed to fetch overdue books: {err}")

        days_menu.bind('<<ComboboxSelected>>', update_overdue)
        update_overdue()  # Initial load

        # Tab 4: Financial Reports
        finance_frame = ttk.Frame(notebook)
        notebook.add(finance_frame, text="💰 Financial Reports")
        
        # Create summary cards
        summary_frame = tk.Frame(finance_frame, bg=COLORS['surface'])
        summary_frame.pack(fill=tk.X, padx=5, pady=5)
        
        try:
            # Total fines collected
            self.cursor.execute("""
                SELECT 
                    SUM(CASE WHEN Paid_Status = 'Paid' THEN fine_total ELSE 0 END) as collected,
                    SUM(CASE WHEN Paid_Status = 'Unpaid' THEN fine_total ELSE 0 END) as pending
                FROM Fines
            """)
            fine_stats = self.cursor.fetchone()
            
            # Create stat cards
            self.create_stat_card(summary_frame, "Collected Fines", 
                                f"${fine_stats['collected'] or 0:.2f}", "💵")
            self.create_stat_card(summary_frame, "Pending Fines", 
                                f"${fine_stats['pending'] or 0:.2f}", "⏳")
            
            # Add monthly trend chart
            self.cursor.execute("""
                SELECT 
                    DATE_FORMAT(payment_date, '%Y-%m') as month,
                    SUM(fine_total) as total
                FROM Fines
                WHERE Paid_Status = 'Paid'
                GROUP BY DATE_FORMAT(payment_date, '%Y-%m')
                ORDER BY month DESC
                LIMIT 12
            """)
            months = []
            totals = []
            for row in self.cursor.fetchall():
                months.append(row['month'])
                totals.append(float(row['total']))
            
            if months and totals:
                plt.style.use('seaborn')
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.plot(months, totals, marker='o')
                ax.set_title('Monthly Fine Collection Trend', pad=20)
                ax.set_ylabel('Amount Collected ($)')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                
                canvas = FigureCanvasTkAgg(fig, master=finance_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(pady=10, fill=tk.BOTH, expand=True)
        
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch financial data: {err}")

        # Tab 5: Library Statistics
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="📊 Statistics")
        
        try:
            # Query the statistics view instead of using the function
            self.cursor.execute("SELECT * FROM vw_library_statistics")
            stats = self.cursor.fetchone()
            
            # Create statistics text
            stats_text = f"""Library Overview:
                    - Total Books: {stats['total_books']}
                    - Total Members: {stats['total_members']}
                    - Total Transactions: {stats['total_transactions']}
                    - Currently Borrowed Books: {stats['active_loans']}
                    - Overdue Books: {stats['overdue_books']}
                    - Total Unpaid Fines: ${stats['total_unpaid_fines']:.2f}"""
            
            ttk.Label(stats_frame, text=stats_text, font=("Segoe UI", 12)).pack(pady=20)
            
            # Add charts frame
            charts_frame = tk.Frame(stats_frame)
            charts_frame.pack(fill=tk.BOTH, expand=True)
            
            # Book categories chart
            self.cursor.execute("""
                SELECT book_category, COUNT(*) as count 
                FROM Books 
                GROUP BY book_category
                ORDER BY count DESC
            """)
            categories = []
            counts = []
            for row in self.cursor.fetchall():
                categories.append(row['book_category'] or 'Uncategorized')
                counts.append(row['count'])

            if categories and counts:
                # Create pie chart
                fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
                
                # Bar chart
                ax1.bar(categories, counts)
                ax1.set_title('Books by Category')
                ax1.set_ylabel('Number of Books')
                plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
                
                # Pie chart
                ax2.pie(counts, labels=categories, autopct='%1.1f%%')
                ax2.set_title('Category Distribution')
                
                plt.tight_layout()
                canvas1 = FigureCanvasTkAgg(fig1, master=charts_frame)
                canvas1.draw()
                canvas1.get_tk_widget().pack(pady=10)
                
                # Add transaction trend chart
                self.cursor.execute("""
                    SELECT 
                        DATE_FORMAT(Transactions_Date, '%Y-%m') as month,
                        COUNT(*) as count
                    FROM Transactions
                    GROUP BY DATE_FORMAT(Transactions_Date, '%Y-%m')
                    ORDER BY month DESC
                    LIMIT 12
                """)
                months = []
                transaction_counts = []
                for row in self.cursor.fetchall():
                    months.append(row['month'])
                    transaction_counts.append(row['count'])
                
                if months and transaction_counts:
                    fig2, ax3 = plt.subplots(figsize=(10, 4))
                    ax3.plot(months, transaction_counts, marker='o')
                    ax3.set_title('Monthly Transaction Trend')
                    ax3.set_ylabel('Number of Transactions')
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    
                    canvas2 = FigureCanvasTkAgg(fig2, master=charts_frame)
                    canvas2.draw()
                    canvas2.get_tk_widget().pack(pady=10)
        
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch library statistics: {err}")

if __name__ == "__main__":
    print("Starting main program...")
    root = tk.Tk()
    app = LibraryManagementApp(root)
    print("Entering main loop...")
    root.mainloop()
    print("Application closed.")
