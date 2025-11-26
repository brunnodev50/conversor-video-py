import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from moviepy.editor import VideoFileClip
import threading
import os

# Função para converter vídeos com barra de progresso
def convert_video(input_file, output_file, output_format):
    try:
        # Verifica se a extensão do arquivo de saída corresponde ao formato selecionado
        if not output_file.endswith(f".{output_format}"):
            messagebox.showerror("Erro", f"A extensão do arquivo de saída deve ser .{output_format}")
            return
        
        video = VideoFileClip(input_file)
        progress_bar.start()
        
        # Executa a conversão apropriada com base no formato de saída
        if output_format == "mp3":
            # Para mp3, converte apenas o áudio
            video.audio.write_audiofile(output_file, codec="libmp3lame")
        else:
            # Para outros formatos de vídeo, converte o vídeo completo
            video.write_videofile(output_file, codec="libx264" if output_format in ["mp4", "mkv"] else "libxvid")

        messagebox.showinfo("Conversão Completa", f"Arquivo convertido para {output_format} com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    finally:
        progress_bar.stop()  # Para a barra de progresso

# Função para selecionar o arquivo de entrada
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Todos os arquivos de vídeo", "*.mp4 *.mkv *.avi")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

# Função para definir o nome e formato do arquivo de saída
def save_file():
    output_path = filedialog.asksaveasfilename(defaultextension=f".{format_var.get()}", filetypes=[("Arquivo de Vídeo", f"*.{format_var.get()}")])
    if output_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_path)

# Função que inicia a conversão em uma nova thread
def start_conversion():
    input_file = input_entry.get()
    output_file = output_entry.get()
    output_format = format_var.get()

    if input_file and output_file and output_format:
        # Verifica se os caminhos de arquivo são válidos
        if not os.path.isfile(input_file):
            messagebox.showerror("Erro", "Arquivo de entrada não encontrado.")
            return
        # Inicia a conversão em uma thread separada para não travar a interface
        conversion_thread = threading.Thread(target=convert_video, args=(input_file, output_file, output_format))
        conversion_thread.start()
    else:
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")

# Configurações da interface gráfica
root = tk.Tk()
root.title("Conversor de Vídeo")
root.geometry("500x500")
root.configure(bg="#2C3E50")

# Estilo personalizado
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#2C3E50", foreground="white", font=("Helvetica", 10))
style.configure("TButton", background="#34495E", foreground="white", font=("Helvetica", 10, "bold"), relief="flat")
style.map("TButton", background=[("active", "#2980B9")])
style.configure("TProgressbar", troughcolor="#34495E", background="#2980B9", thickness=5)

# Frames para organizar melhor os elementos
input_frame = tk.Frame(root, bg="#2C3E50")
input_frame.pack(pady=10)

output_frame = tk.Frame(root, bg="#2C3E50")
output_frame.pack(pady=10)

format_frame = tk.Frame(root, bg="#2C3E50")
format_frame.pack(pady=10)

# Elementos de entrada
ttk.Label(input_frame, text="Arquivo de Entrada:").pack(anchor="w")
input_entry = ttk.Entry(input_frame, width=45)
input_entry.pack(side="left", padx=5, pady=5)
ttk.Button(input_frame, text="Selecionar Arquivo", command=select_file).pack(side="right", padx=5)

# Elementos de saída
ttk.Label(output_frame, text="Arquivo de Saída:").pack(anchor="w")
output_entry = ttk.Entry(output_frame, width=45)
output_entry.pack(side="left", padx=5, pady=5)
ttk.Button(output_frame, text="Salvar Como", command=save_file).pack(side="right", padx=5)

# Seletor de formato
ttk.Label(format_frame, text="Formato de Saída:").pack(anchor="w")
format_var = tk.StringVar(value="mp4")
format_options = ["mp3", "mp4", "avi", "mkv"]
ttk.OptionMenu(format_frame, format_var, *format_options).pack(pady=5)

# Barra de progresso
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate", style="TProgressbar")
progress_bar.pack(pady=10)

# Botão de Conversão
ttk.Button(root, text="Converter", command=start_conversion).pack(pady=20)

root.mainloop()
