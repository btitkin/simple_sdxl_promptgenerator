'''
preset_manager.py
Manages styles, scenes, characters, and predefined configuration settings.
Allows saving, loading, editing, and deleting presets.
'''

import customtkinter as ctk
import json
import os
from tkinter import messagebox

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
    'button': ('Segoe UI', 14, 'bold')
}

class PresetManager:
    def __init__(self, tags_db):
        self.tags_db = tags_db
        self.presets_file = "presets.json"
        self.presets = self.load_presets()

    def load_presets(self):
        """Loads presets from a JSON file"""
        if os.path.exists(self.presets_file):
            try:
                with open(self.presets_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_presets(self):
        """Saves presets to a JSON file"""
        try:
            with open(self.presets_file, 'w', encoding='utf-8') as f:
                json.dump(self.presets, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot save presets: {e}")

    def create_preset(self, name, config):
        """Creates a new preset"""
        self.presets[name] = config
        self.save_presets()

    def delete_preset(self, name):
        """Deletes a preset"""
        if name in self.presets:
            del self.presets[name]
            self.save_presets()

    def view(self, parent):
        """Creates the preset management view"""
        frame = ctk.CTkFrame(parent, fg_color=COLORS['bg_primary'])
        
        # Header
        ctk.CTkLabel(frame, text="🎯 Preset Manager", 
                    font=FONTS['header'], text_color=COLORS['accent_primary']).pack(pady=20)
        
        # Preset list
        preset_frame = ctk.CTkFrame(frame, fg_color=COLORS['bg_secondary'])
        preset_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(preset_frame, text="Saved Presets:", font=FONTS['label']).pack(pady=10)
        
        # Scrollable preset list
        preset_scroll = ctk.CTkScrollableFrame(preset_frame, height=300)
        preset_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        for preset_name in self.presets:
            preset_item = ctk.CTkFrame(preset_scroll, fg_color=COLORS['bg_tertiary'])
            preset_item.pack(fill="x", pady=5)
            
            ctk.CTkLabel(preset_item, text=preset_name, font=FONTS['label']).pack(side="left", padx=10)
            
            load_btn = ctk.CTkButton(preset_item, text="Load", width=80,
                                    fg_color=COLORS['accent_primary'])
            load_btn.pack(side="right", padx=5, pady=5)
            
            del_btn = ctk.CTkButton(preset_item, text="Delete", width=80,
                                   fg_color="#DC2626")
            del_btn.pack(side="right", padx=5, pady=5)
        
        # New preset section
        new_preset_frame = ctk.CTkFrame(frame, fg_color=COLORS['bg_secondary'])
        new_preset_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(new_preset_frame, text="Create New Preset:", font=FONTS['label']).pack(pady=10)
        
        entry_frame = ctk.CTkFrame(new_preset_frame, fg_color="transparent")
        entry_frame.pack(pady=10)
        
        ctk.CTkLabel(entry_frame, text="Name:", font=FONTS['label']).pack(side="left")
        name_entry = ctk.CTkEntry(entry_frame, width=200)
        name_entry.pack(side="left", padx=10)
        
        save_btn = ctk.CTkButton(entry_frame, text="Save Current Settings",
                                fg_color=COLORS['accent_secondary'])
        save_btn.pack(side="left", padx=10)
        
        return frame