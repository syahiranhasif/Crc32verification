import os
import binascii
import customtkinter as ctk
from tkinter import filedialog, messagebox, StringVar, Menu
from tkinterdnd2 import TkinterDnD, DND_FILES
import urllib.request

# ========== CONFIG ==========
CURRENT_VERSION = "v1.4.3"
UPDATE_CHECK_URL = "https://raw.githubusercontent.com/syahiranhasif/CRC32-Hash/refs/heads/main/CRC32%20Hash/version.txt"

# CRC32 presets
known_crc32s = {
    "(OMNIA_LV/PHOENIX": "BA1DED31",
    "(ENTRY/LV" : "6477BBA7",
    "(BASIC/LV" : "932EA465",
    "(RITA MAIN/LV" : "701F0D7B",
    "(RITA UI/CHINA_STM32" : "BC120FC"
}

# ========== Appearance ==========
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ========== Base Window ==========
base = TkinterDnD.Tk()
app = ctk.CTkToplevel(base)
base.withdraw()

selected_crc = StringVar(master=app, value="")


# =========================================================
# CRC32 FUNCTIONS
# =========================================================
def get_crc32(filepath):
    try:
        with open(filepath, 'rb') as f:
            crc = binascii.crc32(f.read()) & 0xFFFFFFFF
            return f"{crc:08X}"
    except Exception as e:
        return f"Error: {e}"


def check_file(filepath):
    if not os.path.isfile(filepath):
        return

    result_crc = get_crc32(filepath)
    expected_crc = known_crc32s.get(selected_crc.get())

    status = "✅ MATCH" if result_crc == expected_crc else "❌ MISMATCH"

    textbox.configure(state="normal")
    textbox.delete("0.0", "end")
    textbox.insert(
        "0.0",
        f"📁 File: {filepath}\n\n"
        f"🔑 CRC32: {result_crc}\n"
        f"🎯 Expected: {expected_crc}\n\n"
        f"📊 Result: {status}"
    )
    textbox.configure(state="disabled")


def browse_and_check():
    filepath = filedialog.askopenfilename()
    if filepath:
        check_file(filepath)


def on_drop(event):
    filepath = event.data.strip().strip("{}")
    check_file(filepath)


def toggle_theme():
    if theme_switch.get():
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")


# =========================================================
# MENU FUNCTIONS
# =========================================================
def check_for_updates():
    try:
        response = urllib.request.urlopen(UPDATE_CHECK_URL)
        latest_version = response.read().decode("utf-8").strip()

        if latest_version != CURRENT_VERSION:
            messagebox.showinfo(
                "Update Available",
                f"A new version is available: {latest_version}\nYou're using: {CURRENT_VERSION}"
            )
        else:
            messagebox.showinfo("Up to Date", f"You are running the latest version ({CURRENT_VERSION}).")

    except Exception as e:
        messagebox.showerror("Update Check Failed", f"Unable to check for updates.\nError: {e}")


def show_about():
    messagebox.showinfo("About", f"CRC32 Checker {CURRENT_VERSION}\nDeveloped by syhiranhasf")


def exit_app():
    app.destroy()
    base.quit()


# =========================================================
# UI LAYOUT
# =========================================================
app.title("🔍 CRC32 Checker")
app.geometry("620x540")
app.resizable(False, False)

app.drop_target_register(DND_FILES)
app.dnd_bind("<<Drop>>", on_drop)


# ---------- Top-right menu ----------
menu_btn = ctk.CTkButton(
    app,
    text="⋮",
    width=25,
    height=25,
    fg_color="transparent",
    hover_color="#d0d0d0",
    text_color="#333333",
    corner_radius=0,
    font=ctk.CTkFont(size=18)
)
menu_btn.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

popup_menu = Menu(app, tearoff=0)
popup_menu.add_command(label="🔄 Check for Updates", command=check_for_updates)
popup_menu.add_command(label="ℹ️ About", command=show_about)
popup_menu.add_separator()
popup_menu.add_command(label="❌ Exit", command=exit_app)


def show_popup(event):
    popup_menu.tk_popup(event.x_root, event.y_root)


menu_btn.bind("<Button-1>", show_popup)


# ---------- Title ----------
title_label = ctk.CTkLabel(
    app,
    text="📁 Drag or Browse File to Check CRC32",
    font=ctk.CTkFont(size=16, weight="bold")
)
title_label.pack(pady=(40, 10))


# =========================================================
# ⭐ SIDE-BY-SIDE RADIO PRESETS (FIXED PART)
# =========================================================
radio_frame = ctk.CTkFrame(app)
radio_frame.pack(pady=10, padx=10)

ctk.CTkLabel(radio_frame, text="Select CRC32 to Match:").grid(
    row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 10)
)

cols = 2  # change if you want more per row

for i, (name, crc) in enumerate(known_crc32s.items()):
    row = i // cols
    col = i % cols

    rb = ctk.CTkRadioButton(
        radio_frame,
        text=f"{name})",
        variable=selected_crc,
        value=name,
        font=ctk.CTkFont(size=12),
        text_color="#18181A",
        radiobutton_height=12,
        radiobutton_width=12,
        fg_color="#A690E4",
        
    )

    rb.grid(row=row + 1, column=col, padx=25, pady=6, sticky="w")


# ---------- Browse button ----------
browse_button = ctk.CTkButton(app, text="Browse File", command=browse_and_check)
browse_button.pack(pady=10)


# ---------- Output textbox ----------
textbox = ctk.CTkTextbox(app, width=540, height=200, font=("Consolas", 12))
textbox.pack(pady=10)
textbox.insert("0.0", "Output will appear here...")
textbox.configure(state="disabled")


# ---------- Theme toggle ----------
theme_switch = ctk.CTkSwitch(app, text="☀️ Light / 🌙 Dark", command=toggle_theme)
theme_switch.pack(pady=5)
theme_switch.select()


# ---------- Footer ----------
version_label = ctk.CTkLabel(app, text=CURRENT_VERSION, font=ctk.CTkFont(size=8), text_color="#888888")
version_label.pack(anchor="se", padx=6, pady=(0, 1))

signature_label = ctk.CTkLabel(app, text="by syhiranhasf", font=ctk.CTkFont(size=8, slant="italic"), text_color="#aaaaaa")
signature_label.pack(anchor="se", padx=6, pady=(0, 6))


app.protocol("WM_DELETE_WINDOW", exit_app)
app.mainloop()
