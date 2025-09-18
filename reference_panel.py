"""
reference_panel.py
Reference and inspiration panel. Displays example prompt+image thumbnails from a local directory or URL.
"""

import customtkinter as ctk
import os
from PIL import Image, ImageTk

COLORS = {
    'bg_primary': '#0F0F23',
    'bg_secondary': '#1A1A35',
    'bg_tertiary': '#2D2D4A',
    'accent_primary': '#6366F1',
    'text_primary': '#F8FAFC',
}

FONTS = {
    'header': ('Segoe UI', 20, 'bold'),
    'label': ('Segoe UI', 14),
}

class ReferencePanel:
    def __init__(self):
        # path to the directory with reference prompts + images
        self.ref_dir = os.path.join(os.path.dirname(__file__), 'resources', 'references')
        self.refs = self.load_references()

    def load_references(self):
        refs = []
        if os.path.isdir(self.ref_dir):
            for fname in os.listdir(self.ref_dir):
                if fname.lower().endswith(('.png','.jpg','.jpeg')):
                    prompt_name = os.path.splitext(fname)[0] + '.txt'
                    prompt_path = os.path.join(self.ref_dir, prompt_name)
                    if os.path.exists(prompt_path):
                        with open(prompt_path, 'r', encoding='utf-8') as f:
                            prompt = f.read().strip()
                        refs.append((prompt, os.path.join(self.ref_dir, fname)))
        return refs

    def view(self, parent):
        frame = ctk.CTkFrame(parent, fg_color=COLORS['bg_primary'])
        ctk.CTkLabel(frame, text="📚 Inspiration Library", font=FONTS['header'], text_color=COLORS['accent_primary']).pack(pady=15)
        
        scroll = ctk.CTkScrollableFrame(frame, fg_color=COLORS['bg_secondary'])
        scroll.pack(fill="both", expand=True, padx=20, pady=10)

        for prompt, img_path in self.refs:
            item = ctk.CTkFrame(scroll, fg_color=COLORS['bg_tertiary'], corner_radius=6)
            item.pack(fill="x", pady=10, padx=10)
            
            # Load thumbnail
            try:
                img = Image.open(img_path).resize((128,128))
                tkimg = ImageTk.PhotoImage(img)
                panel = ctk.CTkLabel(item, image=tkimg)
                panel.image = tkimg
                panel.pack(side="left", padx=10, pady=10)
            except:
                pass
            
            text_frame = ctk.CTkFrame(item, fg_color="transparent")
            text_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            ctk.CTkLabel(text_frame, text=prompt, font=FONTS['label'], wraplength=600, justify="left").pack()

        return frame