# config.py

# Arquivo de Banco de Dados
DB_FILE = "contacts.db"

# Paleta de cores inspirada na Fisk
FISK_RED = "#d9242b"
FISK_BLUE = "#005baa"
SUCCESS_GREEN = "#28a745"
WARNING_ORANGE = "#ffc107"

# Mapeamento e rótulos das colunas do banco de dados/tabela
COLUMNS = [
    ("id", "ID"),
    ("name", "Nome"),
    ("phone", "Telefone"),
    ("email", "Email"),
    ("course", "Curso/Interesse"),
    ("visit_date", "Data da visita"),
    ("status", "Status"),
    ("monthly_fee", "Valor mensalidade"),
    ("how_found", "Como conheceu"),
    ("course_for", "Para quem é"),
    ("attended_by", "Atendido por"),
    ("notes", "Observações"),
]

# Formato de data padrão
DATE_FMT = "%d/%m/%Y"

# Listas de opções para os ComboBoxes
COURSES = ["Inglês", "Espanhol", "Informática", "Profissionalizante", "Robótica"]
STATUS_LIST = ["Novo", "Em contato", "Retornar ligação", "Fechou matrícula", "Sem interesse"]
HOW_FOUND_LIST = [
    "Indicação", "Google", "Instagram", "Facebook", "WhatsApp", "Ligação",
    "Outdoor", "Passagem/Frente da unidade", "Outros"
]
COURSE_FOR_LIST = ["Próprio", "Filho(a)", "Neto(a)", "Sobrinho(a)", "Parceiro(a)", "Outro"]

# Configurações da UI
NOTES_DEFAULT_HEIGHT = 8