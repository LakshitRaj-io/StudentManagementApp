import tkinter as tk
from tkinter import messagebox
from db_config import get_connection
import subprocess
import sys
from time import strftime

# Adjust this if your main app file has a different name
MAIN_APP_FILE = "main_app.py"


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Faculty Login - Student Result System")
        # Bigger default size
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # Fullscreen state
        self.fullscreen = False
        self.root.bind("<F11>", self.toggle_fullscreen_event)
        self.root.bind("<Escape>", self.exit_fullscreen_event)

        # Dark theme colors
        self.bg_color = "#121212"
        self.card_color = "#1E1E1E"
        self.accent_color = "#3F8EFC"
        self.text_color = "#FFFFFF"
        self.muted_text = "#AAAAAA"
        self.error_color = "#FF5555"
        self.entry_bg = "#2A2A2A"

        self.root.configure(bg=self.bg_color)

        # Center frame (card)
        card = tk.Frame(self.root, bg=self.card_color, bd=0, relief=tk.FLAT)
        card.place(relx=0.5, rely=0.5, anchor="center", width=400, height=340)

        # Top bar inside card (clock + fullscreen button)
        top_bar = tk.Frame(card, bg=self.card_color)
        top_bar.pack(fill="x", pady=(5, 0), padx=5)

        self.clock_label = tk.Label(
            top_bar,
            font=("Segoe UI", 9),
            bg=self.card_color,
            fg=self.muted_text,
            anchor="w",
        )
        self.clock_label.pack(side="left", padx=(5, 0))
        self.update_clock()

        fs_btn = tk.Button(
            top_bar,
            text="⤢ Fullscreen",
            font=("Segoe UI", 8),
            bg=self.card_color,
            fg=self.accent_color,
            activebackground=self.card_color,
            activeforeground="#5FA0FF",
            bd=0,
            cursor="hand2",
            command=self.toggle_fullscreen,
        )
        fs_btn.pack(side="right", padx=(0, 5))

        title = tk.Label(
            card,
            text="Teacher Login",
            font=("Segoe UI", 16, "bold"),
            bg=self.card_color,
            fg=self.text_color,
        )
        title.pack(pady=(5, 5))

        subtitle = tk.Label(
            card,
            text="Student Result Management System",
            font=("Segoe UI", 9),
            bg=self.card_color,
            fg=self.muted_text,
        )
        subtitle.pack(pady=(0, 10))

        # Username
        user_label = tk.Label(
            card,
            text="Username",
            font=("Segoe UI", 10),
            bg=self.card_color,
            fg=self.text_color,
            anchor="w",
        )
        user_label.pack(fill="x", padx=25)

        self.username_entry = tk.Entry(
            card,
            font=("Segoe UI", 10),
            bg=self.entry_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            bd=0,
            relief=tk.FLAT,
        )
        self.username_entry.pack(fill="x", padx=25, pady=(0, 10), ipady=4)

        # Password
        pass_label = tk.Label(
            card,
            text="Password",
            font=("Segoe UI", 10),
            bg=self.card_color,
            fg=self.text_color,
            anchor="w",
        )
        pass_label.pack(fill="x", padx=25)

        self.password_entry = tk.Entry(
            card,
            font=("Segoe UI", 10),
            bg=self.entry_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            bd=0,
            relief=tk.FLAT,
            show="*",
        )
        self.password_entry.pack(fill="x", padx=25, pady=(0, 15), ipady=4)

               # Login button
        login_btn = tk.Button(
            card,
            text="Login",
            font=("Segoe UI", 10, "bold"),
            bg=self.accent_color,
            fg=self.text_color,
            activebackground="#5FA0FF",
            activeforeground=self.text_color,
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.login,
        )
        login_btn.pack(fill="x", padx=25, pady=(0, 6), ipady=4)

        info_label = tk.Label(
            card,
            text="Login with your account",
            font=("Segoe UI", 8),
            bg=self.card_color,
            fg=self.muted_text,
        )
        info_label.pack(pady=(0, 2))

        # Register / Forgot password links
        links_frame = tk.Frame(card, bg=self.card_color)
        links_frame.pack(pady=(0, 8))

        reg_btn = tk.Button(
            links_frame,
            text="REGISTER",
            font=("Segoe UI", 8, "underline"),
            bg=self.card_color,
            fg=self.accent_color,
            activebackground=self.card_color,
            activeforeground="#5FA0FF",
            bd=0,
            cursor="hand2",
            command=self.open_register_window,
        )
        reg_btn.pack(side="left", padx=6)

        fp_btn = tk.Button(
            links_frame,
            text="FORGOT PASSWORD?",
            font=("Segoe UI", 8, "underline"),
            bg=self.card_color,
            fg=self.accent_color,
            activebackground=self.card_color,
            activeforeground="#5FA0FF",
            bd=0,
            cursor="hand2",
            command=self.open_forgot_password_window,
        )
        fp_btn.pack(side="left", padx=6)


    # ---------- CLOCK ----------

    def update_clock(self):
        current = strftime("%d-%m-%Y  %H:%M:%S")
        self.clock_label.config(text=current)
        self.clock_label.after(1000, self.update_clock)

    # ---------- FULLSCREEN ----------

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def toggle_fullscreen_event(self, event):
        self.toggle_fullscreen()

    def exit_fullscreen_event(self, event):
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)

    # ---------- LOGIN ----------

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password.")
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "Cannot connect to database.")
            return

        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id FROM users WHERE username=%s AND password=%s",
                (username, password),
            )
            row = cur.fetchone()
            cur.close()
            conn.close()

            if row:
                self.open_main_app()
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def open_main_app(self):
        self.root.destroy()
        subprocess.Popen([sys.executable, MAIN_APP_FILE])

    # ---------- REGISTER USER ----------

    def open_register_window(self):
        win = tk.Toplevel(self.root)
        win.title("Register New User")
        win.geometry("320x230")
        win.configure(bg=self.card_color)
        win.resizable(False, False)

        tk.Label(win, text="Register", font=("Segoe UI", 12, "bold"),
                 bg=self.card_color, fg=self.text_color).pack(pady=(10, 5))

        frame = tk.Frame(win, bg=self.card_color)
        frame.pack(fill="both", expand=True, padx=15, pady=10)

        tk.Label(frame, text="Username", font=("Segoe UI", 10),
                 bg=self.card_color, fg=self.text_color, anchor="w").grid(row=0, column=0, sticky="w")
        username_entry = tk.Entry(
            frame, font=("Segoe UI", 10), bg=self.entry_bg,
            fg=self.text_color, insertbackground=self.text_color,
            bd=0, relief=tk.FLAT
        )
        username_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        tk.Label(frame, text="Password", font=("Segoe UI", 10),
                 bg=self.card_color, fg=self.text_color, anchor="w").grid(row=1, column=0, sticky="w")
        password_entry = tk.Entry(
            frame, font=("Segoe UI", 10), bg=self.entry_bg,
            fg=self.text_color, insertbackground=self.text_color,
            bd=0, relief=tk.FLAT, show="*"
        )
        password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        tk.Label(frame, text="Confirm Password", font=("Segoe UI", 10),
                 bg=self.card_color, fg=self.text_color, anchor="w").grid(row=2, column=0, sticky="w")
        confirm_entry = tk.Entry(
            frame, font=("Segoe UI", 10), bg=self.entry_bg,
            fg=self.text_color, insertbackground=self.text_color,
            bd=0, relief=tk.FLAT, show="*"
        )
        confirm_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        frame.grid_columnconfigure(1, weight=1)

        def do_register():
            u = username_entry.get().strip()
            p = password_entry.get().strip()
            c = confirm_entry.get().strip()
            if not u or not p or not c:
                messagebox.showerror("Error", "All fields are required.", parent=win)
                return
            if p != c:
                messagebox.showerror("Error", "Passwords do not match.", parent=win)
                return

            conn = get_connection()
            if not conn:
                messagebox.showerror("Error", "Cannot connect to database.", parent=win)
                return
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s)",
                    (u, p),
                )
                conn.commit()
                cur.close()
                conn.close()
                messagebox.showinfo("Success", "User registered successfully.", parent=win)
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Could not register user: {e}", parent=win)

        tk.Button(
            win, text="Register", font=("Segoe UI", 10, "bold"),
            bg=self.accent_color, fg=self.text_color,
            activebackground="#5FA0FF", activeforeground=self.text_color,
            bd=0, cursor="hand2", command=do_register
        ).pack(pady=(0, 10), ipadx=10, ipady=4)

    # ---------- FORGOT PASSWORD ----------

    def open_forgot_password_window(self):
        win = tk.Toplevel(self.root)
        win.title("Forgot Password")
        win.geometry("320x230")
        win.configure(bg=self.card_color)
        win.resizable(False, False)

        tk.Label(win, text="Reset Password", font=("Segoe UI", 12, "bold"),
                 bg=self.card_color, fg=self.text_color).pack(pady=(10, 5))

        frame = tk.Frame(win, bg=self.card_color)
        frame.pack(fill="both", expand=True, padx=15, pady=10)

        tk.Label(frame, text="Username", font=("Segoe UI", 10),
                 bg=self.card_color, fg=self.text_color, anchor="w").grid(row=0, column=0, sticky="w")
        username_entry = tk.Entry(
            frame, font=("Segoe UI", 10), bg=self.entry_bg,
            fg=self.text_color, insertbackground=self.text_color,
            bd=0, relief=tk.FLAT
        )
        username_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        tk.Label(frame, text="New Password", font=("Segoe UI", 10),
                 bg=self.card_color, fg=self.text_color, anchor="w").grid(row=1, column=0, sticky="w")
        new_pass_entry = tk.Entry(
            frame, font=("Segoe UI", 10), bg=self.entry_bg,
            fg=self.text_color, insertbackground=self.text_color,
            bd=0, relief=tk.FLAT, show="*"
        )
        new_pass_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        tk.Label(frame, text="Confirm Password", font=("Segoe UI", 10),
                 bg=self.card_color, fg=self.text_color, anchor="w").grid(row=2, column=0, sticky="w")
        confirm_entry = tk.Entry(
            frame, font=("Segoe UI", 10), bg=self.entry_bg,
            fg=self.text_color, insertbackground=self.text_color,
            bd=0, relief=tk.FLAT, show="*"
        )
        confirm_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        frame.grid_columnconfigure(1, weight=1)

        def do_reset():
            u = username_entry.get().strip()
            p = new_pass_entry.get().strip()
            c = confirm_entry.get().strip()
            if not u or not p or not c:
                messagebox.showerror("Error", "All fields are required.", parent=win)
                return
            if p != c:
                messagebox.showerror("Error", "Passwords do not match.", parent=win)
                return

            conn = get_connection()
            if not conn:
                messagebox.showerror("Error", "Cannot connect to database.", parent=win)
                return
            try:
                cur = conn.cursor()
                cur.execute("SELECT id FROM users WHERE username=%s", (u,))
                row = cur.fetchone()
                if not row:
                    messagebox.showerror("Error", "Username not found.", parent=win)
                else:
                    cur.execute(
                        "UPDATE users SET password=%s WHERE username=%s",
                        (p, u),
                    )
                    conn.commit()
                    messagebox.showinfo("Success", "Password updated.", parent=win)
                    win.destroy()
                cur.close()
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", f"Could not update password: {e}", parent=win)

        tk.Button(
            win, text="Update Password", font=("Segoe UI", 10, "bold"),
            bg=self.accent_color, fg=self.text_color,
            activebackground="#5FA0FF", activeforeground=self.text_color,
            bd=0, cursor="hand2", command=do_reset
        ).pack(pady=(0, 10), ipadx=10, ipady=4)


def main():
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
