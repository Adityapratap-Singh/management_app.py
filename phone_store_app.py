import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector

class PhoneStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phone Store App")

        # Connect to MySQL database
        try:
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root@123",
                database="phones"
            )
            self.db_cursor = self.db_connection.cursor()
            self.create_tables()
        except mysql.connector.Error as e:
            print(f"Error connecting to the database: {e}")
            self.root.destroy()

        # Create main frame
        self.create_main_frame()

        # Display welcome message
        self.welcome_label = tk.Label(self.frame, text="Welcome to the Phone Store App!", font=("Arial", 16, "bold"))
        self.welcome_label.pack(pady=20)

        # Initialize selected product label
        self.selected_product_label = tk.Label(self.frame, text="Selected Product: None", font=("Arial", 12))
        self.selected_product_label.pack(pady=10)

        # Initialize grand total label
        self.grand_total_label = tk.Label(self.frame, text="Grand Total: $0.00", font=("Arial", 12))
        self.grand_total_label.pack(pady=10)

        # Create a combobox for selecting product type
        self.product_type_combobox = ttk.Combobox(self.frame, values=["Phones", "Laptops"])
        self.product_type_combobox.set("Select Product Type")
        self.product_type_combobox.pack(side="left", padx=10, pady=10)

        # Add a button to view details based on the selected product type
        self.view_details_button = ttk.Button(self.frame, text="View Details", command=self.view_selected_details)
        self.view_details_button.pack(side="left", padx=10, pady=10)

        # Add fade-in animation
        self.fade_in_animation()

    def create_main_frame(self):
        # Create a frame for the table
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        # Create a treeview widget for the table
        self.create_treeview()

        # Create add, select, remove, calculate total, and search buttons
        self.create_buttons()

    def create_tables(self):
        # Create a table for phones
        phones_table = """
        CREATE TABLE IF NOT EXISTS phones (
            id INT AUTO_INCREMENT PRIMARY KEY,
            brand VARCHAR(255),
            model VARCHAR(255),
            price DECIMAL(10, 2),
            processor VARCHAR(255)
        )
        """
        self.db_cursor.execute(phones_table)

        # Create a table for laptops
        laptops_table = """
        CREATE TABLE IF NOT EXISTS laptops (
            id INT AUTO_INCREMENT PRIMARY KEY,
            brand VARCHAR(255),
            model VARCHAR(255),
            price DECIMAL(10, 2),
            processor VARCHAR(255)
        )
        """
        self.db_cursor.execute(laptops_table)

        self.db_connection.commit()

    def fade_in_animation(self):
        # Function to gradually increase the alpha (transparency) of the root window
        def fade_in(alpha):
            alpha += 0.01
            if alpha < 1.0:
                self.root.after(10, fade_in, alpha)
                self.root.attributes("-alpha", alpha)
            else:
                self.root.attributes("-alpha", 1.0)

        # Set initial transparency to 0
        self.root.attributes("-alpha", 0.0)

        # Schedule the fade-in animation after a delay
        self.root.after(500, fade_in, 0.0)

    def create_treeview(self):
        self.tree = ttk.Treeview(self.frame, selectmode="browse")
        self.tree["columns"] = ("Brand", "Model", "Price", "Processor")

        # Define column headings and widths
        columns = ["Brand", "Model", "Price", "Processor"]
        headings = ["Brand", "Model", "Price", "Processor"]
        widths = [150, 150, 80, 150]

        # Configure columns
        for col, heading, width in zip(columns, headings, widths):
            self.tree.heading(col, text=heading, anchor="w")
            self.tree.column(col, anchor="w", width=width)

        self.tree.pack(fill="both", expand=True)

        # Fetch data from the database (phones table)
        self.db_cursor.execute("SELECT brand, model, price, processor FROM phones")
        phone_rows = self.db_cursor.fetchall()

        # Insert data into the table
        for row in phone_rows:
            self.tree.insert("", "end", values=row)

        # Fetch data from the database (laptops table)
        self.db_cursor.execute("SELECT brand, model, price, processor FROM laptops")
        laptop_rows = self.db_cursor.fetchall()

        # Insert data into the table
        for row in laptop_rows:
            self.tree.insert("", "end", values=row)

    def create_buttons(self):
        # Create add button
        add_button = ttk.Button(self.frame, text="Add Product", command=self.add_product)
        add_button.pack(side="left", padx=10, pady=10)

        # Create select button
        select_button = ttk.Button(self.frame, text="Select Product", command=self.select_product)
        select_button.pack(side="left", padx=10, pady=10)

        # Create remove button
        remove_button = ttk.Button(self.frame, text="Remove Product", command=self.remove_product)
        remove_button.pack(side="left", padx=10, pady=10)

        # Create calculate total button
        calculate_total_button = ttk.Button(self.frame, text="Calculate Total", command=self.calculate_grand_total)
        calculate_total_button.pack(side="left", padx=10, pady=10)

        # Create search button
        search_button = ttk.Button(self.frame, text="Search", command=self.search_product)
        search_button.pack(side="left", padx=10, pady=10)

    def add_product(self):
        # Prompt user for password
        password = simpledialog.askstring("Password", "Enter password:", show='*')

        # Check if password is correct
        if password == "SCOE":  # Replace "your_password_here" with your actual password
            # Create a new window for adding products
            add_window = tk.Toplevel(self.root)
            add_window.title("Add Product")

            # Create entry fields
            labels = ["Brand", "Model", "Price", "Processor"]
            entries = []

            for i, label in enumerate(labels):
                ttk.Label(add_window, text=f"{label}:").grid(row=i, column=0, padx=10, pady=10)
                entry = ttk.Entry(add_window)
                entry.grid(row=i, column=1, padx=10, pady=10)
                entries.append(entry)

            # Create a button to submit the data
            submit_button = ttk.Button(add_window, text="Submit", command=lambda: self.submit_product(
                *[entry.get() for entry in entries], add_window))
            submit_button.grid(row=len(labels), columnspan=2, pady=10)
        else:
            messagebox.showerror("Error", "Incorrect password. Access denied.")

    def submit_product(self, brand, model, price, processor, add_window):
        # Determine the selected product type
        selected_type = self.product_type_combobox.get()
    
        if selected_type == "Phones":
            # Insert the data into the phones table
            table_name = "phones"
        elif selected_type == "Laptops":
            # Insert the data into the laptops table
            table_name = "laptops"
        else:
            messagebox.showinfo("Info", "Please select a valid product type.")
            return
    
        query = f"INSERT INTO {table_name} (brand, model, price, processor) VALUES (%s, %s, %s, %s)"
        values = (brand, model, price, processor)
    
        try:
            self.db_cursor.execute(query, values)
            self.db_connection.commit()
            self.refresh_table()
            messagebox.showinfo("Success", "Product added successfully.")
            add_window.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def select_product(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_values = self.tree.item(selected_item, 'values')
            self.selected_product_label.config(text=f"Selected Product: {selected_values}")
        else:
            messagebox.showinfo("Info", "Please select a product.")

    def remove_product(self):
        selected_item = self.tree.selection()
        if selected_item:
            confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to remove the selected product?")
            if confirmation:
                selected_values = self.tree.item(selected_item, 'values')
                self.delete_product(selected_values)
        else:
            messagebox.showinfo("Info", "Please select a product to remove.")


    def delete_product(self, selected_values):
        # Determine the selected product type
        selected_type = self.product_type_combobox.get()

        if selected_type == "Phones":
            # Delete the selected product from the phones table
            table_name = "phones"
        elif selected_type == "Laptops":
            # Delete the selected product from the laptops table
            table_name = "laptops"
        else:
            messagebox.showinfo("Info", "Please select a valid product type.")
            return

        query = f"DELETE FROM {table_name} WHERE brand = %s AND model = %s AND price = %s AND processor = %s"
        values = tuple(selected_values)

        try:
            self.db_cursor.execute(query, values)
            self.db_connection.commit()
            self.refresh_table()
            messagebox.showinfo("Success", "Product removed successfully.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def calculate_grand_total(self):
        selected_items = self.tree.selection()
        grand_total = 0.0

        for item in selected_items:
            values = self.tree.item(item, 'values')
            price = float(values[2]) if values and values[2] else 0.0
            grand_total += price

        self.grand_total_label.config(text=f"Grand Total: ${grand_total:.2f}")

    def search_product(self):
        # Create a search window
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Product")

        # Create entry field for search
        search_entry = ttk.Entry(search_window)
        search_entry.pack(padx=10, pady=10)

        # Create a button to perform the search
        search_button = ttk.Button(search_window, text="Search", command=lambda: self.perform_search(search_entry.get()))
        search_button.pack(pady=10)

    def perform_search(self, search_term):
        # Search for products in the phones and laptops tables
        query = "SELECT brand, model, price, processor FROM phones WHERE brand LIKE %s OR model LIKE %s OR price LIKE %s OR processor LIKE %s"
        search_term = f"%{search_term}%"
        values = (search_term, search_term, search_term, search_term)

        try:
            self.db_cursor.execute(query, values)
            phone_search_results = self.db_cursor.fetchall()

            # Display phone search results in a new window
            self.display_search_results("Phone Search Results", phone_search_results)

            # Search for products in the laptops table
            query = "SELECT brand, model, price, processor FROM laptops WHERE brand LIKE %s OR model LIKE %s OR price LIKE %s OR processor LIKE %s"
            self.db_cursor.execute(query, values)
            laptop_search_results = self.db_cursor.fetchall()

            # Display laptop search results in a new window
            self.display_search_results("Laptop Search Results", laptop_search_results)

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def display_search_results(self, title, search_results):
        results_window = tk.Toplevel(self.root)
        results_window.title(title)

        search_tree = ttk.Treeview(results_window, columns=("Brand", "Model", "Price", "Processor"))

        # Configure columns
        columns = ["Brand", "Model", "Price", "Processor"]
        headings = ["Brand", "Model", "Price", "Processor"]
        widths = [150, 150, 80, 150]

        for col, heading, width in zip(columns, headings, widths):
            search_tree.heading(col, text=heading, anchor="w")
            search_tree.column(col, anchor="w", width=width)

        search_tree.pack(fill="both", expand=True)

        # Insert search results into the treeview
        for row in search_results:
            search_tree.insert("", "end", values=row)

    def view_selected_details(self):
        selected_type = self.product_type_combobox.get()

        if selected_type == "Phones":
            # Fetch and display phone details from the database
            self.display_phone_details()
        elif selected_type == "Laptops":
            # Fetch and display laptop details from the database
            self.display_laptop_details()
        else:
            messagebox.showinfo("Info", "Please select a valid product type.")

    def display_phone_details(self):
        # Fetch phone details from the database (phones table)
        query = "SELECT * FROM phones"

        try:
            self.db_cursor.execute(query)
            phone_details = self.db_cursor.fetchall()

            # Display details in a new window
            details_window = tk.Toplevel(self.root)
            details_window.title("Phone Details")

            details_tree = ttk.Treeview(details_window, columns=("Brand", "Model", "Price", "Processor"))

            # Configure columns
            columns = ["Brand", "Model", "Price", "Processor"]
            headings = ["Brand", "Model", "Price", "Processor"]
            widths = [150, 150, 80, 150]

            for col, heading, width in zip(columns, headings, widths):
                details_tree.heading(col, text=heading, anchor="w")
                details_tree.column(col, anchor="w", width=width)

            details_tree.pack(fill="both", expand=True)

            # Insert phone details into the treeview
            for phone in phone_details:
                details_tree.insert("", "end", values=phone)

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def display_laptop_details(self):
        # Fetch laptop details from the database (laptops table)
        query = "SELECT brand, model, processor, price FROM laptops ORDER BY brand ASC, price ASC"

        try:
            self.db_cursor.execute(query)
            laptop_details = self.db_cursor.fetchall()

            # Display details in a new window
            details_window = tk.Toplevel(self.root)
            details_window.title("Laptop Details")

            details_tree = ttk.Treeview(details_window, columns=("Brand", "Model", "Processor", "Price"))

            # Configure columns
            columns = ["Brand", "Model", "Price", "Processor"]
            headings = ["Brand", "Model", "Price", "Processor"]
            widths = [150, 150, 80, 150]

            for col, heading, width in zip(columns, headings, widths):
                details_tree.heading(col, text=heading, anchor="w")
                details_tree.column(col, anchor="w", width=width)

            details_tree.pack(fill="both", expand=True)

            # Insert laptop details into the treeview
            for laptop in laptop_details:
                details_tree.insert("", "end", values=laptop)

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def refresh_table(self):
        # Clear existing data in the table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch data from the phones table
        self.db_cursor.execute("SELECT brand, model, price, processor FROM phones")
        phone_rows = self.db_cursor.fetchall()

        # Insert phone data into the table
        for row in phone_rows:
            self.tree.insert("", "end", values=row)

        # Fetch data from the laptops table
        self.db_cursor.execute("SELECT brand, model, price, processor FROM laptops")
        laptop_rows = self.db_cursor.fetchall()

        # Insert laptop data into the table
        for row in laptop_rows:
            self.tree.insert("", "end", values=row)

    def on_closing(self):
        # Close the database connection and exit the application
        if hasattr(self, 'db_cursor') and hasattr(self, 'db_connection'):
            self.db_cursor.close()
            self.db_connection.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhoneStoreApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
