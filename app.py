import os
import subprocess
import datetime
import socket
import platform
import threading
import psutil  # Requer: pip install psutil
import tkinter as tk
from tkinter import messagebox, ttk, filedialog

# --- 1. CONFIGURAÇÕES ---
APP_NAME = "DriverTool Pro"
VERSION = "v2.3.8"

# --- 2. FUNÇÕES DE SEGURANÇA E SUPORTE ---

def log(mensagem, cor="#00ff00"):
    status_var.set(mensagem)
    status.configure(fg=cor)
    app.update_idletasks()

def salvar_log_tecnico(detalhes):
    """Cria um log de erro no Desktop para diagnóstico."""
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        caminho_log = os.path.join(desktop, "drivertool_debug_log.txt")
        with open(caminho_log, "a", encoding="utf-8") as f:
            f.write(f"\n[{datetime.datetime.now()}] ERROR:\n{detalhes}\n{'-'*50}")
    except:
        pass

def verificar_energia():
    """Garante que notebooks tenham bateria para evitar corrupção de arquivos."""
    bateria = psutil.sensors_battery()
    if bateria is None: return True
    if not bateria.power_plugged and bateria.percent < 25:
        return False
    return True

def executar_thread(funcao):
    thread = threading.Thread(target=funcao, daemon=True)
    thread.start()

def validar_pasta_drivers(caminho):
    """Checa se a pasta selecionada tem drivers (.inf) reais."""
    for root, dirs, files in os.walk(caminho):
        if any(f.lower().endswith('.inf') for f in files):
            return True
    return False

# --- 3. FUNÇÕES PRINCIPAIS ---

def info_sistema():
    info = (
        f"Nome do PC: {socket.gethostname()}\n"
        f"Sistema: {platform.system()} {platform.release()}\n"
        f"Versão: {platform.version()}"
    )
    messagebox.showinfo("Informações", info)

def backup_drivers():
    if not verificar_energia():
        messagebox.showwarning("Energia", "Conecte o carregador para fazer o backup!")
        return

    try:
        progress.start(10)
        pc = socket.gethostname()
        data = datetime.date.today().strftime("%d-%m-%Y")
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        pasta_final = os.path.join(desktop, f"BACKUP_DRIVERS_{pc}_{data}")
        
        if not os.path.exists(pasta_final):
            os.makedirs(pasta_final)
        
        log("🚀 Exportando drivers para o Desktop...")
        res = subprocess.run(f'dism /online /export-driver /destination:"{pasta_final}"', 
                             shell=True, capture_output=True, text=True)
        
        progress.stop()
        if res.returncode == 0:
            log("✅ Backup concluído!", "#00ff00")
            messagebox.showinfo("Sucesso", f"Drivers salvos em:\n{pasta_final}")
        else:
            salvar_log_tecnico(res.stdout)
            log("❌ Erro no Backup", "red")
            messagebox.showerror("Erro", "Falha na exportação. Verifique o log no Desktop.")
    except Exception as e:
        progress.stop()
        log("❌ Falha Crítica", "red")
        messagebox.showerror("Erro", str(e))

def restaurar_drivers():
    caminho = filedialog.askdirectory(title="Selecione a pasta de Backup")
    if not caminho: return

    if not validar_pasta_drivers(caminho):
        log("⚠️ Pasta inválida", "yellow")
        messagebox.showwarning("Aviso", "Esta pasta não contém arquivos .inf.")
        return

    try:
        progress.start(10)
        log("📥 Instalando drivers via PnPUtil...")
        caminho_limpo = os.path.normpath(caminho)
        
        # PnPUtil ignora o Erro 50 e permite instalação online
        cmd = f'pnputil /add-driver "{caminho_limpo}\\*.inf" /subdirs /install'
        processo = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        progress.stop()
        if processo.returncode == 0 or "adicionado com êxito" in processo.stdout.lower():
            log("✅ Restauração Finalizada", "#00ff00")
            messagebox.showinfo("Sucesso", "Drivers processados com sucesso pelo Windows!")
        else:
            salvar_log_tecnico(processo.stdout)
            log("⚠️ Aviso de instalação", "yellow")
            messagebox.showwarning("Resultado", "Processo concluído, mas alguns drivers podem ter sido ignorados.")
    except Exception as e:
        progress.stop()
        log("❌ Erro Crítico", "red")
        messagebox.showerror("Erro", str(e))

def reparar_windows():
    def acao():
        if not verificar_energia():
            messagebox.showwarning("Energia", "Conecte o carregador para o reparo do sistema!")
            return
        try:
            progress.start(10)
            log("🛠️ Reparando imagem e arquivos...")
            subprocess.run('dism /online /cleanup-image /restorehealth', shell=True)
            subprocess.run('sfc /scannow', shell=True)
            progress.stop()
            log("✅ Sistema Reparado", "#00ff00")
            messagebox.showinfo("Sucesso", "O Windows foi reparado!")
        except:
            progress.stop()
            log("❌ Erro no Reparo", "red")
    executar_thread(acao)

def limpar_temp():
    try:
        log("🧹 Limpando arquivos temporários...")
        subprocess.run('del /q/f/s %TEMP%\\*', shell=True)
        subprocess.run('del /q/f/s C:\\Windows\\Temp\\*', shell=True)
        log("✅ Limpeza Concluída")
        messagebox.showinfo("Limpeza", "Arquivos desnecessários removidos.")
    except:
        log("⚠️ Limpeza parcial", "yellow")

# --- 4. INTERFACE ---

app = tk.Tk()
app.title(f"{APP_NAME} {VERSION}")
app.geometry("480x720")
app.configure(bg="#1e1e1e")
app.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 10), padding=10)
style.configure("Horizontal.TProgressbar", background='#0078d7', trowcolor='#1e1e1e')

tk.Label(app, text="DRIVERTOOL PRO", font=("Segoe UI", 24, "bold"), bg="#1e1e1e", fg="#0078d7").pack(pady=20)

container = tk.Frame(app, bg="#1e1e1e")
container.pack(fill="both", expand=True, padx=40)

menu = [
    ("📊 Informações do Sistema", info_sistema),
    ("💾 Fazer Backup (Desktop)", lambda: executar_thread(backup_drivers)),
    ("📥 Selecionar e Restaurar Drivers", lambda: executar_thread(restaurar_drivers)),
    ("🛠️ Reparo Completo (SFC/DISM)", reparar_windows),
    ("🧹 Limpar Arquivos Temporários", lambda: executar_thread(limpar_temp)),
    ("🖥️ Gerenciador de Dispositivos", lambda: subprocess.run('devmgmt.msc', shell=True)),
]

for texto, comando in menu:
    ttk.Button(container, text=texto, command=comando).pack(fill="x", pady=5)

progress = ttk.Progressbar(app, orient="horizontal", length=320, mode="indeterminate", style="Horizontal.TProgressbar")
progress.pack(pady=25)

status_var = tk.StringVar(value="Pronto")
status = tk.Label(app, textvariable=status_var, bg="#111", fg="#00ff00", anchor="w", padx=15, height=2, font=("Consolas", 9))
status.pack(fill="x", side="bottom")

app.mainloop()