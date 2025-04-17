import tkinter as tk
from tkinter import scrolledtext
import re

# Token and Semantic Analyzer — same as before
token_specification = [
    ("TYPE",    r'\bint\b|\bfloat\b|\bstring\b'),
    ("ID",      r'[a-zA-Z_]\w*'),
    ("ASSIGN",  r'='),
    ("NUMBER",  r'\d+(\.\d+)?'),
    ("STRING",  r'"[^"]*"'),
    ("PLUS",    r'\+'),
    ("SEMI",    r';'),
    ("SKIP",    r'[ \t]+'),
    ("NEWLINE", r'\n'),
    ("MISMATCH",r'.'),
]
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

def tokenize(code):
    tokens = []
    line_num = 1
    for mo in re.finditer(token_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == "NEWLINE":
            line_num += 1
        elif kind == "SKIP":
            continue
        elif kind == "MISMATCH":
            raise RuntimeError(f"Unexpected token: {value} on line {line_num}")
        else:
            tokens.append((line_num, kind, value))
    return tokens

def get_literal_type(value):
    if re.match(r'^\d+$', value): return 'int'
    if re.match(r'^\d+\.\d+$', value): return 'float'
    if re.match(r'^".*"$', value): return 'string'
    return None

def full_semantic_analysis(code):
    try:
        tokens = tokenize(code)
    except RuntimeError as e:
        return [str(e)]

    symbol_table = {}
    i = 0
    output = []

    while i < len(tokens):
        line, kind, value = tokens[i]

        if kind == "TYPE":
            var_type = value
            i += 1
            if i < len(tokens) and tokens[i][1] == "ID":
                var_name = tokens[i][2]
                if var_name in symbol_table:
                    output.append(f"Line {line}: ❌ Redeclaration of '{var_name}'")
                else:
                    symbol_table[var_name] = var_type
                    output.append(f"Line {line}: ✅ Declared '{var_name}' as {var_type}")
                i += 1
            if i < len(tokens) and tokens[i][1] == "SEMI":
                i += 1
            continue

        elif kind == "ID":
            var_name = value
            if var_name not in symbol_table:
                output.append(f"Line {line}: ❌ Undeclared variable '{var_name}'")
                while i < len(tokens) and tokens[i][1] != "SEMI": i += 1
                i += 1
                continue

            var_type = symbol_table[var_name]
            i += 1
            if i < len(tokens) and tokens[i][1] == "ASSIGN":
                i += 1
                expr_types = []
                while i < len(tokens) and tokens[i][1] != "SEMI":
                    token_type = tokens[i][1]
                    token_value = tokens[i][2]
                    if token_type == "ID":
                        if token_value not in symbol_table:
                            output.append(f"Line {line}: ❌ Undeclared variable '{token_value}' in expression")
                            expr_types.append("unknown")
                        else:
                            expr_types.append(symbol_table[token_value])
                    elif token_type in ["NUMBER", "STRING"]:
                        expr_types.append(get_literal_type(token_value))
                    i += 1
                i += 1  # skip semicolon

                expr_result = ("string" if "string" in expr_types else
                               "float" if "float" in expr_types else
                               "int" if "int" in expr_types else
                               "unknown")

                if var_type != expr_result:
                    output.append(f"Line {line}: ❌ Type mismatch assigning to '{var_name}' (expected {var_type}, got {expr_result})")
                else:
                    output.append(f"Line {line}: ✅ Assigned to '{var_name}'")

    return output

# ============== GUI ==============

class SemanticSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Semantic Analyzer Simulator")

        # Input
        tk.Label(root, text="Enter Code:").pack(anchor="w", padx=10)
        self.code_input = scrolledtext.ScrolledText(root, width=70, height=15, font=("Courier", 11))
        self.code_input.pack(padx=10, pady=5)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="▶ Full Analyze", command=self.full_analyze, bg="#4CAF50", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="⏭ Step Through", command=self.step_through, bg="#2196F3", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="🔄 Reset", command=self.reset, bg="#f44336", fg="white").pack(side="left", padx=5)

        # Output
        tk.Label(root, text="Output:").pack(anchor="w", padx=10)
        self.output_box = scrolledtext.ScrolledText(root, width=70, height=12, font=("Courier", 11), state="disabled")
        self.output_box.pack(padx=10, pady=5)

        self.analysis_results = []
        self.step_index = 0

    def full_analyze(self):
        code = self.code_input.get("1.0", tk.END)
        self.analysis_results = full_semantic_analysis(code)
        self.show_output(self.analysis_results)

    def step_through(self):
        if not self.analysis_results:
            code = self.code_input.get("1.0", tk.END)
            self.analysis_results = full_semantic_analysis(code)
            self.step_index = 0
            self.output_box.config(state="normal")
            self.output_box.delete("1.0", tk.END)

        if self.step_index < len(self.analysis_results):
            self.output_box.config(state="normal")
            self.output_box.insert(tk.END, self.analysis_results[self.step_index] + "\n")
            self.output_box.config(state="disabled")
            self.step_index += 1

    def reset(self):
        self.analysis_results = []
        self.step_index = 0
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.config(state="disabled")

    def show_output(self, lines):
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", tk.END)
        for line in lines:
            self.output_box.insert(tk.END, line + "\n")
        self.output_box.config(state="disabled")

# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = SemanticSimulator(root)
    root.mainloop()
