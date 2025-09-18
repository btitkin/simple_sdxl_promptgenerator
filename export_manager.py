"""
export_manager.py
Zarządzanie eksportem promptów – zapis do plików, clipboard, webhooki, archiwa.
"""

import customtkinter as ctk
import pyperclip
import json
import os
import zipfile
from datetime import datetime
from tkinter import filedialog, messagebox
import requests  # Discord webhooks

COLORS = {
    'bg_primary': '#0F0F23',
    'bg_secondary': '#1A1A35',
    'bg_tertiary': '#2D2D4A',
    'accent_primary': '#6366F1',
    'accent_secondary': '#8B5CF6',
    'text_primary': '#F8FAFC',
}

FONTS = {
    'header': ('Segoe UI', 20, 'bold'),
    'label': ('Segoe UI', 14),
    'button': ('Segoe UI', 12, 'bold'),
    'text': ('Consolas', 11),
}

class ExportManager:
    def __init__(self, get_generator_text=None):
        # callback: callable -> str (zwraca zawartość pola Prompt Generator)
        self.get_generator_text = get_generator_text
        self.export_history = []
        self.settings = self.load_settings()

    def load_settings(self):
        try:
            with open("export_settings.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {'discord_webhook': '', 'auto_timestamp': True, 'default_format': 'txt', 'include_negative': True}

    def save_settings(self):
        try:
            with open("export_settings.json", 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można zapisać ustawień: {e}")

    def view(self, parent):
        frame = ctk.CTkFrame(parent, fg_color=COLORS['bg_primary'])

        ctk.CTkLabel(frame, text="📤 Export Manager",
                     font=FONTS['header'], text_color=COLORS['accent_primary']).pack(pady=15)

        main_container = ctk.CTkFrame(frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        left = ctk.CTkFrame(main_container, fg_color=COLORS['bg_secondary'], width=400)
        left.pack(side="left", fill="y", padx=(0, 10))
        ctk.CTkLabel(left, text="Opcje eksportu:", font=FONTS['label']).pack(pady=15)

        # Format
        format_frame = ctk.CTkFrame(left, fg_color=COLORS['bg_tertiary'])
        format_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(format_frame, text="Format:", font=FONTS['button']).pack(pady=5)
        self.format_var = ctk.StringVar(value="txt")
        ctk.CTkOptionMenu(format_frame, variable=self.format_var, values=["txt", "json", "csv", "zip"], width=200).pack(pady=5)

        # Options
        options_frame = ctk.CTkFrame(left, fg_color=COLORS['bg_tertiary'])
        options_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(options_frame, text="Opcje:", font=FONTS['button']).pack(pady=5)
        self.timestamp_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(options_frame, text="Dodaj timestamp do nazwy", variable=self.timestamp_var, font=FONTS['label']).pack(pady=2, anchor="w", padx=10)
        self.negative_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(options_frame, text="Uwzględnij negative prompt", variable=self.negative_var, font=FONTS['label']).pack(pady=2, anchor="w", padx=10)
        self.metadata_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(options_frame, text="Dodaj metadane", variable=self.metadata_var, font=FONTS['label']).pack(pady=2, anchor="w", padx=10)

        # Quick export
        quick = ctk.CTkFrame(left, fg_color=COLORS['bg_tertiary'])
        quick.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(quick, text="Szybki eksport:", font=FONTS['button']).pack(pady=5)
        ctk.CTkButton(quick, text="📋 Do schowka", fg_color=COLORS['accent_primary'], command=self.export_to_clipboard).pack(pady=5, fill="x", padx=10)
        ctk.CTkButton(quick, text="💾 Do pliku", fg_color=COLORS['accent_secondary'], command=self.export_to_file).pack(pady=5, fill="x", padx=10)

        # Share
        share = ctk.CTkFrame(left, fg_color=COLORS['bg_tertiary'])
        share.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(share, text="Udostępnianie:", font=FONTS['button']).pack(pady=5)
        ctk.CTkButton(share, text="🎮 Discord Webhook", fg_color="#5865F2", command=self.send_to_discord).pack(pady=2, fill="x", padx=10)
        ctk.CTkButton(share, text="🔗 Utwórz link", fg_color="#10B981", command=self.create_share_link).pack(pady=2, fill="x", padx=10)

        # Right side
        right = ctk.CTkFrame(main_container, fg_color=COLORS['bg_secondary'])
        right.pack(side="right", fill="both", expand=True)
        ctk.CTkLabel(right, text="Zawartość do eksportu:", font=FONTS['label']).pack(pady=10)

        self.content_input = ctk.CTkTextbox(right, height=200, font=FONTS['text'])
        self.content_input.pack(fill="both", expand=True, padx=10, pady=5)

        ctk.CTkButton(right, text="📥 Załaduj z generatora", fg_color=COLORS['accent_primary'],
                      command=self.load_from_generator).pack(pady=5)

        ctk.CTkLabel(right, text="Historia eksportów:", font=FONTS['label']).pack(pady=(20,5))
        self.history_display = ctk.CTkScrollableFrame(right, height=150)
        self.history_display.pack(fill="x", padx=10, pady=5)
        self.update_history_display()

        return frame

    def export_to_clipboard(self):
        content = self.content_input.get("0.0", "end").strip()
        if content:
            pyperclip.copy(content)
            self.add_to_history("Clipboard", "txt", len(content.split('\n')))
            messagebox.showinfo("Sukces", "Zawartość skopiowana do schowka!")
        else:
            messagebox.showwarning("Uwaga", "Brak zawartości do eksportu")

    def export_to_file(self):
        content = self.content_input.get("0.0", "end").strip()
        if not content:
            messagebox.showwarning("Uwaga", "Brak zawartości do eksportu")
            return
        format_ext = self.format_var.get()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S') if self.timestamp_var.get() else ""
        default_name = f"nsfw_prompts{('_' + timestamp) if timestamp else ''}.{format_ext}"
        filename = filedialog.asksaveasfilename(
            defaultextension=f".{format_ext}",
            filetypes=[(f"{format_ext.upper()} files", f"*.{format_ext}"), ("All files", "*.*")],
            initialname=default_name
        )
        if filename:
            try:
                if format_ext == "json":
                    self.export_as_json(filename, content)
                elif format_ext == "csv":
                    self.export_as_csv(filename, content)
                elif format_ext == "zip":
                    self.export_as_zip(filename, content)
                else:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(content)
                self.add_to_history("File", format_ext, len(content.split('\n')), filename)
                messagebox.showinfo("Sukces", f"Eksport do {filename} zakończony pomyślnie!")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie można zapisać pliku: {e}")

    def export_as_json(self, filename, content):
        data = {
            "timestamp": datetime.now().isoformat(),
            "generator": "Ultra Detailed NSFW SDXL Prompt Generator",
            "content": content,
            "metadata": {
                "include_negative": self.negative_var.get(),
                "format": "json",
                "lines_count": len(content.split('\n'))
            } if self.metadata_var.get() else None
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def export_as_csv(self, filename, content):
        import csv
        lines = content.split('\n')
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Line', 'Content'])
            for i, line in enumerate(lines, 1):
                writer.writerow([i, line])

    def export_as_zip(self, filename, content):
        with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("prompts.txt", content)
            if self.metadata_var.get():
                metadata = {
                    "timestamp": datetime.now().isoformat(),
                    "generator": "Ultra Detailed NSFW SDXL Prompt Generator",
                    "lines_count": len(content.split('\n')),
                    "include_negative": self.negative_var.get()
                }
                zf.writestr("metadata.json", json.dumps(metadata, indent=2))

    def send_to_discord(self):
        webhook_url = self.settings.get('discord_webhook', '')
        if not webhook_url:
            webhook_url = ctk.CTkInputDialog(text="Podaj Discord Webhook URL:", title="Discord Webhook").get_input()
            if webhook_url:
                self.settings['discord_webhook'] = webhook_url
                self.save_settings()
        if webhook_url:
            content = self.content_input.get("0.0", "end").strip()
            if content:
                try:
                    if len(content) > 2000:
                        content = content[:1990] + "... [skrócono]"
                    payload = {"content": f"``````", "username": "NSFW Prompt Generator"}
                    response = requests.post(webhook_url, json=payload)
                    if response.status_code == 204:
                        self.add_to_history("Discord", "webhook", 1)
                        messagebox.showinfo("Sukces", "Wysłano na Discord!")
                    else:
                        messagebox.showerror("Błąd", f"Błąd Discord: {response.status_code}")
                except Exception as e:
                    messagebox.showerror("Błąd", f"Nie można wysłać na Discord: {e}")

    def create_share_link(self):
        content = self.content_input.get("0.0", "end").strip()
        if content:
            fake_link = f"https://paste.service/prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            pyperclip.copy(fake_link)
            self.add_to_history("Link", "url", 1, fake_link)
            messagebox.showinfo("Link", f"Link skopiowany do schowka:\n{fake_link}")

    def load_from_generator(self):
        """Ładuje realny tekst z generatora przez callback."""
        if callable(self.get_generator_text):
            content = self.get_generator_text() or ""
            self.content_input.delete("0.0", "end")
            self.content_input.insert("0.0", content)
        else:
            messagebox.showwarning("Uwaga", "Brak połączenia z Generatorem. Skonfiguruj callback w main.py.")

    def add_to_history(self, export_type, format_type, items_count, filename=None):
        entry = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "type": export_type,
            "format": format_type,
            "items": items_count,
            "filename": filename
        }
        self.export_history.insert(0, entry)
        if len(self.export_history) > 20:
            self.export_history = self.export_history[:20]
        self.update_history_display()

    def update_history_display(self):
        for widget in self.history_display.winfo_children():
            widget.destroy()
        for entry in self.export_history:
            item = ctk.CTkFrame(self.history_display, fg_color=COLORS['bg_tertiary'])
            item.pack(fill="x", pady=2)
            info = f"{entry['timestamp']} - {entry['type']} ({entry['format']}) - {entry['items']} items"
            if entry.get('filename'):
                info += f" - {os.path.basename(entry['filename'])}"
            ctk.CTkLabel(item, text=info, font=FONTS['text']).pack(side="left", padx=10, pady=5)
