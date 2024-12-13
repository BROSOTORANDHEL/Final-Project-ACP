import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog




def populate_fields(event):
    selected_item = tree.focus()
    if selected_item:
        values = tree.item(selected_item, "values")
        product_name_entry_main.config(state="normal")
        product_name_entry_main.delete(0, tk.END)
        product_name_entry_main.insert(0, values[0])
        product_name_entry_main.config(state="readonly")
        price_entry_main.config(state="normal")
        price_entry_main.delete(0, tk.END)
        price_entry_main.insert(0, values[2])
        price_entry_main.config(state="readonly")



def add_product_window():
    add_product_win = tk.Toplevel(root)
    add_product_win.title("Add Product")

    window_width = 400
    window_height = 325
    x = (root.winfo_screenwidth() // 2) - (window_width // 2)
    y = (root.winfo_screenheight() // 2) - (window_height // 2)
    add_product_win.geometry(f"{window_width}x{window_height}+{x}+{y}")

    input_frame = tk.Frame(add_product_win)
    input_frame.pack(padx=20, pady=20)

    tk.Label(input_frame, text="Product Name:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5,
                                                                                 sticky='w')
    product_name_entry = tk.Entry(input_frame, font=("Arial", 12, "bold"), width=32, bg="black", fg="white")
    product_name_entry.grid(row=1, column=0, padx=5, pady=5, ipady=7)

    tk.Label(input_frame, text="Quantity:", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=5, pady=5,
                                                                             sticky='w')
    quantity_entry = tk.Entry(input_frame, font=("Arial", 12), width=32, bg="black", fg="white")
    quantity_entry.grid(row=3, column=0, padx=5, pady=5, ipady=7)

    tk.Label(input_frame, text="Price:", font=("Arial", 10, "bold")).grid(row=4, column=0, padx=5, pady=5, sticky='w')
    price_entry = tk.Entry(input_frame, font=("Arial", 12), width=32, bg="black", fg="white")
    price_entry.grid(row=5, column=0, padx=5, pady=5, ipady=7)

    def submit_product():
        product_name = product_name_entry.get()
        quantity = quantity_entry.get()
        price = price_entry.get()

        if product_name and quantity and price:
            try:
                quantity = int(quantity)
                price = int(price)
                tree.insert("", tk.END, values=(product_name, quantity, price))
                add_product_win.destroy()
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid integers for quantity and price.")
        else:
            messagebox.showerror("Input Error", "Please fill all fields")

    submit_button = tk.Button(add_product_win, text="Add", command=submit_product, font=("Arial", 10, "bold"))
    submit_button.pack(pady=10)


def add_quantity_window():
    add_quantity_win = tk.Toplevel(root)
    add_quantity_win.title("Add Quantity")

    window_width = 500
    window_height = 300
    x = (root.winfo_screenwidth() // 2) - (window_width // 2)
    y = (root.winfo_screenheight() // 2) - (window_height // 2)
    add_quantity_win.geometry(f"{window_width}x{window_height}+{x}+{y}")

    input_frame = tk.Frame(add_quantity_win)
    input_frame.pack(padx=20, pady=20)

    tk.Label(input_frame, text="Product Name:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=10,
                                                                                 sticky='w')
    product_name_entry = tk.Entry(input_frame, font=("Arial", 12, "bold"), width=32, bg="black", fg="white")
    product_name_entry.grid(row=1, column=0, padx=5, pady=10, ipady=7)

    tk.Label(input_frame, text="Quantity to Add:", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=5, pady=10,
                                                                                    sticky='w')
    quantity_entry = tk.Entry(input_frame, font=("Arial", 12), width=32, bg="black", fg="white")
    quantity_entry.grid(row=3, column=0, padx=5, pady=10, ipady=7)

    def submit_quantity():
        product_name = product_name_entry.get()
        quantity_add = quantity_entry.get()

        if product_name and quantity_add:
            try:
                quantity_add = int(quantity_add)
                for tree_id in tree.get_children():
                    inventory_item = tree.item(tree_id)["values"]
                    if inventory_item[0] == product_name:
                        new_quantity = int(inventory_item[1]) + quantity_add

                        # Check if the new total quantity exceeds 20
                        if new_quantity > 20:
                            result = messagebox.askyesno(
                                "Stock Warning",
                                f"The total stock ({new_quantity}) exceeds 20. Do you still want to proceed?"
                            )
                            if not result:
                                return  # Exit if the user clicks "No"

                        tree.item(tree_id, values=(inventory_item[0], new_quantity, inventory_item[2]))
                        add_quantity_win.destroy()
                        return
                messagebox.showerror("Product Error", "Product not found. Please ensure the product is already listed.")
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid integer for quantity.")
        else:
            messagebox.showerror("Input Error", "Please fill all fields")

    add_button = tk.Button(add_quantity_win, text="Add", command=submit_quantity, font=("Arial", 10, "bold"))
    add_button.pack(pady=20)


def exit_application():
    if messagebox.askokcancel("Exit", "Do you really want to exit the program?"):
        root.quit()


def buy_product():
    try:
        product_name_entry_main.config(state="normal")
        price_entry_main.config(state="normal")

        product_name = product_name_entry_main.get()
        quantity_to_buy = int(quantity_entry_main.get())
        price = int(price_entry_main.get())

        if not product_name or quantity_to_buy <= 0 or price < 0:
            messagebox.showerror("Input Error", "Please fill the quantity and price correctly.")
            product_name_entry_main.config(state="readonly")
            price_entry_main.config(state="readonly")
            return

        for tree_id in tree.get_children():
            inventory_item = tree.item(tree_id)["values"]
            if inventory_item[0] == product_name:
                available_quantity = int(inventory_item[1])
                if quantity_to_buy > available_quantity:
                    messagebox.showerror("Stock Error", "Not enough stock available.")
                    product_name_entry_main.config(state="readonly")
                    price_entry_main.config(state="readonly")
                    return
                else:
                    break
        else:
            messagebox.showerror("Product Error", "Product not found in inventory.")
            product_name_entry_main.config(state="readonly")
            price_entry_main.config(state="readonly")
            return

        total_price = price * quantity_to_buy
        tree2.insert("", tk.END, values=(product_name, quantity_to_buy, price, total_price))
        update_total()
    except ValueError:
        messagebox.showerror("Input Error", "Please ensure quantity and price are integers.")
    finally:
        product_name_entry_main.config(state="readonly")
        price_entry_main.config(state="readonly")


def update_total():
    total = 0
    for row_id in tree2.get_children():
        total += int(tree2.item(row_id)["values"][3])
    total_entry.config(state="normal")
    total_entry.delete(0, tk.END)
    total_entry.insert(0, str(total))
    total_entry.config(state="readonly")


def calculate_change():
    try:
        total = int(total_entry.get())
        pay = int(pay_entry.get())
        if pay >= total:
            change = pay - total
            change_entry.config(state="normal")
            change_entry.delete(0, tk.END)
            change_entry.insert(0, str(change))
            change_entry.config(state="readonly")
            messagebox.showinfo("Success", "Payment accepted!")
            update_inventory()
            clear_table2()
            clear_fields()
        else:
            messagebox.showerror("Payment Error", "Insufficient payment; please pay at least the total amount.")
            change_entry.config(state="normal")
            change_entry.delete(0, tk.END)
            change_entry.config(state="readonly")
    except ValueError:
        messagebox.showerror("Payment Error", "Please enter valid integers for total and payment.")


def update_inventory():
    for row_id in tree2.get_children():
        purchased_item = tree2.item(row_id)["values"]
        purchased_name = purchased_item[0]
        purchased_quantity = int(purchased_item[1])

        for tree_id in tree.get_children():
            inventory_item = tree.item(tree_id)["values"]
            if inventory_item[0] == purchased_name:
                new_quantity = int(inventory_item[1]) - purchased_quantity
                tree.item(tree_id, values=(inventory_item[0], new_quantity, inventory_item[2]))
                break


def clear_table2():
    for row_id in tree2.get_children():
        tree2.delete(row_id)


def clear_fields():
    product_name_entry_main.config(state="normal")
    quantity_entry_main.delete(0, tk.END)
    product_name_entry_main.delete(0, tk.END)
    product_name_entry_main.config(state="readonly")

    price_entry_main.config(state="normal")
    price_entry_main.delete(0, tk.END)
    price_entry_main.config(state="readonly")

    total_entry.config(state="normal")
    total_entry.delete(0, tk.END)
    total_entry.config(state="readonly")

    pay_entry.delete(0, tk.END)

    change_entry.config(state="normal")
    change_entry.delete(0, tk.END)
    change_entry.config(state="readonly")


root = tk.Tk()
root.title("My Application")

root.attributes('-fullscreen', True)

style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
style.configure("Treeview", font=("Arial", 14, "bold"))

inventory_label = tk.Label(root, text="Inventory", font=("Arial", 16, "bold"))
inventory_label.grid(row=0, column=0, columnspan=2, pady=10, sticky='w')

columns1 = ("Product Name", "Quantity", "Price")
tree = ttk.Treeview(root, columns=columns1, show='headings', height=20)
tree.grid(row=1, column=0, padx=20, pady=20, sticky='nsew')

for col in columns1:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=200)

tree.bind("<<TreeviewSelect>>", populate_fields)

columns2 = ("Product Name", "Quantity", "Price", "Total")
tree2 = ttk.Treeview(root, columns=columns2, show='headings', height=20)
tree2.grid(row=1, column=1, padx=20, pady=20, sticky='nsew')

for col in columns2:
    tree2.heading(col, text=col)
    tree2.column(col, anchor="center", width=200)


def display_total(event):
    update_total()


tree2.bind("<<TreeviewSelect>>", display_total)

total_frame = tk.Frame(root)
total_frame.grid(row=3, column=1, padx=20, pady=10, sticky="ne")

label_style = {"font": ("Arial", 10, "bold")}
entry_style = {"font": ("Arial", 12), "width": 42, "bg": "white", "fg": "black"}
entry_style_bold = {"font": ("Arial", 12, "bold"), "width": 42, "bg": "white", "fg": "black"}

tk.Label(total_frame, text="Total:", **label_style).grid(row=0, column=0, padx=5, pady=5, sticky='w')
total_entry = tk.Entry(total_frame, **entry_style)
total_entry.grid(row=1, column=0, padx=5, pady=5, ipady=7)
total_entry.config(state="readonly")

tk.Label(total_frame, text="Pay:", **label_style).grid(row=2, column=0, padx=5, pady=5, sticky='w')
pay_entry = tk.Entry(total_frame, **entry_style)
pay_entry.grid(row=3, column=0, padx=5, pady=5, ipady=7)

tk.Label(total_frame, text="Change:", **label_style).grid(row=4, column=0, padx=5, pady=5, sticky='w')
change_entry = tk.Entry(total_frame, **entry_style)
change_entry.grid(row=5, column=0, padx=5, pady=5, ipady=7)
change_entry.config(state="readonly")

enter_button = tk.Button(total_frame, text="ENTER", command=calculate_change, font=("Arial", 10, "bold"))
enter_button.grid(row=6, column=0, padx=5, pady=10)

input_frame_main = tk.Frame(root)
input_frame_main.grid(row=3, column=0, padx=20, pady=5, sticky="sw")

tk.Label(input_frame_main, text="Product Name:", **label_style).grid(row=0, column=0, padx=5, pady=5, sticky='w')
product_name_entry_main = tk.Entry(input_frame_main, **entry_style_bold)
product_name_entry_main.grid(row=1, column=0, padx=5, pady=5, ipady=7)
product_name_entry_main.config(state="readonly")

tk.Label(input_frame_main, text="Quantity:", **label_style).grid(row=2, column=0, padx=5, pady=5, sticky='w')
quantity_entry_main = tk.Entry(input_frame_main, **entry_style)
quantity_entry_main.grid(row=3, column=0, padx=5, pady=5, ipady=7)

tk.Label(input_frame_main, text="Price:", **label_style).grid(row=4, column=0, padx=5, pady=5, sticky='w')
price_entry_main = tk.Entry(input_frame_main, **entry_style)
price_entry_main.grid(row=5, column=0, padx=5, pady=5, ipady=7)
price_entry_main.config(state="readonly")

buy_button = tk.Button(input_frame_main, text="BUY", command=buy_product, font=("Arial", 10, "bold"))
buy_button.grid(row=6, column=0, padx=5, pady=10)

button_frame_middle = tk.Frame(root)
button_frame_middle.grid(row=5, column=0, columnspan=2, pady=20)

button_style = {"font": ("Arial", 10, "bold"), "width": 15, "height": 2}

add_product_button = tk.Button(button_frame_middle, text="Add Product", command=add_product_window, **button_style)
add_product_button.pack(side=tk.LEFT, padx=5)

add_quantity_button = tk.Button(button_frame_middle, text="Add Quantity", command=add_quantity_window, **button_style)
add_quantity_button.pack(side=tk.LEFT, padx=5)

exit_button = tk.Button(button_frame_middle, text="Exit", command=exit_application, bg='red', fg='white',
                        **button_style)
exit_button.pack(side=tk.LEFT, padx=5)





root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

root.mainloop()
