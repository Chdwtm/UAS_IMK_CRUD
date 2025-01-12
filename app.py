import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Koneksi ke database SQLite
conn = sqlite3.connect("mahasiswa.db")
cursor = conn.cursor()

# Membuat tabel jika belum ada
cursor.execute('''
CREATE TABLE IF NOT EXISTS mahasiswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    nim TEXT NOT NULL UNIQUE,
    program_studi TEXT NOT NULL,
    email TEXT NOT NULL
)
''')
conn.commit()

# Fungsi CRUD
def tambah_mahasiswa():
    nama = entry_nama.get()
    nim = entry_nim.get()
    program_studi = entry_program_studi.get()
    email = entry_email.get()

    if not (nama and nim and program_studi and email):
        messagebox.showwarning("Input Salah", "Semua kolom harus diisi!")
        return

    try:
        cursor.execute("INSERT INTO mahasiswa (nama, nim, program_studi, email) VALUES (?, ?, ?, ?)",
                       (nama, nim, program_studi, email))
        conn.commit()
        messagebox.showinfo("Sukses", "Data mahasiswa berhasil ditambahkan!")
        tampilkan_data()
        clear_entries()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "NIM sudah terdaftar!")

def tampilkan_data():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM mahasiswa")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def hapus_mahasiswa():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Pilih Data", "Pilih data yang ingin dihapus!")
        return

    confirm = messagebox.askyesno("Konfirmasi Hapus", "Apakah Anda yakin ingin menghapus data ini?")
    if not confirm:
        return

    data = tree.item(selected_item)
    mahasiswa_id = data['values'][0]

    cursor.execute("DELETE FROM mahasiswa WHERE id = ?", (mahasiswa_id,))
    conn.commit()
    messagebox.showinfo("Sukses", "Data mahasiswa berhasil dihapus!")
    tampilkan_data()

def update_mahasiswa():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Pilih Data", "Pilih data yang ingin diupdate!")
        return

    data = tree.item(selected_item)
    mahasiswa_id = data['values'][0]

    nama = entry_nama.get()
    nim = entry_nim.get()
    program_studi = entry_program_studi.get()
    email = entry_email.get()

    if not (nama and nim and program_studi and email):
        messagebox.showwarning("Input Salah", "Semua kolom harus diisi!")
        return

    cursor.execute("UPDATE mahasiswa SET nama = ?, nim = ?, program_studi = ?, email = ? WHERE id = ?",
                   (nama, nim, program_studi, email, mahasiswa_id))
    conn.commit()
    messagebox.showinfo("Sukses", "Data mahasiswa berhasil diperbarui!")
    tampilkan_data()
    clear_entries()

def lihat_detail_mahasiswa():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Pilih Data", "Pilih data yang ingin dilihat!")
        return

    data = tree.item(selected_item)
    detail = data['values']

    detail_message = f"ID: {detail[0]}\nNama: {detail[1]}\nNIM: {detail[2]}\nProgram Studi: {detail[3]}\nEmail: {detail[4]}"
    messagebox.showinfo("Detail Mahasiswa", detail_message)

def clear_entries():
    entry_nama.delete(0, tk.END)
    entry_nim.delete(0, tk.END)
    entry_program_studi.delete(0, tk.END)
    entry_email.delete(0, tk.END)

# GUI
root = tk.Tk()
root.title("Aplikasi CRUD Data Mahasiswa")
root.geometry("800x600")
root.configure(bg="#e0f7fa")

# Gaya global
style = ttk.Style()
style.configure("Treeview", font=("Arial", 10))
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
style.configure("TButton", font=("Arial", 10), padding=5)

# Header
header_frame = tk.Frame(root, bg="#00796b", pady=20)
header_frame.pack(fill="x")
header_label = tk.Label(header_frame, text="Manajemen Data Mahasiswa", bg="#00796b", fg="white", font=("Arial", 20, "bold"))
header_label.pack()

# Form Input
frame_input = tk.Frame(root, bg="#e0f7fa", padx=20, pady=20, relief="groove", bd=2)
frame_input.pack(pady=10, fill="x", padx=20)

labels = ["Nama Lengkap", "NIM", "Program Studi", "Email"]
entries = []

for i, label in enumerate(labels):
    tk.Label(frame_input, text=label, bg="#e0f7fa", font=("Arial", 12)).grid(row=i, column=0, sticky="w", pady=5)
    entry = tk.Entry(frame_input, font=("Arial", 12), width=30)
    entry.grid(row=i, column=1, pady=5, padx=10)
    entries.append(entry)

entry_nama, entry_nim, entry_program_studi, entry_email = entries

# Tombol
frame_buttons = tk.Frame(root, bg="#e0f7fa", pady=10)
frame_buttons.pack(fill="x", padx=20)

button_texts = ["Tambah", "Update", "Hapus", "Clear", "Lihat Detail"]
button_commands = [tambah_mahasiswa, update_mahasiswa, hapus_mahasiswa, clear_entries, lihat_detail_mahasiswa]

for i, (text, command) in enumerate(zip(button_texts, button_commands)):
    tk.Button(frame_buttons, text=text, command=command, bg="#004d40", fg="white", font=("Arial", 12), relief="flat", width=12).grid(row=0, column=i, padx=10, pady=5)

# Tabel
frame_table = tk.Frame(root, bg="#e0f7fa", pady=10)
frame_table.pack(fill="both", expand=True, padx=20, pady=10)

tree = ttk.Treeview(frame_table, columns=("ID", "Nama", "NIM", "Program Studi", "Email"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nama", text="Nama")
tree.heading("NIM", text="NIM")
tree.heading("Program Studi", text="Program Studi")
tree.heading("Email", text="Email")

tree.column("ID", width=50, anchor="center")
tree.column("Nama", width=150)
tree.column("NIM", width=100, anchor="center")
tree.column("Program Studi", width=120)
tree.column("Email", width=200)

tree.pack(fill="both", expand=True, padx=10, pady=10)

# Scrollbar
scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscroll=scrollbar.set)

# Load Data Awal
tampilkan_data()

root.mainloop()

# Tutup koneksi database saat aplikasi ditutup
conn.close()
