import os
import customtkinter as ctk

from tags_db import TagsDB
from prompt_generator import PromptGenerator
from prompt_generator_ui import PromptGeneratorUI
from preset_manager import PresetManager
from playground import Playground
from scene_composer import SceneComposer
from export_manager import ExportManager
from reference_panel import ReferencePanel

# Poprawne ustawienia ciemnego trybu i tematu
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        os.chdir(os.path.dirname(__file__))

        self.title("Ultra Detailed NSFW SDXL Suite")
        self.geometry("1024x768")
        self.minsize(1024, 768)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tags_db = TagsDB()
        self.prompt_gen = PromptGenerator(self.tags_db)
        self.preset_mgr = PresetManager(self.tags_db)
        self.prompt_ui = PromptGeneratorUI(self.prompt_gen)
        self.playground = Playground(self.prompt_gen)
        self.scene_composer = SceneComposer(self.prompt_gen)
        self.export_mgr = ExportManager(
    get_generator_text=lambda: self.prompt_ui.prompt_box.get("0.0","end").strip()
)
        self.reference_panel = ReferencePanel()

        nav = ctk.CTkFrame(self, fg_color="#0B1020")
        nav.grid(row=0, column=0, sticky="ew", pady=8, padx=8)
        buttons = [
            ("Generator", self.show_generator),
            ("Presets", self.show_presets),
            ("Playground", self.show_playground),
            ("Scene Composer", self.show_scene_composer),
            ("References", self.show_reference),
            ("Export", self.show_export),
        ]
        for label, cmd in buttons:
            ctk.CTkButton(nav, text=label, command=cmd,
                          fg_color="#3B4261", hover_color="#5962A0", text_color="#E0E1E5").pack(side="left", padx=5)

        container = ctk.CTkFrame(self, fg_color="#0B1020", corner_radius=12)
        container.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for view in [
            self.prompt_ui.view,
            self.preset_mgr.view,
            self.playground.view,
            self.scene_composer.view,
            self.reference_panel.view,
            self.export_mgr.view,
        ]:
            frame = view(container)
            self.frames[view] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_generator()

    def show_generator(self):
        self.frames[self.prompt_ui.view].tkraise()

    def show_presets(self):
        self.frames[self.preset_mgr.view].tkraise()

    def show_playground(self):
        self.frames[self.playground.view].tkraise()

    def show_scene_composer(self):
        self.frames[self.scene_composer.view].tkraise()

    def show_reference(self):
        self.frames[self.reference_panel.view].tkraise()

    def show_export(self):
        self.frames[self.export_mgr.view].tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
