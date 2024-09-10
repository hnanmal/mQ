import tkinter as tk


# Function to perform the calculation
def calculate():
    try:
        # Get the input values
        num1 = float(entry1.get())
        num2 = float(entry2.get())

        # Check which operation is selected and calculate accordingly
        if operation.get() == "sum":
            result = num1**2 + num2**2
        else:  # operation == "difference"
            result = num1**2 - num2**2

        # Display the result
        result_label.config(text=f"Result: {result}")
    except ValueError:
        result_label.config(text="Please enter valid numbers!")


# Create the main application window
root = tk.Tk()
root.title("Sum or Difference of Squares Calculator")

# Create the input fields and labels
label1 = tk.Label(root, text="Enter first number:")
label1.pack()

entry1 = tk.Entry(root)
entry1.pack()

label2 = tk.Label(root, text="Enter second number:")
label2.pack()

entry2 = tk.Entry(root)
entry2.pack()

# Create radio buttons for selecting the operation (Sum or Difference)
operation = tk.StringVar(value="sum")  # Default operation is sum

sum_radio = tk.Radiobutton(root, text="Sum of squares", variable=operation, value="sum")
sum_radio.pack()

difference_radio = tk.Radiobutton(
    root, text="Difference of squares", variable=operation, value="difference"
)
difference_radio.pack()

# Create a button to trigger the calculation
calculate_button = tk.Button(root, text="Calculate", command=calculate)
calculate_button.pack()

# Create a label to display the result
result_label = tk.Label(root, text="Result:")
result_label.pack()

# Start the Tkinter event loop
root.mainloop()
