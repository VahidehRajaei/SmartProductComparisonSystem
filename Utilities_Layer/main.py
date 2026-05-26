import tkinter as tk
from tkinter import ttk
import threading
import os
import sys

# Set path to identify other layers: DAL,PL
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DAL.scraper import PriceScraper
from PL.processor import DataProcessor

class ProfessionalComparator:
    def __init__(self, root):
        self.root = root
        self.root.title("Fiyat Karşılaştırıcı")
        self.root.iconbitmap('UL/icon/ecommerce_store_icon.ico')
        self.root.geometry("950x500")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.scraper = PriceScraper()
        self.processor = DataProcessor()

        # --- Designing UI ---
        header = tk.Frame(root, bg="#2c3e50", pady=20)
        header.pack(fill="x")
        tk.Label(header, text="Enter the product name", bg="#2c3e50", fg="white", font=("Tahoma", 11)).pack()
        self.search_entry = tk.Entry(header, width=40, font=("Tahoma", 12))
        self.search_entry.pack(pady=10)
        self.btn_search = tk.Button(header, text="Start searching and comparing products", command=self.start_thread, 
                                   bg="#27ae60", fg="white", font=("Tahoma", 10, "bold"), width=40)
        self.btn_search.pack()

        self.result_box = tk.Label(root, text="Preparing to receive information...", font=("Tahoma", 10, "bold"), pady=10)
        self.result_box.pack()

        self.tree = ttk.Treeview(root, columns=("Store", "Name", "Price"), show='headings')
        self.tree.heading("Store", text="Store")
        self.tree.heading("Name", text="Product name")
        self.tree.heading("Price", text="Price")
        self.tree.column("Store", width=100)
        self.tree.column("Name", width=600)
        self.tree.column("Price", width=150, anchor="center")
        self.tree.pack(padx=20, pady=10, fill="both", expand=True)

        self.status_bar = tk.Label(root, text="Status: Ready", bd=1, relief="sunken", anchor="w", font=("Tahoma", 9))
        self.status_bar.pack(side="bottom", fill="x")

    def on_closing(self):
        os._exit(0)

    def display_form(self):
        self.root.deiconify()
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after(10, lambda: self.root.attributes("-topmost", False))
        self.root.focus_force()

    def start_thread(self):
        query = self.search_entry.get()
        if not query: return
        self.btn_search.config(state="disabled")
        self.status_bar.config(text="Status: Extracting data...", fg="blue")
        for i in self.tree.get_children(): self.tree.delete(i)
        threading.Thread(target=self.etl_steps, args=(query,), daemon=True).start()

    def etl_steps(self, query):
        try:
            # 1. Extract
            data_t = self.scraper.fetch_trendyol(query)
            data_h = self.scraper.fetch_hepsiburada(query)
            
            # 2. Transform
            processed_list = self.processor.prepare_final_list(data_t + data_h)

            # 3. Load (UI Update)
            self.root.after(0, self.finish_search, processed_list)

        except Exception as e:
            print(f"ETL Error: {e}")
        finally:
            self.root.after(0, self.display_form)
            self.root.after(0, lambda: self.btn_search.config(state="normal"))
            self.root.after(0, lambda: self.status_bar.config(text="Status: Search completed.", fg="#27ae60"))

    def finish_search(self, final_list):
        if not final_list:
            self.result_box.config(text="No items found.", fg="red")
            return
        for item in final_list:
            self.tree.insert("", "end", values=(item[0], item[1], item[2] + " TL"))
        best = final_list[0]
        self.result_box.config(text=f"The cheapest item according to the search: {best[2]} TL in {best[0]}", fg="#27ae60")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProfessionalComparator(root)
    root.mainloop()