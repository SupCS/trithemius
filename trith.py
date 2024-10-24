import tkinter as tk
from tkinter import messagebox, filedialog

class TritemiusCipher:
    def __init__(self, alphabet='абвгґдеєжзийіїклмнопрстуфхцчшщьюя'):
        self.alphabet_lower = alphabet
        self.alphabet_upper = alphabet.upper()
        self.alphabet_size = len(alphabet)

    def set_alphabet(self, alphabet):
        self.alphabet_lower = alphabet
        self.alphabet_upper = alphabet.upper()
        self.alphabet_size = len(alphabet)

    def validate_text(self, text):
        for char in text:
            if char.isalpha() and char not in self.alphabet_lower + self.alphabet_upper:
                raise ValueError("Текст містить недопустимі символи.")
        return text

    def linear_shift(self, position, A, B):
        return (A * position + B) % self.alphabet_size

    def nonlinear_shift(self, position, A, B, C):
        return (A * position**2 + B * position + C) % self.alphabet_size

    def keyword_shift(self, position, keyword):
        keyword = keyword.lower()
        return self.alphabet_lower.index(keyword[position % len(keyword)])

    def encrypt(self, text, method, key_params):
        text = self.validate_text(text)
        encrypted_text = ''
        for i, char in enumerate(text):
            if char in self.alphabet_lower:
                shift = self.calculate_shift(i, method, key_params)
                index = (self.alphabet_lower.index(char) + shift) % self.alphabet_size
                encrypted_text += self.alphabet_lower[index]
            elif char in self.alphabet_upper:
                shift = self.calculate_shift(i, method, key_params)
                index = (self.alphabet_upper.index(char) + shift) % self.alphabet_size
                encrypted_text += self.alphabet_upper[index]
            else:
                encrypted_text += char
        return encrypted_text

    def decrypt(self, text, method, key_params):
        text = self.validate_text(text)
        decrypted_text = ''
        for i, char in enumerate(text):
            if char in self.alphabet_lower:
                shift = self.calculate_shift(i, method, key_params)
                index = (self.alphabet_lower.index(char) - shift) % self.alphabet_size
                decrypted_text += self.alphabet_lower[index]
            elif char in self.alphabet_upper:
                shift = self.calculate_shift(i, method, key_params)
                index = (self.alphabet_upper.index(char) - shift) % self.alphabet_size
                decrypted_text += self.alphabet_upper[index]
            else:
                decrypted_text += char
        return decrypted_text

    def calculate_shift(self, position, method, key_params):
        if method == 'linear':
            A, B = key_params
            return self.linear_shift(position, A, B)
        elif method == 'nonlinear':
            A, B, C = key_params
            return self.nonlinear_shift(position, A, B, C)
        elif method == 'keyword':
            keyword = key_params[0]
            return self.keyword_shift(position, keyword)
        else:
            raise ValueError("Невідомий метод шифрування.")

class CryptoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Криптосистема на основі шифру Тритеміуса")
        self.root.geometry("700x700")
        self.root.configure(bg="#f0f0f0")

        self.tritemius_cipher_ua = TritemiusCipher()  # Український алфавіт
        self.tritemius_cipher_en = TritemiusCipher(alphabet='abcdefghijklmnopqrstuvwxyz')  # Англійський алфавіт

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Відкрити", command=self.open_file)
        file_menu.add_command(label="Зберегти", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Вийти", command=self.root.quit)

        text_frame = tk.Frame(self.root, pady=10, bg="#f0f0f0")
        text_frame.pack(fill="x")

        self.label = tk.Label(text_frame, text="Введіть текст для шифрування/розшифрування:",
                              font=("Arial", 12, "bold"), bg="#f0f0f0")
        self.label.pack(padx=20, pady=5)

        self.text_input = tk.Text(text_frame, height=5, width=70, borderwidth=2, relief="solid")
        self.text_input.pack(padx=10)

        method_frame = tk.Frame(self.root, pady=10, bg="#f0f0f0")
        method_frame.pack(fill="x")

        self.method_label = tk.Label(method_frame, text="Оберіть метод шифрування:", font=("Arial", 10), bg="#f0f0f0")
        self.method_label.pack(side="left", padx=10)

        self.method_var = tk.StringVar(value="linear")
        self.linear_method = tk.Radiobutton(method_frame, text="Лінійний", variable=self.method_var, value="linear", bg="#f0f0f0", command=self.show_key_inputs)
        self.nonlinear_method = tk.Radiobutton(method_frame, text="Нелінійний", variable=self.method_var, value="nonlinear", bg="#f0f0f0", command=self.show_key_inputs)
        self.keyword_method = tk.Radiobutton(method_frame, text="Гасло", variable=self.method_var, value="keyword", bg="#f0f0f0", command=self.show_key_inputs)
        self.linear_method.pack(side="left")
        self.nonlinear_method.pack(side="left")
        self.keyword_method.pack(side="left")

        language_frame = tk.Frame(self.root, pady=10, bg="#f0f0f0")
        language_frame.pack(fill="x")

        self.language_label = tk.Label(language_frame, text="Оберіть мову:", font=("Arial", 10), bg="#f0f0f0")
        self.language_label.pack(side="left", padx=10)

        self.language_var = tk.StringVar(value="ua")
        self.language_ua = tk.Radiobutton(language_frame, text="Українська", variable=self.language_var, value="ua", bg="#f0f0f0")
        self.language_en = tk.Radiobutton(language_frame, text="Англійська", variable=self.language_var, value="en", bg="#f0f0f0")
        self.language_ua.pack(side="left")
        self.language_en.pack(side="left")

        key_frame = tk.Frame(self.root, pady=10, bg="#f0f0f0")
        key_frame.pack(fill="x")

        self.key_label = tk.Label(key_frame, text="Введіть ключ шифрування:", font=("Arial", 10), bg="#f0f0f0")
        self.key_label.pack(side="left", padx=10)

        self.key_input_A = tk.Entry(key_frame, width=10, borderwidth=2, relief="solid")
        self.key_input_B = tk.Entry(key_frame, width=10, borderwidth=2, relief="solid")
        self.key_input_C = tk.Entry(key_frame, width=10, borderwidth=2, relief="solid")
        self.key_input_keyword = tk.Entry(key_frame, width=30, borderwidth=2, relief="solid")

        self.show_key_inputs()

        button_frame = tk.Frame(self.root, pady=10, bg="#f0f0f0")
        button_frame.pack(fill="x")

        self.encrypt_button = tk.Button(button_frame, text="Зашифрувати", width=15, bg="#4CAF50", fg="white",
                                        font=("Arial", 10, "bold"), command=self.encrypt_text)
        self.encrypt_button.pack(side="left", padx=10)

        self.decrypt_button = tk.Button(button_frame, text="Розшифрувати", width=15, bg="#2196F3", fg="white",
                                        font=("Arial", 10, "bold"), command=self.decrypt_text)
        self.decrypt_button.pack(side="left", padx=10)

        # Додаємо кнопку для інформації про автора
        self.about_button = tk.Button(button_frame, text="Про автора", width=15, bg="#9C27B0", fg="white",
                                      font=("Arial", 10, "bold"), command=self.show_about_info)
        self.about_button.pack(side="left", padx=10)

        result_frame = tk.Frame(self.root, pady=10, bg="#f0f0f0")
        result_frame.pack(fill="x")

        self.result_label = tk.Label(result_frame, text="Результат:", font=("Arial", 12, "bold"), bg="#f0f0f0")
        self.result_label.pack(anchor="w", padx=10)

        self.result_output = tk.Text(result_frame, height=10, width=70, borderwidth=2, relief="solid")
        self.result_output.pack(padx=10)

    def show_about_info(self):
        messagebox.showinfo("Про розробника", "Розробник: Дмитро Аспарян ТВ-11\nКриптосистема на основі шифру Тритеміуса")


    def show_key_inputs(self):
        method = self.method_var.get()
        self.key_input_A.pack_forget()
        self.key_input_B.pack_forget()
        self.key_input_C.pack_forget()
        self.key_input_keyword.pack_forget()

        if method == "linear":
            self.key_input_A.pack(side="left", padx=5)
            self.key_input_B.pack(side="left", padx=5)
        elif method == "nonlinear":
            self.key_input_A.pack(side="left", padx=5)
            self.key_input_B.pack(side="left", padx=5)
            self.key_input_C.pack(side="left", padx=5)
        elif method == "keyword":
            self.key_input_keyword.pack(side="left", padx=5)

    def parse_key(self):
        method = self.method_var.get()

        if method == "linear":
            try:
                A = int(self.key_input_A.get().strip())
                B = int(self.key_input_B.get().strip())
                return method, (A, B)
            except ValueError:
                raise ValueError("Невірний формат ключа для лінійного шифрування. Використовуйте два числа.")
        elif method == "nonlinear":
            try:
                A = int(self.key_input_A.get().strip())
                B = int(self.key_input_B.get().strip())
                C = int(self.key_input_C.get().strip())
                return method, (A, B, C)
            except ValueError:
                raise ValueError("Невірний формат ключа для нелінійного шифрування. Використовуйте три числа.")
        elif method == "keyword":
            keyword = self.key_input_keyword.get().strip()
            if not keyword:
                raise ValueError("Гасло не може бути порожнім.")
            return method, (keyword,)
        else:
            raise ValueError("Невідомий метод шифрування.")

    def encrypt_text(self):
        text = self.text_input.get("1.0", tk.END).strip()
        language = self.language_var.get()

        if language == "ua":
            cipher = self.tritemius_cipher_ua
        else:
            cipher = self.tritemius_cipher_en

        try:
            method, key_params = self.parse_key()
            encrypted_text = cipher.encrypt(text, method, key_params)
            self.result_output.delete("1.0", tk.END)
            self.result_output.insert(tk.END, encrypted_text)
        except ValueError as e:
            messagebox.showerror("Помилка", str(e))

    def decrypt_text(self):
        text = self.text_input.get("1.0", tk.END).strip()
        language = self.language_var.get()

        if language == "ua":
            cipher = self.tritemius_cipher_ua
        else:
            cipher = self.tritemius_cipher_en

        try:
            method, key_params = self.parse_key()
            decrypted_text = cipher.decrypt(text, method, key_params)
            self.result_output.delete("1.0", tk.END)
            self.result_output.insert(tk.END, decrypted_text)
        except ValueError as e:
            messagebox.showerror("Помилка", str(e))

    def save_file(self):
        content = self.result_output.get("1.0", tk.END).strip()
        if not content:
            messagebox.showerror("Помилка", "Немає тексту для збереження.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            messagebox.showinfo("Успіх", "Файл успішно збережено.")

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert(tk.END, content)

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoGUI(root)
    root.mainloop()
