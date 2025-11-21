import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from simulation import FIFOHandler, LRUHandler, OptimalHandler, ClockHandler, LFUHandler
from visualization import plot_page_faults
 
class ModernPageSimGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PagePlay - Page Replacement Simulator")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1a1a2e')
        
        # Tema warna modern
        self.colors = {
            'bg_dark': '#1a1a2e',
            'bg_medium': '#16213e',
            'accent_primary': '#0f3460',
            'accent_glow': '#e94560',
            'text_main': '#eaeaea',
            'text_secondary': '#94a3b8',
            'success': '#4ade80',
            'warning': '#fb923c'
        }

        self.setup_styles()
        self.build_interface()
        self.simulation_count = 0

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('Modern.TFrame',
                           background=self.colors['bg_dark'])
        
        self.style.configure('Card.TFrame',
                           background=self.colors['bg_medium'],
                           relief='flat')
        
        self.style.configure('Primary.TButton',
                           background=self.colors['accent_glow'],
                           foreground='white',
                           borderwidth=0,
                           font=('Segoe UI', 11, 'bold'),
                           padding=12)
        self.style.map('Primary.TButton',
                     background=[('active', '#d63447')])
        
        self.style.configure('Secondary.TButton',
                           background=self.colors['accent_primary'],
                           foreground='white',
                           borderwidth=0,
                           font=('Segoe UI', 10),
                           padding=10)
        
        self.style.configure('Modern.TEntry',
                           fieldbackground=self.colors['bg_medium'],
                           foreground=self.colors['text_main'],
                           borderwidth=2,
                           relief='solid')
        
        self.style.configure('Title.TLabel',
                           font=('Segoe UI', 24, 'bold'),
                           foreground=self.colors['text_main'],
                           background=self.colors['bg_dark'])
        
        self.style.configure('Subtitle.TLabel',
                           font=('Segoe UI', 11),
                           foreground=self.colors['text_secondary'],
                           background=self.colors['bg_dark'])
        
        self.style.configure('Section.TLabel',
                           font=('Segoe UI', 12, 'bold'),
                           foreground=self.colors['text_main'],
                           background=self.colors['bg_medium'])

    def build_interface(self):
        # Container utama
        main_container = ttk.Frame(self.root, style='Modern.TFrame')
        main_container.pack(fill='both', expand=True, padx=25, pady=25)

        # Header Section
        self.create_header(main_container)
        
        # Input Configuration Card
        self.create_input_section(main_container)
        
        # Algorithm Selection Card
        self.create_algorithm_section(main_container)
        
        # Action Buttons
        self.create_action_buttons(main_container)
        
        # Progress Indicator
        self.create_progress_section(main_container)
        
        # Results Display
        self.create_results_section(main_container)

    def create_header(self, parent):
        header_frame = ttk.Frame(parent, style='Modern.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        title = ttk.Label(header_frame, 
                         text="PagePlay Simulator", 
                         style='Title.TLabel')
        title.pack(anchor='w')
        
        subtitle = ttk.Label(header_frame,
                           text="Analisis Algoritma Penggantian Halaman Memori",
                           style='Subtitle.TLabel')
        subtitle.pack(anchor='w')

    def create_input_section(self, parent):
        card = ttk.Frame(parent, style='Card.TFrame', padding=20)
        card.pack(fill='x', pady=(0, 15))
        
        ttk.Label(card, text="Konfigurasi Simulasi", 
                 style='Section.TLabel').grid(row=0, column=0, columnspan=4, sticky='w', pady=(0, 15))
        
        # Jumlah frame
        ttk.Label(card, text="Jumlah Frame:", 
                 foreground=self.colors['text_main'],
                 background=self.colors['bg_medium']).grid(row=1, column=0, sticky='w', padx=(0, 10))
        self.frame_entry = ttk.Entry(card, style='Modern.TEntry', width=15)
        self.frame_entry.grid(row=1, column=1, sticky='w', padx=(0, 20))
        self.frame_entry.insert(0, "3")
        
        # Page reference
        ttk.Label(card, text="Urutan Halaman:", 
                 foreground=self.colors['text_main'],
                 background=self.colors['bg_medium']).grid(row=1, column=2, sticky='w', padx=(0, 10))
        self.sequence_entry = ttk.Entry(card, style='Modern.TEntry', width=35)
        self.sequence_entry.grid(row=1, column=3, sticky='ew')
        self.sequence_entry.insert(0, "7,0,1,2,0,3,0,4,2,3,0,3,2")
        
        # Upload button
        upload_btn = ttk.Button(card, text="📂 Muat dari File", 
                              command=self.load_from_file, 
                              style='Secondary.TButton')
        upload_btn.grid(row=2, column=3, sticky='e', pady=(10, 0))

    def create_algorithm_section(self, parent):
        card = ttk.Frame(parent, style='Card.TFrame', padding=20)
        card.pack(fill='x', pady=(0, 15))
        
        ttk.Label(card, text="Pilih Algoritma", 
                 style='Section.TLabel').pack(anchor='w', pady=(0, 15))
        
        algo_container = ttk.Frame(card, style='Card.TFrame')
        algo_container.pack(fill='x')
        
        self.algorithm_vars = {}
        algorithms = [
            ('FIFO', 'First In First Out'),
            ('LRU', 'Least Recently Used'),
            ('OPTIMAL', 'Optimal Page Replacement')
        ]
        
        for i, (code, name) in enumerate(algorithms):
            var = tk.IntVar(value=1)
            self.algorithm_vars[code] = var
            
            cb = ttk.Checkbutton(algo_container, 
                               text=f"{code} - {name}",
                               variable=var)
            cb.grid(row=i//2, column=i%2, sticky='w', padx=10, pady=5)

    def create_action_buttons(self, parent):
        btn_frame = ttk.Frame(parent, style='Modern.TFrame')
        btn_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Button(btn_frame, text="▶ Jalankan Simulasi", 
                 command=self.execute_simulation, 
                 style='Primary.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(btn_frame, text="📊 Visualisasi", 
                 command=self.display_visualization, 
                 style='Secondary.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(btn_frame, text="💾 Ekspor Hasil", 
                 command=self.export_results, 
                 style='Secondary.TButton').pack(side='left')
        
        ttk.Button(btn_frame, text="🔄 Reset", 
                 command=self.reset_simulation, 
                 style='Secondary.TButton').pack(side='right')

    def create_progress_section(self, parent):
        self.progress_bar = ttk.Progressbar(parent,
                                          length=500,
                                          mode='determinate')
        self.progress_bar.pack(fill='x', pady=(0, 15))
        
        self.status_label = ttk.Label(parent,
                                    text="Siap untuk simulasi",
                                    foreground=self.colors['text_secondary'],
                                    background=self.colors['bg_dark'])
        self.status_label.pack(anchor='w')

    def create_results_section(self, parent):
        card = ttk.Frame(parent, style='Card.TFrame', padding=20)
        card.pack(fill='both', expand=True)
        
        ttk.Label(card, text="Hasil Simulasi", 
                 style='Section.TLabel').pack(anchor='w', pady=(0, 10))
        
        # Text widget dengan scrollbar
        text_container = ttk.Frame(card, style='Card.TFrame')
        text_container.pack(fill='both', expand=True)
        
        self.results_display = tk.Text(text_container,
                                      bg=self.colors['bg_dark'],
                                      fg=self.colors['text_main'],
                                      font=('Consolas', 10),
                                      wrap=tk.WORD,
                                      borderwidth=0,
                                      padx=10,
                                      pady=10)
        
        scrollbar = ttk.Scrollbar(text_container, command=self.results_display.yview)
        self.results_display.configure(yscrollcommand=scrollbar.set)
        
        self.results_display.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Welcome message
        self.results_display.insert('1.0', 
            "╔═══════════════════════════════════════════════════╗\n"
            "  Selamat datang di PagePlay Simulator\n"
            "╚═══════════════════════════════════════════════════╝\n\n"
            "Petunjuk:\n"
            "1. Masukkan jumlah frame memori\n"
            "2. Masukkan urutan referensi halaman (pisahkan dengan koma)\n"
            "3. Pilih algoritma yang ingin disimulasikan\n"
            "4. Klik 'Jalankan Simulasi'\n\n"
            "Siap untuk memulai! 🚀\n")
        self.results_display.config(state='disabled')

    def load_from_file(self):
        try:
            filepath = filedialog.askopenfilename(
                title="Pilih File Data",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if filepath:
                with open(filepath, 'r') as file:
                    data = file.read().strip()
                    self.sequence_entry.delete(0, tk.END)
                    self.sequence_entry.insert(0, data)
                    self.update_status(f"✓ Data dimuat dari: {filepath}", 'success')
        except Exception as error:
            messagebox.showerror("Error", f"Gagal memuat file:\n{str(error)}")

    def execute_simulation(self):
        try:
            # Validasi input
            num_frames = int(self.frame_entry.get())
            if num_frames <= 0:
                raise ValueError("Jumlah frame harus lebih dari 0")
            
            page_sequence = [int(x.strip()) for x in self.sequence_entry.get().split(',')]
            
            if not page_sequence:
                raise ValueError("Urutan halaman tidak boleh kosong")
            
            # Cek algoritma yang dipilih
            selected_algorithms = []
            if self.algorithm_vars['FIFO'].get(): 
                selected_algorithms.append(('FIFO', FIFOHandler(num_frames)))
            if self.algorithm_vars['LRU'].get(): 
                selected_algorithms.append(('LRU', LRUHandler(num_frames)))
            if self.algorithm_vars['OPTIMAL'].get(): 
                selected_algorithms.append(('OPTIMAL', OptimalHandler(num_frames, page_sequence)))
            
            if not selected_algorithms:
                messagebox.showwarning("Peringatan", "Pilih minimal satu algoritma!")
                return
            
            # Jalankan simulasi
            self.progress_bar['value'] = 0
            self.update_status("⏳ Memproses simulasi...", 'warning')
            
            total_pages = len(page_sequence)
            self.simulation_results = {}
            self.fault_progression = {}
            
            for idx, page in enumerate(page_sequence):
                for algo_name, handler in selected_algorithms:
                    fault_count, memory_state = handler.step(page)
                    self.fault_progression.setdefault(algo_name, []).append(fault_count)
                
                self.progress_bar['value'] = ((idx + 1) / total_pages) * 100
                self.root.update_idletasks()
            
            # Simpan hasil
            for algo_name, handler in selected_algorithms:
                self.simulation_results[algo_name] = handler.page_faults
            
            self.simulation_count += 1
            self.show_results()
            self.update_status("✓ Simulasi selesai!", 'success')
            
        except ValueError as ve:
            messagebox.showerror("Input Error", f"Format input salah:\n{str(ve)}")
            self.update_status("✗ Simulasi gagal - input tidak valid", 'warning')
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan:\n{str(e)}")
            self.update_status("✗ Simulasi gagal", 'warning')

    def show_results(self):
        self.results_display.config(state='normal')
        self.results_display.delete('1.0', tk.END)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        output = f"╔═══════════════════════════════════════════════════╗\n"
        output += f"  HASIL SIMULASI #{self.simulation_count}\n"
        output += f"  {timestamp}\n"
        output += f"╚═══════════════════════════════════════════════════╝\n\n"
        
        output += f"Konfigurasi:\n"
        output += f"  • Jumlah Frame: {self.frame_entry.get()}\n"
        output += f"  • Panjang Urutan: {len(self.sequence_entry.get().split(','))} halaman\n"
        output += f"  • Urutan: {self.sequence_entry.get()}\n\n"
        
        output += f"Hasil Page Fault:\n"
        output += f"─────────────────────────────────────────────────\n"
        
        sorted_results = sorted(self.simulation_results.items(), key=lambda x: x[1])
        
        for algo_name, fault_count in sorted_results:
            bar_length = int((fault_count / max(self.simulation_results.values())) * 30)
            bar = "█" * bar_length
            output += f"  {algo_name:10} : {fault_count:3} faults {bar}\n"
        
        output += f"\n─────────────────────────────────────────────────\n"
        
        # Hitung total hits untuk setiap algoritma
        total_hits = {}
        total_references = len(self.sequence_entry.get().split(','))
        
        for algo_name in self.simulation_results.keys():
            y = self.fault_progression[algo_name]
            hit_count = 0
            for j in range(1, len(y)):
                if y[j] == y[j-1]:  # Tidak ada increment = HIT
                    hit_count += 1
            total_hits[algo_name] = hit_count
        
        # Kesimpulan
        best_algo = sorted_results[0]
        worst_algo = sorted_results[-1]
        
        output += f"\n╔═══════════════════════════════════════════════════╗\n"
        output += f"  📊 KESIMPULAN ANALISIS\n"
        output += f"╚═══════════════════════════════════════════════════╝\n\n"
        
        output += f"🏆 Algoritma Paling Optimal: {best_algo[0]}\n"
        output += f"   • Page Faults: {best_algo[1]} dari {total_references} referensi\n"
        output += f"   • Page Hits: {total_hits[best_algo[0]]} ({(total_hits[best_algo[0]]/total_references*100):.1f}%)\n"
        output += f"   • Hit Ratio: {(total_hits[best_algo[0]]/total_references*100):.1f}%\n\n"
        
        # Perbandingan dengan semua algoritma lainnya
        if len(sorted_results) > 1:
            output += f"📈 Perbandingan dengan Algoritma Lainnya:\n"
            
            for algo_name, fault_count in sorted_results:
                if algo_name != best_algo[0]:
                    fault_diff = fault_count - best_algo[1]
                    if fault_count > 0:
                        efficiency = ((fault_count - best_algo[1]) / fault_count) * 100
                    else:
                        efficiency = 0
                    
                    output += f"   • {algo_name}:\n"
                    output += f"     - Selisih Faults: +{fault_diff} (lebih banyak {fault_diff} page fault)\n"
                    output += f"     - Efisiensi {best_algo[0]}: {efficiency:.1f}% lebih baik dari {algo_name}\n"
        
        output += f"\n╚═══════════════════════════════════════════════════╝\n"
        
        self.results_display.insert('1.0', output)
        self.results_display.config(state='disabled')

    def display_visualization(self):
        if hasattr(self, 'simulation_results') and self.simulation_results:
            plot_page_faults(
                list(self.simulation_results.keys()),
                list(self.simulation_results.values()),
                self.fault_progression
            )
        else:
            messagebox.showinfo("Info", "Jalankan simulasi terlebih dahulu untuk melihat visualisasi")

    def export_results(self):
        try:
            if not hasattr(self, 'simulation_results') or not self.simulation_results:
                messagebox.showinfo("Info", "Tidak ada hasil untuk diekspor")
                return
            
            filepath = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
                title="Simpan Hasil Simulasi"
            )
            
            if filepath:
                with open(filepath, 'w', encoding='utf-8') as file:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    file.write("=" * 70 + "\n")
                    file.write("  LAPORAN SIMULASI PENGGANTIAN HALAMAN MEMORI\n")
                    file.write("  PagePlay Simulator\n")
                    file.write(f"  Tanggal: {timestamp}\n")
                    file.write("=" * 70 + "\n\n")
                    
                    file.write("KONFIGURASI SIMULASI:\n")
                    file.write(f"  Jumlah Frame      : {self.frame_entry.get()}\n")
                    file.write(f"  Urutan Halaman    : {self.sequence_entry.get()}\n")
                    file.write(f"  Panjang Urutan    : {len(self.sequence_entry.get().split(','))}\n\n")
                    
                    file.write("HASIL SIMULASI:\n")
                    file.write("-" * 70 + "\n")
                    
                    sorted_results = sorted(self.simulation_results.items(), key=lambda x: x[1])
                    
                    for algo, faults in sorted_results:
                        file.write(f"  {algo:12} : {faults} page faults\n")
                    
                    file.write("\n" + "-" * 70 + "\n")
                    
                    # Hitung total hits untuk setiap algoritma
                    total_hits = {}
                    total_references = len(self.sequence_entry.get().split(','))
                    
                    for algo_name in self.simulation_results.keys():
                        y = self.fault_progression[algo_name]
                        hit_count = 0
                        for j in range(1, len(y)):
                            if y[j] == y[j-1]:  # Tidak ada increment = HIT
                                hit_count += 1
                        total_hits[algo_name] = hit_count
                    
                    # Tambahkan Kesimpulan
                    best_algo = sorted_results[0]
                    
                    file.write("\n" + "=" * 70 + "\n")
                    file.write("  KESIMPULAN ANALISIS\n")
                    file.write("=" * 70 + "\n\n")
                    
                    file.write(f"Algoritma Paling Optimal: {best_algo[0]}\n")
                    file.write(f"  - Page Faults: {best_algo[1]} dari {total_references} referensi\n")
                    file.write(f"  - Page Hits: {total_hits[best_algo[0]]} ({(total_hits[best_algo[0]]/total_references*100):.1f}%)\n")
                    file.write(f"  - Hit Ratio: {(total_hits[best_algo[0]]/total_references*100):.1f}%\n\n")
                    
                    # Perbandingan dengan semua algoritma lainnya
                    if len(sorted_results) > 1:
                        file.write("Perbandingan dengan Algoritma Lainnya:\n\n")
                        
                        for algo_name, fault_count in sorted_results:
                            if algo_name != best_algo[0]:
                                fault_diff = fault_count - best_algo[1]
                                if fault_count > 0:
                                    efficiency = ((fault_count - best_algo[1]) / fault_count) * 100
                                else:
                                    efficiency = 0
                                
                                file.write(f"  {algo_name}:\n")
                                file.write(f"    - Page Faults: {fault_count}\n")
                                file.write(f"    - Page Hits: {total_hits[algo_name]} ({(total_hits[algo_name]/total_references*100):.1f}%)\n")
                                file.write(f"    - Selisih Faults: +{fault_diff} (lebih banyak {fault_diff} page fault)\n")
                                file.write(f"    - Efisiensi {best_algo[0]}: {efficiency:.1f}% lebih baik dari {algo_name}\n\n")
                    
                    file.write("=" * 70 + "\n")
                    file.write("  END OF REPORT\n")
                    file.write("=" * 70 + "\n")
                
                self.update_status(f"✓ Hasil diekspor ke: {filepath}", 'success')
                
        except Exception as error:
            messagebox.showerror("Error", f"Gagal menyimpan file:\n{str(error)}")

    def reset_simulation(self):
        self.frame_entry.delete(0, tk.END)
        self.frame_entry.insert(0, "3")
        self.sequence_entry.delete(0, tk.END)
        self.sequence_entry.insert(0, "7,0,1,2,0,3,0,4,2,3,0,3,2")
        self.progress_bar['value'] = 0
        
        for var in self.algorithm_vars.values():
            var.set(1)
        
        self.results_display.config(state='normal')
        self.results_display.delete('1.0', tk.END)
        self.results_display.insert('1.0',
            "╔═══════════════════════════════════════════════════╗\n"
            "  Simulasi telah di-reset\n"
            "╚═══════════════════════════════════════════════════╝\n\n"
            "Konfigurasi dikembalikan ke default.\n"
            "Siap untuk simulasi baru! 🔄\n")
        self.results_display.config(state='disabled')
        
        self.update_status("Siap untuk simulasi baru", 'success')
        
        if hasattr(self, 'simulation_results'):
            delattr(self, 'simulation_results')
        if hasattr(self, 'fault_progression'):
            delattr(self, 'fault_progression')

    def update_status(self, message, status_type='normal'):
        color_map = {
            'success': self.colors['success'],
            'warning': self.colors['warning'],
            'normal': self.colors['text_secondary']
        }
        self.status_label.config(
            text=message,
            foreground=color_map.get(status_type, self.colors['text_secondary'])
        )