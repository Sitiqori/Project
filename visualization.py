import matplotlib
matplotlib.use("TkAgg")  # pastikan backend GUI sesuai untuk Tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

# === Patch Toolbar ===
# Hapus semua tool kecuali Save (💾)
NavigationToolbar2Tk.toolitems = [t for t in NavigationToolbar2Tk.toolitems if t[0] == 'Save']

def plot_page_faults(algorithms, faults, states):
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('#0a0a0a')
    
    colors = ['#FFDCDC', '#91C8E4', '#80D8C3']

    # === Grafik Bar (Total Page Faults) ===
    ax1.bar(algorithms, faults, color=colors[:len(algorithms)])
    ax1.set_title('Total Page Faults', color='white', fontweight='bold')
    ax1.set_ylabel('Jumlah Fault', color='white')
    ax1.tick_params(colors='white')
    ax1.grid(alpha=0.3, linestyle='--')

    # === Grafik Bar (Total Page Hits) ===
    total_hits = []
    for algo in algorithms:
        y = states[algo]  # Kumulatif faults
        hit_count = 0
        for j in range(1, len(y)):
            if y[j] == y[j-1]:  # Tidak ada kenaikan fault berarti hit
                hit_count += 1
        total_hits.append(hit_count)
    
    ax2.bar(algorithms, total_hits, color=colors[:len(algorithms)])
    ax2.set_title('Total Page Hits', color='white', fontweight='bold')
    ax2.set_ylabel('Jumlah Hit', color='white')
    ax2.tick_params(colors='white')
    ax2.grid(alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.show()