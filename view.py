import tkinter as tk
from tkinter import scrolledtext
from analizadorLexico import LexerAnalyzer 

class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("Lexer Analyzer")

        font_style = ("Consolas", 12, "normal")
        background_color = "#1e1e1e"
        foreground_color = "#d4d4d4"

        # Configuración de frames
        self.left_frame = tk.Frame(master)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.right_frame = tk.Frame(master)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.lexer_analyzer = LexerAnalyzer()

        # Configuración del área de texto de entrada
        self.input_text = scrolledtext.ScrolledText(self.left_frame, wrap=tk.WORD, width=60, height=20, font=font_style)
        self.input_text.pack(pady=10)
        self.input_text.config(bg=background_color, fg=foreground_color, insertbackground=foreground_color)

        # Botón para analizar
        self.analyze_button = tk.Button(self.left_frame, text="Analyze", command=self.analyze)
        self.analyze_button.pack(pady=5)

        # Área para mostrar resultados del análisis
        self.result_text = scrolledtext.ScrolledText(self.left_frame, wrap=tk.WORD, width=60, height=10, font=font_style)
        self.result_text.pack(pady=10)
        self.result_text.config(bg=background_color, fg=foreground_color, state='disabled')
        self.result_text.tag_config('error', foreground='red')
        self.result_text.tag_config('correct', foreground='#32CD32')  # Light green

        # Área para mostrar el valor de las variables, en el lado derecho
        self.vars_text = scrolledtext.ScrolledText(self.right_frame, wrap=tk.WORD, width=30, height=40, font=font_style)
        self.vars_text.pack(pady=10)
        self.vars_text.config(bg=background_color, fg=foreground_color, state='disabled')

    def analyze(self):
        data = self.input_text.get("1.0", tk.END)
        lex_results = self.lexer_analyzer.analyze(data)
        
        # Limpiar resultados previos y salidas
        self.result_text.configure(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.vars_text.configure(state='normal')
        self.vars_text.delete('1.0', tk.END)
        
        # Asegurarse de que imp_outputs está limpio al inicio del análisis
        self.lexer_analyzer.imp_outputs.clear()

        success, parse_result_or_errors = self.lexer_analyzer.parse(data)

        if success:
            self.result_text.insert(tk.END, "Syntax Analysis Complete: No Errors\n", 'correct')
        else:
            for error in parse_result_or_errors:
                self.result_text.insert(tk.END, error + '\n', 'error')
                
        self.result_text.insert(tk.END, "Token List:\n")
        for token in lex_results:
            self.result_text.insert(tk.END, f"{token}\n")
            
        self.result_text.configure(state='disabled')
        
        # Actualizar y mostrar salidas de imp en el lado derecho
        for output in self.lexer_analyzer.imp_outputs:
            self.vars_text.insert(tk.END, f"{output}\n")
        self.vars_text.configure(state='disabled')



        
        
        

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()