import tkinter as tk
from tkinter import messagebox

#List to store booking records
bookings = []

#Function to create a new booking
def create_booking():
    movie_choice = movie_var.get()
    if movie_choice == 1:
        movie_name = "Mufasa: The Lion King"
        ticket_price = 4.90
    elif movie_choice == 2:
        movie_name = "Babah"
        ticket_price = 4.50
    elif movie_choice == 3:
        movie_name = "Seventeen Right Here [Live Viewing]"
        ticket_price = 33.00
    elif movie_choice == 4:
        movie_name = "Wicked"
        ticket_price = 3.00
    elif movie_choice == 5:
        movie_name = "Weathering With You"
        ticket_price = 4.00
    elif movie_choice == 6:
        movie_name = "The Gangster, The Cop, The Devil"
        ticket_price = 6.50
    else:
        messagebox.showerror("Error", "Invalid movie choice!")
        return

    tickets = int(ticket_entry.get())
    merchandise_total = 0
    if movie_choice == 5 and merchandise_var.get() == "yes":
        merch_quantity = int(merchandise_quantity_entry.get())
        merchandise_total = merch_quantity * 7.00

    total_price = (tickets * ticket_price) + merchandise_total
    booking = {
        "movie": movie_name,
        "tickets": tickets,
        "merchandise_total": merchandise_total,
        "total_price": total_price
    }
    bookings.append(booking)
    messagebox.showinfo("Success", f"Booking created successfully! Total price: ${total_price:.2f}")
    reset_fields()

#Function to view all bookings
def view_bookings():
    view_window = tk.Toplevel(root)
    view_window.title("View All Bookings")
    for idx, booking in enumerate(bookings):
        booking_info = f"Booking {idx + 1}:\n"
        booking_info += f"Movie: {booking['movie']}\n"
        booking_info += f"Tickets: {booking['tickets']}\n"
        booking_info += f"Merchandise Total: ${booking['merchandise_total']:.2f}\n"
        booking_info += f"Total Price: ${booking['total_price']:.2f}\n"
        tk.Label(view_window, text=booking_info).pack(padx=10, pady=5)

#Function to update an existing booking
def update_booking():
    # Display all bookings first
    if not bookings:
        messagebox.showwarning("No Bookings", "No bookings available to update.")
        return

    update_window = tk.Toplevel(root)
    update_window.title("Update Booking")

    #Prompt user to select the booking number to update
    tk.Label(update_window, text="Enter Booking Number to Update:").pack(padx=10, pady=5)
    booking_index_entry = tk.Entry(update_window)
    booking_index_entry.pack(padx=10, pady=5)

    #Function to apply updates
    def apply_update():
        try:
            booking_index = int(booking_index_entry.get()) - 1
            if 0 <= booking_index < len(bookings):
                booking = bookings[booking_index]

                #Create input fields for new ticket and merchandise updates
                tk.Label(update_window, text=f"Updating '{booking['movie']}'").pack(pady=5)

                tk.Label(update_window, text="Enter new number of tickets:").pack(padx=10, pady=5)
                new_tickets_entry = tk.Entry(update_window)
                new_tickets_entry.insert(0, booking['tickets'])
                new_tickets_entry.pack(padx=10, pady=5)

                if booking['movie'] == "Weathering With You":
                    tk.Label(update_window, text="Enter new number of merchandise:").pack(padx=10, pady=5)
                    new_merch_entry = tk.Entry(update_window)
                    new_merch_entry.insert(0, int(booking['merchandise_total'] / 5))
                    new_merch_entry.pack(padx=10, pady=5)

                def save_update():
                    #Save updated tickets
                    booking['tickets'] = int(new_tickets_entry.get())

                    #Save updated merchandise (if applicable)
                    if booking['movie'] == "Weathering With You":
                        merch_quantity = int(new_merch_entry.get())
                        booking['merchandise_total'] = merch_quantity * 7.00

                    #Recalculate total price
                    ticket_price = 4.00 if booking['movie'] == "Weathering With You" else 0
                    booking['total_price'] = (booking['tickets'] * ticket_price) + booking['merchandise_total']

                    messagebox.showinfo("Success", "Booking updated successfully!")
                    update_window.destroy()

                tk.Button(update_window, text="Save Updates", command=save_update).pack(pady=10)

            else:
                messagebox.showerror("Error", "Invalid booking number.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid booking number.")

    #Button to confirm booking to update
    tk.Button(update_window, text="Confirm Booking Number", command=apply_update).pack(padx=10, pady=10)

#Function to delete a booking
def delete_booking():
    if not bookings:
        messagebox.showwarning("No Bookings", "No bookings available to delete.")
        return
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Booking")
    booking_index_label = tk.Label(delete_window, text="Enter booking number to delete:")
    booking_index_label.pack(padx=10, pady=5)
    booking_index_entry = tk.Entry(delete_window)
    booking_index_entry.pack(padx=10, pady=5)

    def apply_delete():
        try:
            booking_index = int(booking_index_entry.get()) - 1
            if booking_index < 0 or booking_index >= len(bookings):
                raise IndexError
            deleted_booking = bookings.pop(booking_index)
            messagebox.showinfo("Success", f"Booking for '{deleted_booking['movie']}' deleted successfully!")
            delete_window.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid booking number.")
        except IndexError:
            messagebox.showerror("Booking Not Found", "The specified booking number does not exist.")

    delete_button = tk.Button(delete_window, text="Delete Booking", command=apply_delete)
    delete_button.pack(padx=10, pady=10)

#Function to reset fields
def reset_fields():
    ticket_entry.delete(0, tk.END)
    merchandise_quantity_entry.delete(0, tk.END)

#Set up main window
root = tk.Tk()
root.title("Movie Ticket Booking System")

#Movie selection
movie_var = tk.IntVar(value=1)
movie_label = tk.Label(root, text="Select Movie:")
movie_label.pack(padx=10, pady=5)
movie_options = [
    "Mufasa: The Lion King", "Babah", "Seventeen Right Here [Live Viewing]",
    "Wicked", "Weathering With You", "The Gangster, The Cop, The Devil"
]
for idx, movie in enumerate(movie_options, start=1):
    tk.Radiobutton(root, text=movie, variable=movie_var, value=idx).pack(padx=10, pady=2)

#Ticket input
ticket_label = tk.Label(root, text="Number of Tickets:")
ticket_label.pack(padx=10, pady=5)
ticket_entry = tk.Entry(root)
ticket_entry.pack(padx=10, pady=5)

#Merchandise option
merchandise_label = tk.Label(root, text="Would you like to buy merchandise? (only for 'Weathering With You'):")
merchandise_label.pack(padx=10, pady=5)
merchandise_var = tk.StringVar(value="no")
tk.Radiobutton(root, text="Yes", variable=merchandise_var, value="yes").pack(padx=10, pady=2)
tk.Radiobutton(root, text="No", variable=merchandise_var, value="no").pack(padx=10, pady=2)

#Merchandise quantity
merchandise_quantity_label = tk.Label(root, text="How many merchandise? (only for 'Weathering With You'):")
merchandise_quantity_label.pack(padx=10, pady=5)
merchandise_quantity_entry = tk.Entry(root)
merchandise_quantity_entry.pack(padx=10, pady=5)

#Buttons for actions
create_button = tk.Button(root, text="Create Booking", command=create_booking)
create_button.pack(padx=10, pady=10)

view_button = tk.Button(root, text="View Bookings", command=view_bookings)
view_button.pack(padx=10, pady=5)

update_button = tk.Button(root, text="Update Booking", command=update_booking)
update_button.pack(padx=10, pady=5)

delete_button = tk.Button(root, text="Delete Booking", command=delete_booking)
delete_button.pack(padx=10, pady=5)

#Run the Tkinter event loop
root.mainloop()