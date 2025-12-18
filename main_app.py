import tkinter as tk
from tkinter import ttk, messagebox
from db_config import get_connection


class StudentResultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1100x650")
        self.root.minsize(1000, 600)

        # Dark theme colors
        self.bg_color = "#101010"
        self.header_color = "#181818"
        self.card_color = "#1E1E1E"
        self.accent_color = "#3F8EFC"
        self.accent_alt = "#FFB300"
        self.text_color = "#FFFFFF"
        self.muted_text = "#AAAAAA"
        self.error_color = "#FF5555"
        self.success_color = "#55FF88"
        self.entry_bg = "#2A2A2A"

        self.root.configure(bg=self.bg_color)

        self.marks_entries = {}   # subject_id -> Entry widget

        self.setup_style()
        self.build_layout()
        self.load_subjects()
        self.load_students()
        self.load_results()

    # ----APPEARANCE SETUP----

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background=self.card_color,
            foreground=self.text_color,
            fieldbackground=self.card_color,
            rowheight=24,
            bordercolor=self.header_color,
            borderwidth=0,
        )
        style.map("Treeview", background=[("selected", "#305D9C")])

        style.configure(
            "Treeview.Heading",
            background=self.header_color,
            foreground=self.text_color,
            relief="flat",
        )

        style.configure(
            "TNotebook",
            background=self.bg_color,
            borderwidth=0,
        )
        style.configure(
            "TNotebook.Tab",
            background=self.header_color,
            foreground=self.muted_text,
            padding=[15, 5],
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", self.card_color)],
            foreground=[("selected", self.text_color)],
        )

    def build_layout(self):
        header = tk.Frame(self.root, bg=self.header_color, height=60)
        header.pack(side="top", fill="x")

        title = tk.Label(
            header,
            text="Student Result Management System",
            font=("Segoe UI", 16, "bold"),
            bg=self.header_color,
            fg=self.text_color,
        )
        title.pack(side="left", padx=20)

        subtitle = tk.Label(
            header,
            text="CREATED BY LAKSHIT RAJ | E-CELL | MEMBER-TECHNICAL(AIML)",
            font=("Times New Roman", 9),
            bg=self.header_color,
            fg=self.muted_text,
        )
        subtitle.pack(side="left", padx=10)

        logout_btn = tk.Button(
            header,
            text="Logout",
            font=("Segoe UI", 10, "bold"),
            bg="#333333",
            fg=self.text_color,
            activebackground="#444444",
            activeforeground=self.text_color,
            bd=0,
            cursor="hand2",
            command=self.root.destroy,
        )
        logout_btn.pack(side="right", padx=20, pady=10, ipadx=10, ipady=4)

        main_body = tk.Frame(self.root, bg=self.bg_color)
        main_body.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(main_body)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.subjects_tab = tk.Frame(self.notebook, bg=self.bg_color)
        self.students_tab = tk.Frame(self.notebook, bg=self.bg_color)
        self.results_tab = tk.Frame(self.notebook, bg=self.bg_color)

        self.notebook.add(self.subjects_tab, text="Subjects")
        self.notebook.add(self.students_tab, text="Students & Marks")
        self.notebook.add(self.results_tab, text="Results")

        self.build_subjects_tab()
        self.build_students_tab()
        self.build_results_tab()

    # ---------- SUBJECTS ----------

    def build_subjects_tab(self):
        left_frame = tk.Frame(self.subjects_tab, bg=self.bg_color)
        left_frame.pack(side="left", fill="y", padx=(10, 5), pady=10)

        card = tk.Frame(left_frame, bg=self.card_color, bd=0)
        card.pack(fill="x")

        title = tk.Label(
            card,
            text="Add Course Details",
            font=("Segoe UI", 12, "bold"),
            bg=self.card_color,
            fg=self.text_color,
        )
        title.pack(pady=(10, 5), padx=15, anchor="w")

        name_label = tk.Label(
            card,
            text="Course Name With Code",
            font=("Segoe UI", 10),
            bg=self.card_color,
            fg=self.text_color,
        )
        name_label.pack(padx=15, pady=(5, 0), anchor="w")

        self.subject_name_entry = tk.Entry(
            card,
            font=("Segoe UI", 10),
            bg=self.entry_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            bd=0,
            relief=tk.FLAT,
        )
        self.subject_name_entry.pack(padx=15, pady=(0, 10), fill="x", ipady=4)

        btn_frame = tk.Frame(card, bg=self.card_color)
        btn_frame.pack(padx=15, pady=(0, 15), fill="x")

        add_btn = tk.Button(
            btn_frame,
            text="Add Course",
            font=("Segoe UI", 10, "bold"),
            bg=self.accent_color,
            fg=self.text_color,
            activebackground="#5FA0FF",
            activeforeground=self.text_color,
            bd=0,
            cursor="hand2",
            command=self.add_subject,
        )
        add_btn.pack(side="left", ipadx=10, ipady=4)

        del_btn = tk.Button(
            btn_frame,
            text="Delete Selected",
            font=("Segoe UI", 10, "bold"),
            bg="#AA3333",
            fg=self.text_color,
            activebackground="#CC4444",
            activeforeground=self.text_color,
            bd=0,
            cursor="hand2",
            command=self.delete_subject,
        )
        del_btn.pack(side="left", padx=10, ipadx=10, ipady=4)

        right_frame = tk.Frame(self.subjects_tab, bg=self.bg_color)
        right_frame.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)

        table_card = tk.Frame(right_frame, bg=self.card_color, bd=0)
        table_card.pack(fill="both", expand=True)

        table_title = tk.Label(
            table_card,
            text="Course List",
            font=("Segoe UI", 12, "bold"),
            bg=self.card_color,
            fg=self.text_color,
        )
        table_title.pack(pady=(10, 5), padx=10, anchor="w")

        columns = ("id", "name")
        self.subject_tree = ttk.Treeview(
            table_card,
            columns=columns,
            show="headings",
            selectmode="browse",
        )
        self.subject_tree.heading("id", text="ID")
        self.subject_tree.heading("name", text="Subject Name")
        self.subject_tree.column("id", width=60, anchor="center")
        self.subject_tree.column("name", width=200, anchor="w")

        vsb = ttk.Scrollbar(table_card, orient="vertical", command=self.subject_tree.yview)
        self.subject_tree.configure(yscrollcommand=vsb.set)

        self.subject_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(0, 10))
        vsb.pack(side="left", fill="y", padx=(0, 10), pady=(0, 10))

    def add_subject(self):
        name = self.subject_name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Subject name cannot be empty.")
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "Cannot connect to database.")
            return

        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO subjects (subject_name) VALUES (%s)",
                (name,),
            )
            conn.commit()
            cur.close()
            conn.close()

            self.subject_name_entry.delete(0, tk.END)
            self.load_subjects()
            self.refresh_subjects_in_marks()
            messagebox.showinfo("Success", "Subject added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not add subject: {e}")

    def delete_subject(self):
        selected = self.subject_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a subject to delete.")
            return

        item = self.subject_tree.item(selected[0])
        subject_id = item["values"][0]

        if not messagebox.askyesno(
            "Confirm Delete", "Delete this subject? Related marks will also be deleted."
        ):
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "Cannot connect to database.")
            return

        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM subjects WHERE id=%s", (subject_id,))
            conn.commit()
            cur.close()
            conn.close()

            self.load_subjects()
            self.refresh_subjects_in_marks()
            self.load_results()
            messagebox.showinfo("Success", "Subject deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete subject: {e}")

    def load_subjects(self):
        for row in self.subject_tree.get_children():
            self.subject_tree.delete(row)

        conn = get_connection()
        if not conn:
            return

        try:
            cur = conn.cursor()
            cur.execute("SELECT id, subject_name FROM subjects ORDER BY id")
            for row in cur.fetchall():
                self.subject_tree.insert("", tk.END, values=row)
            cur.close()
            conn.close()
        except Exception as e:
            print("Error loading subjects:", e)

    # ---------- STUDENTS & MARKS TAB ----------

    def build_students_tab(self):
        top_frame = tk.Frame(self.students_tab, bg=self.bg_color)
        top_frame.pack(side="top", fill="x", padx=10, pady=(10, 5))

        card = tk.Frame(top_frame, bg=self.card_color)
        card.pack(fill="x")

        title = tk.Label(
            card,
            text="Student Details & Marks",
            font=("Segoe UI", 12, "bold"),
            bg=self.card_color,
            fg=self.text_color,
        )
        title.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 5), sticky="w")

        row_y = 1
        tk.Label(card, text="Register No", font=("Segoe UI", 10),
                 bg=self.card_color, fg=self.text_color).grid(row=row_y, column=0, padx=10, pady=5, sticky="w")
        self.roll_entry = tk.Entry(
            card, font=("Segoe UI", 10), bg=self.entry_bg,
            fg=self.text_color, insertbackground=self.text_color,
            bd=0, relief=tk.FLAT
        )
        self.roll_entry.grid(row=row_y, column=1, padx=10, pady=5, sticky="we")

        tk.Label(card, text="Name", font=("Segoe UI", 10),
                 bg=self.card_color, fg=self.text_color).grid(row=row_y, column=2, padx=10, pady=5, sticky="w")
        self.name_entry = tk.Entry(
            card, font=("Segoe UI", 10), bg=self.entry_bg,
            fg=self.text_color, insertbackground=self.text_color,
            bd=0, relief=tk.FLAT
        )
        self.name_entry.grid(row=row_y, column=3, padx=10, pady=5, sticky="we")

        row_y += 1
        tk.Label(card, text="Department & Specialisation", font=("Segoe UI", 10),
                 bg=self.card_color, fg=self.text_color).grid(row=row_y, column=0, padx=10, pady=5, sticky="w")
        self.class_entry = tk.Entry(
            card, font=("Segoe UI", 10), bg=self.entry_bg,
            fg=self.text_color, insertbackground=self.text_color,
            bd=0, relief=tk.FLAT
        )
        self.class_entry.grid(row=row_y, column=1, padx=10, pady=5, sticky="we")

        tk.Label(card, text="Section", font=("Segoe UI", 10),
                 bg=self.card_color, fg=self.text_color).grid(row=row_y, column=2, padx=10, pady=5, sticky="w")
        self.section_entry = tk.Entry(
            card, font=("Segoe UI", 10), bg=self.entry_bg,
            fg=self.text_color, insertbackground=self.text_color,
            bd=0, relief=tk.FLAT
        )
        self.section_entry.grid(row=row_y, column=3, padx=10, pady=5, sticky="we")

        for i in range(4):
            card.grid_columnconfigure(i, weight=1)

        marks_frame = tk.Frame(self.students_tab, bg=self.bg_color)
        marks_frame.pack(side="top", fill="x", padx=10, pady=(5, 10))

        marks_card = tk.Frame(marks_frame, bg=self.card_color)
        marks_card.pack(fill="x")

        m_title = tk.Label(
            marks_card,
            text="Marks (per subject)",
            font=("Segoe UI", 12, "bold"),
            bg=self.card_color,
            fg=self.text_color,
        )
        m_title.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 5), sticky="w")

        self.marks_container = marks_card
        self.refresh_subjects_in_marks()

        btn_frame = tk.Frame(self.students_tab, bg=self.bg_color)
        btn_frame.pack(side="top", fill="x", padx=10, pady=(0, 10))

        save_btn = tk.Button(
            btn_frame,
            text="Save / Update Student & Marks",
            font=("Segoe UI", 10, "bold"),
            bg=self.accent_color,
            fg=self.text_color,
            activebackground="#5FA0FF",
            activeforeground=self.text_color,
            bd=0,
            cursor="hand2",
            command=self.save_student_and_marks,
        )
        save_btn.pack(side="left", padx=(0, 10), ipadx=10, ipady=4)

        clear_btn = tk.Button(
            btn_frame,
            text="Clear Form",
            font=("Segoe UI", 10, "bold"),
            bg="#444444",
            fg=self.text_color,
            activebackground="#555555",
            activeforeground=self.text_color,
            bd=0,
            cursor="hand2",
            command=self.clear_student_form,
        )
        clear_btn.pack(side="left", ipadx=10, ipady=4)

        delete_btn = tk.Button(
            btn_frame,
            text="Delete Selected Student",
            font=("Segoe UI", 10, "bold"),
            bg="#AA3333",
            fg=self.text_color,
            activebackground="#CC4444",
            activeforeground=self.text_color,
            bd=0,
            cursor="hand2",
            command=self.delete_student,
        )
        delete_btn.pack(side="left", padx=10, ipadx=10, ipady=4)

        bottom_frame = tk.Frame(self.students_tab, bg=self.bg_color)
        bottom_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 10))

        card2 = tk.Frame(bottom_frame, bg=self.card_color)
        card2.pack(fill="both", expand=True)

        s_title = tk.Label(
            card2,
            text="Students",
            font=("Segoe UI", 12, "bold"),
            bg=self.card_color,
            fg=self.text_color,
        )
        s_title.pack(pady=(10, 5), padx=10, anchor="w")

        columns = ("id", "roll", "name", "class", "section")
        self.student_tree = ttk.Treeview(
            card2, columns=columns, show="headings", selectmode="browse"
        )
        self.student_tree.heading("id", text="ID")
        self.student_tree.heading("roll", text="Roll No")
        self.student_tree.heading("name", text="Name")
        self.student_tree.heading("class", text="Class")
        self.student_tree.heading("section", text="Section")

        self.student_tree.column("id", width=50, anchor="center")
        self.student_tree.column("roll", width=100, anchor="center")
        self.student_tree.column("name", width=200, anchor="w")
        self.student_tree.column("class", width=100, anchor="center")
        self.student_tree.column("section", width=80, anchor="center")

        vsb = ttk.Scrollbar(card2, orient="vertical", command=self.student_tree.yview)
        self.student_tree.configure(yscrollcommand=vsb.set)

        self.student_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(0, 10))
        vsb.pack(side="left", fill="y", padx=(0, 10), pady=(0, 10))

        self.student_tree.bind("<<TreeviewSelect>>", self.on_student_select)

    def refresh_subjects_in_marks(self):
        for widget in self.marks_container.grid_slaves():
            if int(widget.grid_info().get("row", 99)) >= 1:
                widget.destroy()

        self.marks_entries.clear()

        conn = get_connection()
        if not conn:
            return

        try:
            cur = conn.cursor()
            cur.execute("SELECT id, subject_name FROM subjects ORDER BY id")
            subjects = cur.fetchall()
            cur.close()
            conn.close()
        except Exception as e:
            print("Error loading subjects for marks:", e)
            subjects = []

        if not subjects:
            label = tk.Label(
                self.marks_container,
                text="No subjects yet. Add subjects in the Subjects tab.",
                font=("Segoe UI", 9),
                bg=self.card_color,
                fg=self.muted_text,
            )
            label.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="w")
            return

        row = 1
        col = 0
        for subject_id, subject_name in subjects:
            lbl = tk.Label(
                self.marks_container,
                text=f"{subject_name} Marks",
                font=("Segoe UI", 10),
                bg=self.card_color,
                fg=self.text_color,
            )
            lbl.grid(row=row, column=col, padx=10, pady=5, sticky="w")

            entry = tk.Entry(
                self.marks_container,
                font=("Segoe UI", 10),
                bg=self.entry_bg,
                fg=self.text_color,
                insertbackground=self.text_color,
                bd=0,
                relief=tk.FLAT,
                width=10,
            )
            entry.grid(row=row, column=col + 1, padx=10, pady=5, sticky="w")

            self.marks_entries[subject_id] = entry

            col += 2
            if col >= 4:
                col = 0
                row += 1

    def save_student_and_marks(self):
        roll = self.roll_entry.get().strip()
        name = self.name_entry.get().strip()
        class_name = self.class_entry.get().strip()
        section = self.section_entry.get().strip()

        if not roll or not name:
            messagebox.showerror("Error", "Roll No and Name are required.")
            return

        marks_dict = {}
        for subject_id, entry in self.marks_entries.items():
            val = entry.get().strip()
            if val == "":
                continue
            try:
                m = float(val)
            except ValueError:
                messagebox.showerror("Error", f"Invalid marks for subject ID {subject_id}.")
                return
            marks_dict[subject_id] = m

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "Cannot connect to database.")
            return

        try:
            cur = conn.cursor()

            cur.execute("SELECT id FROM students WHERE roll_no=%s", (roll,))
            row = cur.fetchone()
            if row:
                student_id = row[0]
                cur.execute(
                    """
                    UPDATE students
                    SET name=%s, class_name=%s, section=%s
                    WHERE id=%s
                    """,
                    (name, class_name, section, student_id),
                )
            else:
                cur.execute(
                    """
                    INSERT INTO students (roll_no, name, class_name, section)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (roll, name, class_name, section),
                )
                student_id = cur.lastrowid

            cur.execute("DELETE FROM marks WHERE student_id=%s", (student_id,))
            for subject_id, m in marks_dict.items():
                cur.execute(
                    """
                    INSERT INTO marks (student_id, subject_id, marks_obtained)
                    VALUES (%s, %s, %s)
                    """,
                    (student_id, subject_id, m),
                )

            conn.commit()
            cur.close()
            conn.close()

            self.load_students()
            self.load_results()
            messagebox.showinfo("Success", "Student and marks saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save data: {e}")

    def clear_student_form(self):
        self.roll_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.class_entry.delete(0, tk.END)
        self.section_entry.delete(0, tk.END)
        for entry in self.marks_entries.values():
            entry.delete(0, tk.END)

    def on_student_select(self, event):
        selected = self.student_tree.selection()
        if not selected:
            return

        item = self.student_tree.item(selected[0])
        student_id, roll, name, class_name, section = item["values"]

        self.roll_entry.delete(0, tk.END)
        self.roll_entry.insert(0, roll)

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, name)

        self.class_entry.delete(0, tk.END)
        self.class_entry.insert(0, class_name)

        self.section_entry.delete(0, tk.END)
        self.section_entry.insert(0, section)

        for entry in self.marks_entries.values():
            entry.delete(0, tk.END)

        conn = get_connection()
        if not conn:
            return

        try:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT subject_id, marks_obtained
                FROM marks
                WHERE student_id=%s
                """,
                (student_id,),
            )
            for subject_id, marks in cur.fetchall():
                entry = self.marks_entries.get(subject_id)
                if entry:
                    entry.insert(0, str(marks))
            cur.close()
            conn.close()
        except Exception as e:
            print("Error loading student marks:", e)

    def delete_student(self):
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to delete.")
            return

        item = self.student_tree.item(selected[0])
        student_id = item["values"][0]

        if not messagebox.askyesno(
            "Confirm Delete", "Delete this student and all their marks?"
        ):
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "Cannot connect to database.")
            return

        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM students WHERE id=%s", (student_id,))
            conn.commit()
            cur.close()
            conn.close()

            self.load_students()
            self.load_results()
            self.clear_student_form()
            messagebox.showinfo("Success", "Student deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete student: {e}")

    def load_students(self):
        for row in self.student_tree.get_children():
            self.student_tree.delete(row)

        conn = get_connection()
        if not conn:
            return

        try:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, roll_no, name, class_name, section
                FROM students
                ORDER BY id
                """
            )
            for row in cur.fetchall():
                self.student_tree.insert("", tk.END, values=row)
            cur.close()
            conn.close()
        except Exception as e:
            print("Error loading students:", e)

    # ---------- RESULTS TAB ----------

    def build_results_tab(self):
        top_frame = tk.Frame(self.results_tab, bg=self.bg_color)
        top_frame.pack(side="top", fill="x", padx=10, pady=(10, 5))

        card = tk.Frame(top_frame, bg=self.card_color)
        card.pack(fill="x")

        title = tk.Label(
            card,
            text="Results",
            font=("Segoe UI", 12, "bold"),
            bg=self.card_color,
            fg=self.text_color,
        )
        title.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 5), sticky="w")

        tk.Label(
            card,
            text="Search (Roll or Name)",
            font=("Segoe UI", 10),
            bg=self.card_color,
            fg=self.text_color,
        ).grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.search_entry = tk.Entry(
            card,
            font=("Segoe UI", 10),
            bg=self.entry_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            bd=0,
            relief=tk.FLAT,
        )
        self.search_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        search_btn = tk.Button(
            card,
            text="Search",
            font=("Segoe UI", 10, "bold"),
            bg=self.accent_color,
            fg=self.text_color,
            activebackground="#5FA0FF",
            activeforeground=self.text_color,
            bd=0,
            cursor="hand2",
            command=self.load_results,
        )
        search_btn.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        reset_btn = tk.Button(
            card,
            text="Reset",
            font=("Segoe UI", 10, "bold"),
            bg="#444444",
            fg=self.text_color,
            activebackground="#555555",
            activeforeground=self.text_color,
            bd=0,
            cursor="hand2",
            command=self.reset_results_search,
        )
        reset_btn.grid(row=1, column=3, padx=10, pady=5, sticky="w")

        for c in range(4):
            card.grid_columnconfigure(c, weight=1)

        bottom_frame = tk.Frame(self.results_tab, bg=self.bg_color)
        bottom_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 10))

        card2 = tk.Frame(bottom_frame, bg=self.card_color)
        card2.pack(fill="both", expand=True)

        columns = (
            "roll",
            "name",
            "class",
            "section",
            "total",
            "percent",
            "grade",
        )

        self.results_tree = ttk.Treeview(
            card2, columns=columns, show="headings", selectmode="browse"
        )

        self.results_tree.heading("roll", text="Roll No")
        self.results_tree.heading("name", text="Name")
        self.results_tree.heading("class", text="Class")
        self.results_tree.heading("section", text="Section")
        self.results_tree.heading("total", text="Total Marks")
        self.results_tree.heading("percent", text="Percentage")
        self.results_tree.heading("grade", text="Grade")

        self.results_tree.column("roll", width=80, anchor="center")
        self.results_tree.column("name", width=200, anchor="w")
        self.results_tree.column("class", width=80, anchor="center")
        self.results_tree.column("section", width=60, anchor="center")
        self.results_tree.column("total", width=100, anchor="center")
        self.results_tree.column("percent", width=100, anchor="center")
        self.results_tree.column("grade", width=80, anchor="center")

        vsb = ttk.Scrollbar(card2, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=vsb.set)

        self.results_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(0, 10))
        vsb.pack(side="left", fill="y", padx=(0, 10), pady=(0, 10))

    def reset_results_search(self):
        self.search_entry.delete(0, tk.END)
        self.load_results()

    def load_results(self):
        for row in self.results_tree.get_children():
            self.results_tree.delete(row)

        search_text = self.search_entry.get().strip()
        like_pattern = f"%{search_text}%" if search_text else None

        conn = get_connection()
        if not conn:
            return

        try:
            cur = conn.cursor()

            query = """
                SELECT
                    s.roll_no,
                    s.name,
                    s.class_name,
                    s.section,
                    COALESCE(SUM(m.marks_obtained), 0) AS total_marks,
                    CASE
                        WHEN COUNT(m.subject_id) = 0 THEN 0
                        ELSE ROUND(SUM(m.marks_obtained) / COUNT(m.subject_id), 2)
                    END AS percent_marks
                FROM students s
                LEFT JOIN marks m ON s.id = m.student_id
            """
            params = []

            if like_pattern:
                query += """
                    WHERE s.roll_no LIKE %s OR s.name LIKE %s
                """
                params.extend([like_pattern, like_pattern])

            query += """
                GROUP BY s.id
                ORDER BY s.id
            """

            cur.execute(query, tuple(params))
            rows = cur.fetchall()

            for roll_no, name, class_name, section, total, percent in rows:
                grade = self.calculate_grade(percent)
                self.results_tree.insert(
                    "", tk.END,
                    values=(roll_no, name, class_name, section, total, percent, grade)
                )

            cur.close()
            conn.close()
        except Exception as e:
            print("Error loading results:", e)

    @staticmethod
    def calculate_grade(percent):
        if percent >= 90:
            return "A+"
        elif percent >= 80:
            return "A"
        elif percent >= 70:
            return "B+"
        elif percent >= 60:
            return "B"
        elif percent >= 50:
            return "C"
        elif percent >= 40:
            return "D"
        else:
            return "F"


def main():
    root = tk.Tk()
    app = StudentResultApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
