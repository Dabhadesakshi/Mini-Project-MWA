import tkinter as tk
from tkinter import scrolledtext
import re

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

def semantic_analyzer(code):
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
                i += 1

                expr_result = ("string" if "string" in expr_types else
                               "float" if "float" in expr_types else
                               "int" if "int" in expr_types else
                               "unknown")

                if var_type != expr_result:
                    output.append(f"Line {line}: ❌ Type mismatch assigning to '{var_name}' (expected {var_type}, got {expr_result})")
                else:
                    output.append(f"Line {line}: ✅ Assigned to '{var_name}'")

    return output


def run_analysis():
    code = code_input.get("1.0", tk.END)
    results = semantic_analyzer(code)
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    for res in results:
        output_box.insert(tk.END, res + "\n")
    output_box.config(state="disabled")

root = tk.Tk()
root.title("Mini Semantic Analyzer")

tk.Label(root, text="Enter your code:").pack(anchor="w", padx=10)
code_input = scrolledtext.ScrolledText(root, width=70, height=15, font=("Courier", 11))
code_input.pack(padx=10, pady=5)

tk.Button(root, text="Run Semantic Analysis", command=run_analysis, bg="#4CAF50", fg="white", font=("Arial", 10)).pack(pady=10)

tk.Label(root, text="Output:").pack(anchor="w", padx=10)
output_box = scrolledtext.ScrolledText(root, width=70, height=12, font=("Courier", 11), state="disabled")
output_box.pack(padx=10, pady=5)

root.mainloop()
