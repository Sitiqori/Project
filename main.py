import tkinter as tk
from gui import ModernPageSimGUI
import sys

def main():
    """
    Entry point untuk PagePlay Simulator
    Aplikasi untuk simulasi algoritma penggantian halaman memori
    """
    try:
        root = tk.Tk()
        root.resizable(True, True)
        root.minsize(900, 650)
        
        # Inisialisasi aplikasi
        app = ModernPageSimGUI(root)
        
        # Jalankan aplikasi
        root.mainloop()
        
    except Exception as e:
        print(f"Error saat menjalankan aplikasi: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()