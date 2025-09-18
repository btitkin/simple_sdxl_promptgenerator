import customtkinter as ctk
from PIL import Image

def make_linear_gradient(width, height, start_hex="#0B1020", end_hex="#0A2A46"):
    def hex_to_rgb(h):
        return tuple(int(h[i:i+2], 16) for i in (1, 3 ,5))
    s = hex_to_rgb(start_hex)
    e = hex_to_rgb(end_hex)
    img = Image.new("RGB", (width, height), s)
    for y in range(height):
        t = y / max(1, height - 1)
        r = int(s[0] + t * (e[0] - s[0]))
        g = int(s[1] + t * (e[1] - s[1]))
        b = int(s[2] + t * (e[2] - s[2]))
        for x in range(width):
            img.putpixel((x, y), (r, g, b))
    return img

class PromptGeneratorUI:
    def __init__(self, prompt_gen):
        self.prompt_gen = prompt_gen
        self.selected_roleplays = set()
        self.prompt_font_size = 14
        self._rp_collapsed = True
        self._hero_img = None
        self._hero_label = None

        self.colors = {
            "background": "#0B1020",
            "card_bg": "#1A1F38",
            "card_border": "#2A2F45",
            "button_bg": "#3B4261",
            "button_hover": "#5962A0",
            "button_red": "#DC2626",
            "text_header": "#E0E1E5",
            "text_normal": "#A7A9BE",
            "text_highlight": "#CFD1DC",
            "textbox_bg": "#1A1F38",
        }

    def _build_hero(self, parent):
        hero = ctk.CTkFrame(parent, fg_color=self.colors["background"])
        hero.grid_columnconfigure(0, weight=1)
        self._hero_label = ctk.CTkLabel(hero, text="")
        self._hero_label.grid(row=0, column=0, sticky="ew")

        # Teksty na banerze – Arial, uniwersalny font
        text_box = ctk.CTkFrame(hero, fg_color="transparent")
        text_box.grid(row=0, column=0, sticky="nw", padx=24, pady=18)
        ctk.CTkLabel(
            text_box,
            text="Ultra Detailed NSFW SDXL Prompt Suite",
            font=("Arial", 28, "bold"),
            text_color=self.colors["text_header"]
        ).pack(anchor="w")
        ctk.CTkLabel(
            text_box,
            text="Prepare professional prompts fast — with styles, scenes, and roleplay context.",
            font=("Arial", 12),
            text_color=self.colors["text_normal"]
        ).pack(anchor="w", pady=(4,0))

        def _on_resize(e):
            w = max(600, e.width)
            h = 140
            img = make_linear_gradient(w, h, "#0B1020", "#0A2A46")
            self._hero_img = ctk.CTkImage(light_image=img, dark_image=img, size=(w, h))
            self._hero_label.configure(image=self._hero_img)

        hero.bind("<Configure>", _on_resize)
        return hero

    def view(self, parent):
        root = ctk.CTkFrame(parent, fg_color=self.colors["background"])
        root.grid_rowconfigure(4, weight=1)
        root.grid_columnconfigure(0, weight=1)

        hero = self._build_hero(root)
        hero.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        card = ctk.CTkFrame(root, fg_color=self.colors["card_bg"], corner_radius=12,
                            border_color=self.colors["card_border"], border_width=1)
        card.grid(row=1, column=0, sticky="ew", padx=10, pady=6)
        for i in range(4):
            card.grid_columnconfigure(i, weight=1)

        # Art style
        self.artstyle = ctk.StringVar(value="Film Photography")
        art_styles = [
            "Film Photography","Digital Art","Anime","Realistic",
            "Amateur","Retro","Webcam","Spycam","CCTV","Smartphone","Polaroid",
            "Analog","Editorial","Portrait Studio","Street Photography","Fashion Editorial"
        ]
        ctk.CTkLabel(card, text="Art Style", text_color=self.colors["text_normal"]).grid(row=0, column=0, padx=8, pady=(8,2), sticky="w")
        ctk.CTkOptionMenu(card, values=art_styles, variable=self.artstyle).grid(row=1, column=0, padx=8, pady=(0,8), sticky="ew")

        # Subject
        self.subject = ctk.StringVar(value="Female")
        subjects = [
            "Female","Male","Couple",
            "Futanari","Trans-Female","Trans-Male","Femboy",
            "Non-binary / Genderfluid","Anthro / Furry","Monster / Creature","Alien / Sci-fi"
        ]
        ctk.CTkLabel(card, text="Subject", text_color=self.colors["text_normal"]).grid(row=0, column=1, padx=8, pady=(8,2), sticky="w")
        ctk.CTkOptionMenu(card, values=subjects, variable=self.subject).grid(row=1, column=1, padx=8, pady=(0,8), sticky="ew")

        # Character style
        self.charstyle = ctk.StringVar(value="Goth")
        char_list = self.prompt_gen.tags_db.character_styles or ["Goth"]
        ctk.CTkLabel(card, text="Character Style", text_color=self.colors["text_normal"]).grid(row=0, column=2, padx=8, pady=(8,2), sticky="w")
        ctk.CTkOptionMenu(card, values=char_list, variable=self.charstyle).grid(row=1, column=2, padx=8, pady=(0,8), sticky="ew")

        # Scene Type
        self.scene_type = ctk.StringVar(value="Single")
        scene_types = getattr(self.prompt_gen.tags_db, "scene_types", ["Single","Couple","Threesome","Group"])
        ctk.CTkLabel(card, text="Scene Type", text_color=self.colors["text_normal"]).grid(row=0, column=3, padx=8, pady=(8,2), sticky="w")
        ctk.CTkOptionMenu(card, values=scene_types, variable=self.scene_type).grid(row=1, column=3, padx=8, pady=(0,8), sticky="ew")

        # Roleplay (collapsible)
        rp_card = ctk.CTkFrame(root, fg_color=self.colors["card_bg"], corner_radius=12,
                               border_color=self.colors["card_border"], border_width=1)
        rp_card.grid(row=2, column=0, sticky="ew", padx=10, pady=6)
        rp_card.grid_columnconfigure(0, weight=1)

        self._rp_title = ctk.StringVar(value="Roleplay ▸")
        rp_header = ctk.CTkButton(rp_card, textvariable=self._rp_title,
                                  fg_color=self.colors["button_bg"],
                                  hover_color=self.colors["button_hover"],
                                  text_color=self.colors["text_header"],
                                  corner_radius=8, height=36, anchor="w",
                                  command=self._toggle_roleplay)
        rp_header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self._rp_content = ctk.CTkFrame(rp_card, fg_color=self.colors["background"])
        self._rp_content.grid_columnconfigure(0, weight=1)
        self._rp_content.grid_columnconfigure(1, weight=0)
        self._rp_content.grid_columnconfigure(2, weight=0)
        self._rp_content.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,10))

        rp_options = getattr(self.prompt_gen.tags_db, "roleplay_scenarios", [
            "Default","Dom/Sub","Professor/Student (adult roleplay)","Boss/Employee",
            "Friends","Childhood Friends","Roommates","Neighbors","Bodyguard/Client","Nurse/Patient (adult)"
        ])
        self.roleplay_var = ctk.StringVar(value="Default")
        ctk.CTkLabel(self._rp_content, text="Select", text_color=self.colors["text_normal"]).grid(row=0, column=0, sticky="w", padx=6, pady=6)
        ctk.CTkOptionMenu(self._rp_content, values=rp_options, variable=self.roleplay_var).grid(row=0, column=1, sticky="w", padx=6, pady=6)
        ctk.CTkButton(self._rp_content, text="Add", width=90, command=self._add_roleplay,
                      fg_color=self.colors["button_bg"], hover_color=self.colors["button_hover"],
                      text_color=self.colors["text_header"]).grid(row=0, column=2, sticky="w", padx=6, pady=6)
        ctk.CTkButton(self._rp_content, text="Clear", width=90, command=self._clear_roleplays,
                      fg_color=self.colors["button_red"], hover_color="#B02020",
                      text_color=self.colors["text_header"]).grid(row=0, column=3, sticky="w", padx=6, pady=6)

        self._rp_tags = ctk.CTkScrollableFrame(self._rp_content, fg_color=self.colors["background"], height=90)
        self._rp_tags.grid(row=1, column=0, columnspan=4, sticky="ew", padx=6, pady=6)
        self._rp_content.grid_remove()

        # Toggles
        toggles = ctk.CTkFrame(root, fg_color=self.colors["card_bg"], corner_radius=12,
                               border_color=self.colors["card_border"], border_width=1)
        toggles.grid(row=3, column=0, sticky="ew", padx=10, pady=6)
        toggles.grid_columnconfigure(0, weight=1)
        toggles.grid_columnconfigure(1, weight=1)

        self.nudity = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(toggles, text="Include nudity", variable=self.nudity,
                        text_color=self.colors["text_normal"]).grid(row=0, column=0, padx=10, pady=8, sticky="w")

        self.acts = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(toggles, text="Include sexual acts", variable=self.acts,
                        text_color=self.colors["text_normal"]).grid(row=0, column=1, padx=10, pady=8, sticky="w")

        # Prompt
        prompt_card = ctk.CTkFrame(root, fg_color=self.colors["card_bg"], corner_radius=12,
                                   border_color=self.colors["card_border"], border_width=1)
        prompt_card.grid(row=4, column=0, sticky="nsew", padx=10, pady=6)
        prompt_card.grid_rowconfigure(0, weight=1)
        prompt_card.grid_columnconfigure(0, weight=1)

        self.prompt_box = ctk.CTkTextbox(prompt_card,
                                         font=("Consolas", self.prompt_font_size),
                                         fg_color=self.colors["textbox_bg"],
                                         text_color=self.colors["text_highlight"])
        self.prompt_box.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Font size
        font_row = ctk.CTkFrame(root, fg_color=self.colors["background"])
        font_row.grid(row=5, column=0, sticky="ew", padx=10, pady=(0,6))
        ctk.CTkLabel(font_row, text="Font size", text_color=self.colors["text_normal"]).pack(side="left", padx=(0,8))
        self.font_size_var = ctk.IntVar(value=self.prompt_font_size)
        ctk.CTkSlider(font_row, from_=10, to=22, number_of_steps=12,
                      variable=self.font_size_var, command=self._apply_font_size).pack(side="left", fill="x", expand=True)

        # Footer
        footer = ctk.CTkFrame(root, fg_color=self.colors["background"])
        footer.grid(row=6, column=0, sticky="ew", padx=10, pady=(0,10))
        footer.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(footer, text="Enhance focus", text_color=self.colors["text_normal"]).grid(row=0, column=0, sticky="w")
        self.enhance_focus = ctk.StringVar(value="auto")
        ctk.CTkOptionMenu(footer,
                          values=["auto","face","body","clothing","pose","scene","lighting","composition","post"],
                          variable=self.enhance_focus).grid(row=0, column=1, padx=6, sticky="w")

        ctk.CTkLabel(footer, text="Intensity", text_color=self.colors["text_normal"]).grid(row=0, column=2, padx=6, sticky="w")
        self.enhance_intensity = ctk.StringVar(value="2")
        ctk.CTkOptionMenu(footer, values=["1","2","3"], variable=self.enhance_intensity).grid(row=0, column=3, padx=6, sticky="w")

        ctk.CTkButton(footer, text="Generate", fg_color=self.colors["button_bg"],
                      hover_color=self.colors["button_hover"],
                      text_color=self.colors["text_header"],
                      command=self.generate).grid(row=0, column=4, padx=(12,6), sticky="e")

        ctk.CTkButton(footer, text="Enhance", fg_color=self.colors["button_bg"],
                      hover_color=self.colors["button_hover"],
                      text_color=self.colors["text_header"],
                      command=self.enhance).grid(row=0, column=5, padx=(6,0), sticky="e")

        return root

    # Roleplay helpers
    def _toggle_roleplay(self):
        self._rp_collapsed = not self._rp_collapsed
        if self._rp_collapsed:
            self._rp_title.set("Roleplay ▸")
            self._rp_content.grid_remove()
        else:
            self._rp_title.set("Roleplay ▾")
            self._rp_content.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,10))

    def _render_roleplay_tags(self):
        for w in self._rp_tags.winfo_children():
            w.destroy()
        for tag in sorted(self.selected_roleplays):
            row = ctk.CTkFrame(self._rp_tags, fg_color="#17203a", corner_radius=8)
            row.pack(fill="x", padx=6, pady=3)
            ctk.CTkLabel(row, text=tag, text_color=self.colors["text_header"]).pack(side="left", padx=8, pady=4)
            ctk.CTkButton(row, text="×", width=26, fg_color=self.colors["button_red"], hover_color="#B02020",
                          text_color=self.colors["text_header"], command=lambda t=tag: self._remove_roleplay(t)).pack(side="right", padx=6, pady=4)

    def _add_roleplay(self):
        choice = self.roleplay_var.get()
        if choice == "Default":
            if not self.selected_roleplays:
                self.selected_roleplays.add(choice)
        else:
            if "Default" in self.selected_roleplays:
                self.selected_roleplays.remove("Default")
            self.selected_roleplays.add(choice)
        self._render_roleplay_tags()

    def _remove_roleplay(self, tag):
        if tag in self.selected_roleplays:
            self.selected_roleplays.remove(tag)
        self._render_roleplay_tags()

    def _clear_roleplays(self):
        self.selected_roleplays.clear()
        self._render_roleplay_tags()

    def _apply_font_size(self, _=None):
        self.prompt_font_size = int(self.font_size_var.get())
        self.prompt_box.configure(font=("Consolas", self.prompt_font_size))

    def _roleplay_list(self):
        if self.selected_roleplays and "Default" in self.selected_roleplays and len(self.selected_roleplays) > 1:
            return [t for t in self.selected_roleplays if t != "Default"]
        return list(self.selected_roleplays)

    def generate(self):
        pos, neg = self.prompt_gen.generate_single(
            subject=self.subject.get().lower(),
            nudity=self.nudity.get(),
            acts=self.acts.get(),
            artstyle=self.artstyle.get().lower(),
            charstyle=self.charstyle.get().lower(),
            scene_type=self.scene_type.get().lower(),
            roleplays=self._roleplay_list()
        )
        self.prompt_box.delete("0.0","end")
        self.prompt_box.insert("0.0", f"POSITIVE:\n{pos}\n\nNEGATIVE:\n{neg}")

    def enhance(self):
        text = self.prompt_box.get("0.0","end")
        pos, neg = "", ""
        if "NEGATIVE:" in text:
            parts = text.split("NEGATIVE:", 1)
            pos = parts[0].replace("POSITIVE:", "").strip()
            neg = parts[1].strip()
        else:
            pos = text.strip()

        focus = self.enhance_focus.get().lower()
        intensity = int(self.enhance_intensity.get())
        enhanced = self.prompt_gen.enhance_prompt(pos, focus=focus, intensity=intensity)

        out = f"POSITIVE:\n{enhanced}"
        if neg:
            out += f"\n\nNEGATIVE:\n{neg}"
        self.prompt_box.delete("0.0","end")
        self.prompt_box.insert("0.0", out)
