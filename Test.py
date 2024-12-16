import random
import tkinter as tk
from tkinter import ttk, messagebox

class IncomeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Income Generator")
        self.root.geometry("600x800")
        
        # Style configuration
        style = ttk.Style()
        style.configure("TLabel", padding=5, font=('Arial', 10))
        style.configure("TButton", padding=5, font=('Arial', 10))
        style.configure("TEntry", padding=5)
        
        # Input Frame
        input_frame = ttk.Frame(root, padding="10")
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Total Days Input
        ttk.Label(input_frame, text="Enter Total Days:").pack(anchor=tk.W)
        self.days_entry = ttk.Entry(input_frame)
        self.days_entry.pack(fill=tk.X, pady=5)
        
        # Total Income Input
        ttk.Label(input_frame, text="Enter Total Income:").pack(anchor=tk.W)
        self.income_entry = ttk.Entry(input_frame)
        self.income_entry.pack(fill=tk.X, pady=5)
        
        # Generate Button
        ttk.Button(input_frame, text="Generate Daily Incomes", command=self.generate_income).pack(pady=10)
        
        # Results Frame
        results_frame = ttk.Frame(root, padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Results Text Area
        self.results_text = tk.Text(results_frame, height=30, width=50)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.configure(yscrollcommand=scrollbar.set)

    def generate_daily_incomes(self, total_days, target_total):
        # Calculate average daily income
        average = target_total / total_days
        
        if average < 2000 or average > 5000:
            return None  # Invalid average - outside possible range
            
        daily_incomes = []
        remaining_total = target_total
        remaining_days = total_days
        
        # Generate random numbers that sum to target_total
        for day in range(total_days - 1):
            # Calculate safe min and max for this day
            min_value = max(2000, remaining_total - (5000 * (remaining_days - 1)))
            max_value = min(5000, remaining_total - (2000 * (remaining_days - 1)))
            
            if min_value > max_value:
                return None  # Invalid distribution
            
            income = random.randint(int(min_value), int(max_value))
            daily_incomes.append(income)
            remaining_total -= income
            remaining_days -= 1
        
        # Add the last day
        if 2000 <= remaining_total <= 5000:
            daily_incomes.append(remaining_total)
            return daily_incomes
        return None

    def generate_income(self):
        try:
            total_days = int(self.days_entry.get())
            target_total = int(self.income_entry.get())
            
            if total_days <= 0:
                messagebox.showerror("Error", "Please enter a positive number of days")
                return
                
            if target_total <= 0:
                messagebox.showerror("Error", "Please enter a positive total income")
                return
            
            # Clear previous results
            self.results_text.delete(1.0, tk.END)
            
            # Generate daily incomes that sum to exact target
            daily_incomes = self.generate_daily_incomes(total_days, target_total)
            
            if daily_incomes is None:
                messagebox.showerror("Error", 
                    "Cannot distribute the total income across the given days while keeping daily income between 2000-5000. " +
                    "Try a different total income or number of days.")
                return
            
            # Display results
            self.results_text.insert(tk.END, f"Total days = {total_days}\n")
            self.results_text.insert(tk.END, f"Total income = {target_total:,}\n\n")
            self.results_text.insert(tk.END, "Daily Incomes:\n")
            
            for income in daily_incomes:
                self.results_text.insert(tk.END, f"{income:,}\n")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")

def main():
    root = tk.Tk()
    app = IncomeGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
