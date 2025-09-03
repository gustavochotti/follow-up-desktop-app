# ui_manager.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import datetime
import pandas as pd
import os
import sys
import shutil

import ttkbootstrap as b
from ttkbootstrap.constants import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Importando dos nossos módulos
from config import *
from utils import (resource_path, _only_digits, format_ddmmyyyy_from_digits, 
                   format_br_phone_from_digits, normalize_money)
from database import DatabaseManager
from reports import ReportGenerator

class App(b.Window):
    def __init__(self):
        super().__init__(themename="flatly")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.title("Follow-up - Cadastro e Relatórios")
        self.state("zoomed")
        self.minsize(1200, 760)

        # Inicializa os gerenciadores de lógica
        self.db_manager = DatabaseManager(DB_FILE)
        self.report_generator = ReportGenerator()
        
        try:
            self.iconbitmap(resource_path("logo-fisk.ico"))
        except tk.TclError:
            print("Ícone 'logo-fisk.ico' não encontrado.")

        # --- ALTERAÇÃO 1: Inicializando a bandeira de fechamento ---
        self._is_closing = False
        
        self.setup_styles()
        self.initialize_variables()
        self.load_assets()
        self.create_widgets()
        self.bind_events()
        
        self.refresh_filter_options()
        self.refresh_table()
        self.clear_form()

    def setup_styles(self):
        style = b.Style()
        style.configure("Treeview.Heading", background=FISK_BLUE, foreground="white", font=('Helvetica', 10, 'bold'))
        style.map("Treeview.Heading", background=[('active', FISK_RED)])
        style.configure("Treeview", rowheight=25)
        style.map('Treeview', background=[('selected', '#e0e0e0')], foreground=[('selected', 'black')])
        plt.style.use('seaborn-v0_8-pastel')

    # --- ALTERAÇÃO 2: Ativando a bandeira ao iniciar o fechamento ---
    def on_closing(self):
        """
        Executa os procedimentos de limpeza antes de fechar a aplicação.
        """
        # Ativa a bandeira primeiro para que nenhum outro evento seja processado
        self._is_closing = True
        
        # Fecha todas as figuras do Matplotlib para evitar erros em segundo plano
        plt.close('all')
        # Agora, destrói a janela principal do Tkinter
        self.destroy()

    def initialize_variables(self):
        # Variáveis de filtros (Cadastro)
        self.var_search = tk.StringVar()
        self.var_filter_phone = tk.StringVar()
        self.var_filter_att = tk.StringVar(value="Todos")
        self.var_filter_course = tk.StringVar(value="Todos")
        self.var_filter_status = tk.StringVar(value="Todos")
        self.var_filter_from = tk.StringVar()
        self.var_filter_to = tk.StringVar()

        # Variáveis do formulário (Cadastro)
        self.var_name = tk.StringVar()
        self.var_phone = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_course = tk.StringVar()
        self.var_visit_date = tk.StringVar()
        self.var_status = tk.StringVar(value="Novo")
        self.var_monthly_fee = tk.StringVar()
        self.var_how_found = tk.StringVar(value="Indicação")
        self.var_course_for = tk.StringVar(value="Próprio")
        self.var_attended_by = tk.StringVar()

        # Variáveis dos relatórios
        self.var_report_from = tk.StringVar()
        self.var_report_to = tk.StringVar()
        self.report_period = tk.StringVar(value="30_days")
        self.var_report_att = tk.StringVar(value="Todos")
        self.var_report_course = tk.StringVar(value="Todos")
        
    def load_assets(self):
        self.logo_img = None
        try:
            from PIL import Image, ImageTk
            img_path = resource_path("fisk-background-logo.png")
            img = Image.open(img_path)
            img = img.resize((110, 48))
            self.logo_img = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Não foi possível carregar a logo: {e}")

    def create_widgets(self):
        self.create_menu()
        
        self.notebook = b.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.tab_cadastro = b.Frame(self.notebook, padding=(10))
        self.notebook.add(self.tab_cadastro, text='  Cadastro e Acompanhamento  ')
        
        self.tab_relatorios = b.Frame(self.notebook, padding=(10))
        self.notebook.add(self.tab_relatorios, text='  Relatórios  ')

        self.create_cadastro_tab_content()
        self.create_relatorios_tab_content()

    def create_cadastro_tab_content(self):
        self.create_topbar(self.tab_cadastro)
        self.create_form(self.tab_cadastro)
        self.create_table(self.tab_cadastro)

    def create_menu(self):
        menubar = b.Menu(self)
        filemenu = b.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exportar CSV...", command=self.export_csv)
        filemenu.add_command(label="Fazer Backup do Banco de Dados...", command=self.backup_database)
        filemenu.add_command(label="Verificar Contatos Duplicados...", command=self.check_duplicates)
        filemenu.add_separator()
        # Corrigido para usar o método de fechamento seguro
        filemenu.add_command(label="Sair", command=self.on_closing)
        menubar.add_cascade(label="Arquivo", menu=filemenu)
        helpmenu = b.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Sobre", command=self.show_about)
        menubar.add_cascade(label="Ajuda", menu=helpmenu)
        self.config(menu=menubar)

    def create_topbar(self, parent):
        top = b.Frame(parent)
        top.pack(fill=tk.X, pady=(0, 15))
        
        search_row = b.Frame(top)
        search_row.pack(fill=tk.X)
        b.Label(search_row, text="Buscar por nome:").grid(row=0, column=0, sticky=tk.W, padx=(0, 6))
        e_name = b.Entry(search_row, textvariable=self.var_search)
        e_name.grid(row=0, column=1, sticky="ew", padx=(0, 18))
        b.Label(search_row, text="Buscar por telefone:").grid(row=0, column=2, sticky=tk.W, padx=(0, 6))
        e_phone = b.Entry(search_row, textvariable=self.var_filter_phone)
        e_phone.grid(row=0, column=3, sticky="ew", padx=(0, 18))
        b.Frame(search_row).grid(row=0, column=4, sticky="ew")
        
        if self.logo_img:
            b.Label(search_row, image=self.logo_img).grid(row=0, column=5, sticky="e", padx=(6, 0))

        search_row.grid_columnconfigure(1, weight=3, minsize=420)
        search_row.grid_columnconfigure(3, weight=2, minsize=320)
        search_row.grid_columnconfigure(4, weight=1)
        search_row.grid_columnconfigure(5, weight=0)

        self.attach_phone_autofmt(e_phone, self.var_filter_phone)
        
        filt_row = b.Frame(top)
        filt_row.pack(fill=tk.X, pady=(10, 0))

        c = 0
        b.Label(filt_row, text="Atendido por:").grid(row=0, column=c, sticky=tk.W); c += 1
        self.cb_att = b.Combobox(filt_row, textvariable=self.var_filter_att, state="readonly", width=16, values=["Todos"])
        self.cb_att.grid(row=0, column=c, sticky=tk.W, padx=(4, 10)); c += 1
        b.Label(filt_row, text="Curso:").grid(row=0, column=c, sticky=tk.W); c += 1
        self.cb_course = b.Combobox(filt_row, textvariable=self.var_filter_course, state="readonly", width=16, values=["Todos"] + COURSES)
        self.cb_course.grid(row=0, column=c, sticky=tk.W, padx=(4, 10)); c += 1
        b.Label(filt_row, text="Status:").grid(row=0, column=c, sticky=tk.W); c += 1
        self.cb_status = b.Combobox(filt_row, textvariable=self.var_filter_status, state="readonly", width=16, values=["Todos"])
        self.cb_status.grid(row=0, column=c, sticky=tk.W, padx=(4, 10)); c += 1
        b.Label(filt_row, text="Visita de:").grid(row=0, column=c, sticky=tk.W); c += 1
        e_from = b.Entry(filt_row, textvariable=self.var_filter_from, width=15)
        e_from.grid(row=0, column=c, sticky=tk.W, padx=(4, 6)); c += 1
        b.Label(filt_row, text="até:").grid(row=0, column=c, sticky=tk.W, padx=(0, 4)); c += 1
        e_to = b.Entry(filt_row, textvariable=self.var_filter_to, width=15)
        e_to.grid(row=0, column=c, sticky=tk.W, padx=(0, 8)); c += 1
        b.Button(filt_row, text="Aplicar", command=self.refresh_table, bootstyle=PRIMARY).grid(row=0, column=c, padx=(0, 6)); c += 1
        b.Button(filt_row, text="Limpar", command=self.clear_filters, bootstyle="secondary-outline").grid(row=0, column=c, padx=(0, 6)); c += 1
        
        self.attach_date_autofmt(e_from, self.var_filter_from)
        self.attach_date_autofmt(e_to, self.var_filter_to)

    def create_form(self, parent):
        main_form_frame = b.Frame(parent)
        main_form_frame.pack(fill=tk.X)
        
        form = b.LabelFrame(main_form_frame, text=" Dados do contato ", padding=10, bootstyle=PRIMARY)
        form.pack(fill=tk.X)

        row_top = b.Frame(form)
        row_top.pack(fill=tk.X, pady=4)

        labels = ["Nome *", "Telefone", "Email", "Curso/Interesse", "Data da visita", "Status", "Valor de mensalidade (R$)"]
        for i, label in enumerate(labels):
            b.Label(row_top, text=label).grid(row=0, column=i, sticky=tk.W)

        e_name = b.Entry(row_top, textvariable=self.var_name, width=50)
        e_name.grid(row=1, column=0, padx=(0, 12), sticky=tk.W)
        e_phone_form = b.Entry(row_top, textvariable=self.var_phone, width=30)
        e_phone_form.grid(row=1, column=1, padx=(0, 12), sticky=tk.W)
        self.attach_phone_autofmt(e_phone_form, self.var_phone)
        b.Entry(row_top, textvariable=self.var_email, width=35).grid(row=1, column=2, padx=(0, 12), sticky=tk.W)
        b.Combobox(row_top, textvariable=self.var_course, state="readonly", values=COURSES, width=18).grid(row=1, column=3, padx=(0, 12), sticky=tk.W)
        e_visit = b.Entry(row_top, textvariable=self.var_visit_date, width=15)
        e_visit.grid(row=1, column=4, padx=(0, 12), sticky=tk.W)
        self.attach_date_autofmt(e_visit, self.var_visit_date)
        b.Combobox(row_top, textvariable=self.var_status, values=STATUS_LIST, width=18, state="readonly").grid(row=1, column=5, padx=(0, 12), sticky=tk.W)
        e_fee = b.Entry(row_top, textvariable=self.var_monthly_fee, width=24)
        e_fee.grid(row=1, column=6, padx=(0, 0), sticky=tk.W)
        self.attach_money_autofmt(e_fee, self.var_monthly_fee)

        row_mid = b.Frame(form)
        row_mid.pack(fill=tk.X, pady=6)
        b.Label(row_mid, text="Como conheceu a unidade").grid(row=0, column=0, sticky=tk.W)
        b.Combobox(row_mid, textvariable=self.var_how_found, values=HOW_FOUND_LIST, width=28, state="readonly").grid(row=1, column=0, padx=(0,12), sticky=tk.W)
        b.Label(row_mid, text="Para quem é o curso").grid(row=0, column=1, sticky=tk.W)
        b.Combobox(row_mid, textvariable=self.var_course_for, values=COURSE_FOR_LIST, width=22, state="readonly").grid(row=1, column=1, padx=(0,12), sticky=tk.W)
        b.Label(row_mid, text="Atendido por").grid(row=0, column=2, sticky=tk.W)
        b.Entry(row_mid, textvariable=self.var_attended_by, width=25).grid(row=1, column=2, padx=(0,0), sticky=tk.W)

        notes_block = b.LabelFrame(main_form_frame, text=" Observações ", padding=(10, 6), bootstyle=INFO)
        notes_block.pack(fill=tk.X, pady=(10,0))
        notes_inner = b.Frame(notes_block)
        notes_inner.pack(fill=tk.X)
        self.txt_notes = tk.Text(notes_inner, height=NOTES_DEFAULT_HEIGHT, wrap="word", relief="solid", borderwidth=1)
        self.txt_notes.pack(side=tk.LEFT, fill=tk.X, expand=True)
        notes_scroll = b.Scrollbar(notes_inner, orient="vertical", command=self.txt_notes.yview, bootstyle="round")
        notes_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_notes.configure(yscrollcommand=notes_scroll.set)

        btns = b.Frame(main_form_frame)
        btns.pack(fill=tk.X, pady=(15, 0))
        b.Button(btns, text="Novo / Limpar", command=self.clear_form, bootstyle="info-outline").pack(side=tk.LEFT)
        b.Button(btns, text="Salvar", command=self.save_contact, bootstyle=SUCCESS).pack(side=tk.LEFT, padx=6)
        b.Button(btns, text="Atualizar Selecionado", command=self.update_selected, bootstyle=PRIMARY).pack(side=tk.LEFT, padx=6)
        b.Button(btns, text="Apagar Selecionado", command=self.delete_selected, bootstyle=DANGER).pack(side=tk.LEFT, padx=6)

    def create_table(self, parent):
        table_frame = b.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(15,0))
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        cols = [c[0] for c in COLUMNS]
        self.tree = b.Treeview(table_frame, columns=cols, show="headings", selectmode="browse", bootstyle=PRIMARY)
        self.tree.grid(row=0, column=0, sticky="nsew")

        vsb = b.Scrollbar(table_frame, orient="vertical", command=self.tree.yview, bootstyle="round-primary")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb = b.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview, bootstyle="round-primary")
        hsb.grid(row=1, column=0, sticky="ew")
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        widths = {
            "id": 60, "name": 220, "phone": 130, "email": 220, "course": 160,
            "visit_date": 130, "status": 160, "monthly_fee": 140,
            "how_found": 190, "course_for": 150, "attended_by": 150, "notes": 800
        }
        for key, label in COLUMNS:
            self.tree.heading(key, text=label, command=lambda k=key: self.sort_by(k, False))
            self.tree.column(key, width=widths.get(key, 120), anchor=tk.W)

    def create_relatorios_tab_content(self):
        main_frame = b.Frame(self.tab_relatorios)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        filters_frame = b.LabelFrame(main_frame, text=" Filtros de Período ", padding=10, bootstyle=PRIMARY)
        filters_frame.grid(row=0, column=0, sticky="ns", padx=(0, 10))

        b.Label(filters_frame, text="Selecione o período de análise:", justify=tk.LEFT).pack(anchor="w")
        period_options = [
            ("Últimos 7 dias", "7_days"), ("Últimos 15 dias", "15_days"),
            ("Últimos 30 dias", "30_days"), ("Últimos 60 dias", "60_days"),
            ("Últimos 90 dias", "90_days"), ("Este Mês", "this_month"),
        ]
        for text, val in period_options:
            rb = b.Radiobutton(filters_frame, text=text, variable=self.report_period, value=val, bootstyle="primary")
            rb.pack(anchor="w", pady=2, padx=5)
        
        b.Radiobutton(filters_frame, text="Período Personalizado:", variable=self.report_period, value="custom", bootstyle="primary").pack(anchor="w", pady=(10, 2), padx=5)

        custom_date_frame = b.Frame(filters_frame)
        custom_date_frame.pack(anchor="w", padx=25)
        b.Label(custom_date_frame, text="De:").grid(row=0, column=0, padx=(0, 5))
        e_from = b.Entry(custom_date_frame, textvariable=self.var_report_from, width=12)
        e_from.grid(row=0, column=1)
        self.attach_date_autofmt(e_from, self.var_report_from)
        b.Label(custom_date_frame, text="Até:").grid(row=1, column=0, padx=(0, 5), pady=2)
        e_to = b.Entry(custom_date_frame, textvariable=self.var_report_to, width=12)
        e_to.grid(row=1, column=1, pady=2)
        self.attach_date_autofmt(e_to, self.var_report_to)
        
        b.Separator(filters_frame, orient='horizontal').pack(fill='x', pady=10)
        
        b.Label(filters_frame, text="Atendente:").pack(anchor='w', pady=(5,0))
        self.cb_report_att = b.Combobox(filters_frame, textvariable=self.var_report_att, state="readonly", values=["Todos"])
        self.cb_report_att.pack(anchor='w', fill='x', pady=(0,5))
        b.Label(filters_frame, text="Curso:").pack(anchor='w', pady=(5,0))
        self.cb_report_course = b.Combobox(filters_frame, textvariable=self.var_report_course, state="readonly", values=["Todos"] + COURSES)
        self.cb_report_course.pack(anchor='w', fill='x')
        b.Separator(filters_frame, orient='horizontal').pack(fill='x', pady=15)
        b.Button(filters_frame, text="Gerar Relatórios", command=self.update_all_reports, bootstyle=SUCCESS).pack(fill='x', ipady=5)

        if self.logo_img:
            b.Label(filters_frame, image=self.logo_img).pack(side='bottom', anchor='center', pady=20)

        charts_frame = b.Frame(main_frame)
        charts_frame.grid(row=0, column=1, sticky="nsew")
        charts_frame.rowconfigure(1, weight=1)
        charts_frame.columnconfigure(0, weight=1)
        charts_frame.columnconfigure(1, weight=1)

        self.fig1, self.ax1 = self.create_plot_canvas(charts_frame, 0, 0)
        self.fig2, self.ax2 = self.create_plot_canvas(charts_frame, 0, 1)
        self.fig3, self.ax3 = self.create_plot_canvas(charts_frame, 1, 0)
        self.fig4, self.ax4 = self.create_plot_canvas(charts_frame, 1, 1)

    def create_plot_canvas(self, parent, r, c):
        fig = Figure(figsize=(6, 4), dpi=100, constrained_layout=True)
        fig.set_facecolor("#f0f0f0") 
        ax = fig.add_subplot(111)
        ax.set_facecolor("#ffffff")
        
        canvas_frame = b.Frame(parent)
        canvas_frame.grid(row=r, column=c, sticky="nsew", padx=5, pady=5)
        canvas_frame.rowconfigure(0, weight=1)
        canvas_frame.columnconfigure(0, weight=1)

        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        return fig, ax

    # --- ALTERAÇÃO 3: Usando uma função segura para os callbacks ---
    def bind_events(self):
        # Função segura que verifica a bandeira de fechamento antes de agir
        def _safe_refresh_table(*args):
            if self._is_closing:
                return
            self.refresh_table()

        # Usando a função segura para todos os eventos que atualizam a tabela
        self.var_search.trace_add("write", _safe_refresh_table)
        self.var_filter_phone.trace_add("write", _safe_refresh_table)
        self.cb_att.bind("<<ComboboxSelected>>", _safe_refresh_table)
        self.cb_course.bind("<<ComboboxSelected>>", _safe_refresh_table)
        self.cb_status.bind("<<ComboboxSelected>>", _safe_refresh_table)
        
        self.tree.bind("<Double-1>", self.on_double_click)
        
    def refresh_filter_options(self):
        att_list = ["Todos"] + self.db_manager.get_distinct_values("attended_by")
        self.cb_att["values"] = att_list
        self.cb_report_att["values"] = att_list
        
        self.cb_course["values"] = ["Todos"] + COURSES
        self.cb_status["values"] = ["Todos"] + self.db_manager.get_distinct_values("status")

    def ddmmyyyy_to_iso(self, s):
        s = (s or "").strip()
        if not s: return None
        norm = format_ddmmyyyy_from_digits(s)
        if norm: s = norm
        try:
            d = datetime.datetime.strptime(s, DATE_FMT).date()
            return d.strftime("%Y-%m-%d")
        except ValueError:
            return None

    def build_filters(self):
        where, params = [], []
        q = self.var_search.get().strip()
        if q:
            where.append("name LIKE ?")
            params.append(f"%{q}%")
        
        phone_q = _only_digits(self.var_filter_phone.get())
        if phone_q:
            phone_digits_expr = "replace(replace(replace(replace(replace(replace(phone,'(',''),')',''),'-',''),' ',''),'.',''),'+','')"
            where.append(f"{phone_digits_expr} LIKE ?")
            params.append(f"%{phone_q}%")
        
        if self.var_filter_att.get() and self.var_filter_att.get() != "Todos":
            where.append("attended_by = ?")
            params.append(self.var_filter_att.get())
        if self.var_filter_course.get() and self.var_filter_course.get() != "Todos":
            where.append("course = ?")
            params.append(self.var_filter_course.get())
        if self.var_filter_status.get() and self.var_filter_status.get() != "Todos":
            where.append("status = ?")
            params.append(self.var_filter_status.get())

        vfrom_iso = self.ddmmyyyy_to_iso(self.var_filter_from.get())
        vto_iso = self.ddmmyyyy_to_iso(self.var_filter_to.get())
        visit_iso_expr = "(substr(visit_date,7,4)||'-'||substr(visit_date,4,2)||'-'||substr(visit_date,1,2))"
        if vfrom_iso and vto_iso:
            where.append(f"{visit_iso_expr} BETWEEN ? AND ?")
            params.extend([vfrom_iso, vto_iso])
        elif vfrom_iso:
            where.append(f"{visit_iso_expr} >= ?")
            params.append(vfrom_iso)
        elif vto_iso:
            where.append(f"{visit_iso_expr} <= ?")
            params.append(vto_iso)
            
        clause = (" WHERE " + " AND ".join(where)) if where else ""
        return {"clause": clause, "params": params}

    def refresh_table(self):
        for label, v in [("Visita (De)", self.var_filter_from.get().strip()), ("Visita (Até)", self.var_filter_to.get().strip())]:
            if v and self.ddmmyyyy_to_iso(v) is None:
                messagebox.showerror("Erro", "Data inválida. Use dd/mm/aaaa (8 dígitos aceitos).")
                return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        filters = self.build_filters()
        rows = self.db_manager.get_contacts(filters)
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def _get_form_data(self):
        name = self.var_name.get().strip()
        if not name:
            messagebox.showwarning("Atenção", "O campo Nome é obrigatório.")
            return None

        visit_date = self.var_visit_date.get().strip()
        if visit_date and self.ddmmyyyy_to_iso(visit_date) is None:
            messagebox.showerror("Erro", "Data da visita inválida.")
            return None

        return (
            name, self.var_phone.get().strip(), self.var_email.get().strip(),
            self.var_course.get().strip(), visit_date or None, self.var_status.get().strip(),
            normalize_money(self.var_monthly_fee.get()), self.var_how_found.get().strip(),
            self.var_course_for.get().strip(), self.var_attended_by.get().strip(),
            self.txt_notes.get("1.0", tk.END).strip(),
        )

    def save_contact(self):
        data = self._get_form_data()
        if data:
            self.db_manager.add_contact(data)
            self.refresh_filter_options()
            self.refresh_table()
            self.clear_form()
            messagebox.showinfo("Sucesso", "Contato salvo com sucesso.")
    
    def update_selected(self):
        contact_id = self.get_selected_id()
        if not contact_id:
            messagebox.showwarning("Atenção", "Selecione um contato na tabela para atualizar.")
            return

        data = self._get_form_data()
        if data:
            data_with_id = data + (contact_id,)
            self.db_manager.update_contact(data_with_id)
            self.refresh_filter_options()
            self.refresh_table()
            messagebox.showinfo("Sucesso", "Contato atualizado com sucesso.")

    def delete_selected(self):
        contact_id = self.get_selected_id()
        if not contact_id:
            messagebox.showwarning("Atenção", "Selecione um contato para apagar.")
            return
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja apagar este contato?"):
            self.db_manager.delete_contact(contact_id)
            self.refresh_filter_options()
            self.refresh_table()
            self.clear_form()
            messagebox.showinfo("Removido", "Contato apagado.")
    
    def on_double_click(self, event):
        item = self.tree.selection()
        if not item: return
        vals = self.tree.item(item, "values")
        (_id, name, phone, email, course, visit_date, status, monthly_fee, how_found, course_for, attended_by, notes) = vals
        
        self.var_name.set(name)
        self.var_phone.set(phone)
        self.var_email.set(email)
        self.var_course.set(course)
        self.var_visit_date.set(visit_date or "")
        self.var_status.set(status or "Novo")
        self.var_monthly_fee.set(monthly_fee or "")
        self.var_how_found.set(how_found or "Indicação")
        self.var_course_for.set(course_for or "Próprio")
        self.var_attended_by.set(attended_by or "")
        self.txt_notes.delete("1.0", tk.END)
        self.txt_notes.insert(tk.END, notes or "")

    def get_selected_id(self):
        sel = self.tree.selection()
        return self.tree.item(sel, "values")[0] if sel else None

    def clear_form(self):
        self.var_name.set("")
        self.var_phone.set("")
        self.var_email.set("")
        self.var_course.set("")
        self.var_visit_date.set(datetime.date.today().strftime(DATE_FMT))
        self.var_status.set("Novo")
        self.var_monthly_fee.set("")
        self.var_how_found.set("Indicação")
        self.var_course_for.set("Próprio")
        self.var_attended_by.set("")
        if hasattr(self, "txt_notes"):
            self.txt_notes.delete("1.0", tk.END)
        
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection()[0])

    def clear_filters(self):
        self.var_search.set("")
        self.var_filter_phone.set("")
        self.var_filter_att.set("Todos")
        self.var_filter_course.set("Todos")
        self.var_filter_status.set("Todos")
        self.var_filter_from.set("")
        self.var_filter_to.set("")
        self.refresh_table()

    def sort_by(self, col, descending):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        key_func = None
        if col == "visit_date":
            def key(v):
                try: return datetime.datetime.strptime(v[0], DATE_FMT).date() if v[0] else datetime.date.min
                except Exception: return datetime.date.min
            key_func = key
        elif col in ["id", "monthly_fee"]:
            def key(v):
                s = v[0]
                if col == "monthly_fee": s = (s or "").replace(".", "").replace(",", ".")
                try: return float(s)
                except: return 0.0
            key_func = key
        else: key_func = lambda v: (v[0] or "").lower()
        
        data.sort(key=key_func, reverse=descending)
        for index, (_, child) in enumerate(data):
            self.tree.move(child, '', index)
        self.tree.heading(col, command=lambda: self.sort_by(col, not descending))

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")], title="Salvar lista como CSV")
        if not path: return
        filters = self.build_filters()
        rows = self.db_manager.get_contacts(filters)
        
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow([label for _, label in COLUMNS])
            w.writerows(rows)
        messagebox.showinfo("Exportado", f"Arquivo CSV salvo em:\n{path}")
    
    def backup_database(self):
        """
        Cria uma cópia de segurança do arquivo do banco de dados em um local
        escolhido pelo usuário.
        """
        try:
            # Determina o caminho do executável para encontrar o contacts.db
            if getattr(sys, 'frozen', False):
                # Se estiver rodando como um executável (congelado pelo PyInstaller)
                source_dir = os.path.dirname(sys.executable)
            else:
                # Se estiver rodando como um script .py normal
                source_dir = os.path.dirname(os.path.abspath(__file__))

            source_path = os.path.join(source_dir, DB_FILE)

            if not os.path.exists(source_path):
                messagebox.showerror("Erro", f"Arquivo do banco de dados não encontrado em:\n{source_path}")
                return

            # Gera um nome de arquivo de backup com data e hora
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
            suggested_filename = f"backup_contacts_{timestamp}.db"

            # Abre a janela "Salvar como..." para o usuário escolher o destino
            destination_path = filedialog.asksaveasfilename(
                title="Salvar backup do banco de dados como...",
                initialfile=suggested_filename,
                defaultextension=".db",
                filetypes=[("Database files", "*.db"), ("All files", "*.*")]
            )

            # Se o usuário clicou em "Cancelar", o caminho estará vazio
            if not destination_path:
                return

            # Copia o arquivo do banco de dados para o destino escolhido
            shutil.copy2(source_path, destination_path)
            
            messagebox.showinfo("Backup Concluído", f"Backup salvo com sucesso em:\n{destination_path}")

        except Exception as e:
            messagebox.showerror("Erro no Backup", f"Ocorreu um erro inesperado ao tentar criar o backup:\n{e}")
        
    def show_about(self):
        messagebox.showinfo(
            "Sobre",
            "Fisk Follow-up\n"
            "Versão 8.1\n\n"
            "O Fisk Follow-up é uma plataforma inteligente de gestão e análise de contatos.\n\n"
            "Desenvolvido por Gustavo Chotti\n"
            f"Copyright © {datetime.date.today().year}"
        )
        
    # --- MÉTODOS DE AUTO-FORMATAÇÃO COM A VERIFICAÇÃO DE FECHAMENTO ---
    def attach_date_autofmt(self, entry_widget, var: tk.StringVar):
        def on_keyrelease(_ev=None):
            if self._is_closing: return
            digits = _only_digits(var.get())
            if len(digits) == 8:
                fmt = format_ddmmyyyy_from_digits(digits)
                if fmt and fmt != var.get():
                    var.set(fmt)
        def on_focusout(_ev=None):
            if self._is_closing: return
            text = (var.get() or "").strip()
            if not text: return
            fmt = format_ddmmyyyy_from_digits(text) or text
            iso = self.ddmmyyyy_to_iso(fmt)
            if iso:
                d = datetime.datetime.strptime(iso, "%Y-%m-%d").date()
                var.set(d.strftime(DATE_FMT))
        entry_widget.bind("<KeyRelease>", on_keyrelease)
        entry_widget.bind("<FocusOut>", on_focusout)

    def attach_money_autofmt(self, entry_widget, var: tk.StringVar):
        def on_focusout(_ev=None):
            if self._is_closing: return
            s = (var.get() or "").strip()
            if not s: return
            formatted = normalize_money(s)
            var.set(formatted)
        entry_widget.bind("<FocusOut>", on_focusout)

    def attach_phone_autofmt(self, entry_widget, var: tk.StringVar):
        def normalize_and_set(fmt: str):
            var.set(fmt)
            try: entry_widget.icursor(tk.END)
            except Exception: pass
        def on_keyrelease(_ev=None):
            if self._is_closing: return
            d = _only_digits(var.get())
            if len(d) > 11:
                d = d[:11]
                fmt = format_br_phone_from_digits(d)
                if fmt: normalize_and_set(fmt)
            elif len(d) == 11:
                fmt = format_br_phone_from_digits(d)
                if fmt and fmt != var.get(): normalize_and_set(fmt)
        def on_focusout(_ev=None):
            if self._is_closing: return
            fmt = format_br_phone_from_digits(var.get())
            if fmt and fmt != var.get(): var.set(fmt)
        entry_widget.bind("<KeyRelease>", on_keyrelease)
        entry_widget.bind("<FocusOut>", on_focusout)

    # --- MÉTODOS DE RELATÓRIO E DUPLICADOS ---
    def update_all_reports(self):
        df = self.db_manager.get_data_as_dataframe()
        
        from_str = self.var_report_from.get()
        to_str = self.var_report_to.get()
        
        if (self.report_period.get() == "custom"):
            if from_str and self.ddmmyyyy_to_iso(from_str) is None:
                messagebox.showerror("Data Inválida", f"A data 'De' ('{from_str}') é inválida. Use o formato DD/MM/AAAA.")
                return
            if to_str and self.ddmmyyyy_to_iso(to_str) is None:
                messagebox.showerror("Data Inválida", f"A data 'Até' ('{to_str}') é inválida. Use o formato DD/MM/AAAA.")
                return

        df_filtered = self.report_generator.get_filtered_data(
            df, self.report_period.get(), from_str, to_str,
            self.var_report_att.get(), self.var_report_course.get()
        )
        
        self.report_generator.update_visits_enrollments_chart(self.ax1, self.fig1, df_filtered)
        self.report_generator.update_status_distribution_chart(self.ax2, self.fig2, df_filtered)
        self.report_generator.update_lead_source_chart(self.ax3, self.fig3, df_filtered)
        self.report_generator.update_top_courses_chart(self.ax4, self.fig4, df_filtered)

    def check_duplicates(self):
        df = self.db_manager.get_data_as_dataframe()
        if df.empty:
            messagebox.showinfo("Deduplicação", "Nenhum contato na base de dados.")
            return

        df['phone_digits'] = df['phone'].apply(_only_digits)
        df_phone = df[df['phone_digits'] != '']
        df_email = df[df['email'].str.strip() != ''].dropna(subset=['email'])

        phone_dupes = df_phone[df_phone.duplicated(subset=['phone_digits'], keep=False)]
        email_dupes = df_email[df_email.duplicated(subset=['email'], keep=False)]

        all_dupes = pd.concat([phone_dupes, email_dupes]).drop_duplicates(subset=['id']).sort_values('phone_digits')

        if all_dupes.empty:
            messagebox.showinfo("Deduplicação", "Nenhum contato duplicado encontrado.")
            return
        
        self.show_duplicate_manager(all_dupes)

    def show_duplicate_manager(self, df_dupes):
        win = tk.Toplevel(self)
        win.title("Gerenciador de Contatos Duplicados")
        win.geometry("800x600")

        b.Label(win, text="Foram encontrados os seguintes contatos duplicados. Selecione os que deseja apagar.", wraplength=780, justify='left').pack(padx=10, pady=10)

        tree_frame = b.Frame(win)
        tree_frame.pack(expand=True, fill='both', padx=10, pady=5)
        
        cols_dupe = ["id", "name", "phone", "email"]
        tree_dupe = b.Treeview(tree_frame, columns=cols_dupe, show='headings', bootstyle=PRIMARY)
        tree_dupe.pack(side='left', expand=True, fill='both')

        for col in cols_dupe:
            tree_dupe.heading(col, text=col.capitalize())
            tree_dupe.column(col, width=150)
        
        for index, row in df_dupes.iterrows():
            tree_dupe.insert("", "end", values=(row['id'], row['name'], row['phone'], row['email']))

        def delete_selected_dupes():
            selected_items = tree_dupe.selection()
            if not selected_items:
                messagebox.showwarning("Atenção", "Nenhum item selecionado para apagar.", parent=win)
                return

            ids_to_delete = [tree_dupe.item(item)['values'][0] for item in selected_items]
            
            if messagebox.askyesno("Confirmar", f"Tem certeza que deseja apagar os {len(ids_to_delete)} contatos selecionados?", parent=win):
                deleted_count = self.db_manager.delete_contacts_by_ids(ids_to_delete)
                messagebox.showinfo("Sucesso", f"{deleted_count} contatos apagados.", parent=win)
                win.destroy()
                self.refresh_table()
        
        btn_frame = b.Frame(win)
        btn_frame.pack(pady=10)
        b.Button(btn_frame, text="Apagar Selecionados", command=delete_selected_dupes, bootstyle=DANGER).pack(side='left', padx=5)
        b.Button(btn_frame, text="Fechar", command=win.destroy, bootstyle=SECONDARY).pack(side='left', padx=5)