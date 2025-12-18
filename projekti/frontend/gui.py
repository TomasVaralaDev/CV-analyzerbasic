import tkinter as tk
from tkinter import ttk, messagebox
import requests
from styles import apply_dark_theme, apply_light_theme

class CVAnalyzerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("CV Analysoija")
        self.master.state('zoomed')  # Koko näyttö

        # Tyylit
        self.style = ttk.Style()
        self.is_dark_mode = True  # Aloitetaan tummalla teemalla
        self.apply_theme()

        # Pääkehys
        frame = ttk.Frame(self.master, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure((0, 1), weight=1)
        frame.rowconfigure(1, weight=1)

        # CV
        ttk.Label(frame, text="📄 CV").grid(row=0, column=0, sticky='w', pady=(0, 5))
        self.cv_entry = tk.Text(frame, wrap=tk.WORD, font=('Arial', 11), relief=tk.FLAT)
        self.cv_entry.insert('1.0', 'Liitä CV tähän...')
        self.cv_entry.grid(row=1, column=0, sticky='nsew', padx=(0, 10), pady=(0, 10))

        # Työpaikkailmoitus
        ttk.Label(frame, text="💼 Työpaikkailmoitus").grid(row=0, column=1, sticky='w', pady=(0, 5))
        self.job_entry = tk.Text(frame, wrap=tk.WORD, font=('Arial', 11), relief=tk.FLAT)
        self.job_entry.insert('1.0', 'Liitä työpaikkailmoitus tähän...')
        self.job_entry.grid(row=1, column=1, sticky='nsew', padx=(10, 0), pady=(0, 10))

        # Analysoi-painike
        analyze_btn = ttk.Button(frame, text="🔍 Analysoi", command=self.analyze)
        analyze_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Vaihda teema -nappi
        toggle_theme_btn = ttk.Button(frame, text="🔲 Vaihda teema", command=self.toggle_theme)
        toggle_theme_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # Tulosalue kehys + scrollbar
        result_frame = ttk.Frame(self.master)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        result_frame.rowconfigure(0, weight=1)
        result_frame.columnconfigure(0, weight=1)

        self.output = tk.Text(result_frame, wrap=tk.WORD, font=('Courier', 11), relief=tk.FLAT)
        self.output.config(state=tk.DISABLED)
        self.output.grid(row=0, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(result_frame, orient='vertical', command=self.output.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.output['yscrollcommand'] = scrollbar.set

    def apply_theme(self):
        """Vaihtaa teeman (tumman/vaalean)."""
        if self.is_dark_mode:
            apply_dark_theme(self.style)
        else:
            apply_light_theme(self.style)

    def toggle_theme(self):
        """Vaihda teemaa."""
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def analyze(self):
        cv = self.cv_entry.get('1.0', tk.END).strip()
        job = self.job_entry.get('1.0', tk.END).strip()
        if not cv or not job:
            messagebox.showerror('Virhe', 'Täytä molemmat kentät.')
            return
        try:
            resp = requests.post('http://127.0.0.1:5000/analyze', json={'cv': cv, 'job': job})
            data = resp.json()
            text = (
                f"📄 Sanamäärä: {data['word_count']}\n\n"
                f"🔑 Avainsanat (CV): {', '.join(data['cv_keywords'])}\n"
                f"📌 Avainsanat (Työpaikka): {', '.join(data['job_keywords'])}\n\n"
                f"🧠 Sentimentti: {data['sentiment']}\n"
                f"✅ Vastaavuus: {data['match']} %"
            )
            self.output.config(state=tk.NORMAL)
            self.output.delete('1.0', tk.END)
            self.output.insert(tk.END, text)
            self.output.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror('Virhe', f'Yhteys epäonnistui: {e}')

if __name__ == '__main__':
    root = tk.Tk()
    app = CVAnalyzerApp(root)
    root.mainloop()
