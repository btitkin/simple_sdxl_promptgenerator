import customtkinter as ctk
import random
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
    'button': ('Segoe UI', 12, 'bold'),
    'text': ('Consolas', 12)
}

class Playground:
    def __init__(self, prompt_generator):
        self.prompt_gen = prompt_generator
        self.current_tags = {k: [] for k in [
            'quality', 'subject', 'body', 'clothing',
            'pose', 'location', 'lighting', 'effects'
        ]}

    def view(self, parent):
        frame = ctk.CTkFrame(parent, fg_color=COLORS['bg_primary'])
        ctk.CTkLabel(frame, text="🎨 Prompt Playground",
                     font=FONTS['header'], text_color=COLORS['accent_primary']).pack(pady=15)

        container = ctk.CTkFrame(frame, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=10)

        # Left side: category buttons
        left = ctk.CTkFrame(container, fg_color=COLORS['bg_secondary'], width=300)
        left.pack(side="left", fill="y", padx=(0,10))
        ctk.CTkLabel(left, text="Tag Categories:", font=FONTS['label']).pack(pady=10)

        categories = [
            ("Quality & Tech", "quality"),
            ("Subject & Character", "subject"),
            ("Body & Hair", "body"),
            ("Clothing / Nude", "clothing"),
            ("Pose / Action", "pose"),
            ("Scene / Environment", "location"),
            ("Lighting & Effects", "lighting"),
            ("Special Effects", "effects")
        ]
        for name, key in categories:
            row = ctk.CTkFrame(left, fg_color=COLORS['bg_tertiary'])
            row.pack(fill="x", pady=5, padx=10)
            ctk.CTkLabel(row, text=name, font=FONTS['label']).pack(side="left", padx=10)
            ctk.CTkButton(row, text="Add Random", width=100,
                          command=lambda k=key: self.add_random_tag(k)).pack(side="right", padx=5)

        # Right side: tags display and preview
        right = ctk.CTkFrame(container, fg_color=COLORS['bg_secondary'])
        right.pack(side="right", fill="both", expand=True)
        ctk.CTkLabel(right, text="Current Tags:", font=FONTS['label']).pack(pady=10)
        self.tags_display = ctk.CTkScrollableFrame(right, height=150)
        self.tags_display.pack(fill="x", padx=10)
        ctk.CTkLabel(right, text="Prompt Preview:", font=FONTS['label']).pack(pady=(20,5))
        self.prompt_preview = ctk.CTkTextbox(right, height=250, font=FONTS['text'])
        self.prompt_preview.pack(fill="both", expand=True, padx=10, pady=5)

        ctrl = ctk.CTkFrame(right, fg_color="transparent")
        ctrl.pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(ctrl, text="Refresh", fg_color=COLORS['accent_primary'],
                      command=self.update_preview).pack(side="left", padx=5)
        ctk.CTkButton(ctrl, text="Clear All", fg_color="#DC2626",
                      command=self.clear_all_tags).pack(side="left", padx=5)
        ctk.CTkButton(ctrl, text="Randomize All", fg_color=COLORS['accent_secondary'],
                      command=self.randomize_all).pack(side="left", padx=5)

        return frame

    def get_tags_for_category(self, category):
        db = self.prompt_gen.tags_db
        if category == "quality":
            return db.quality_tags
        if category == "subject":
            return db.get_subjects('female') + db.get_subjects('male') + db.get_subjects('couple')
        if category == "body":
            return db.body_types + db.hair_styles
        if category == "clothing":
            return db.clothing_lingerie + db.clothing_revealing + db.clothing_nude
        if category == "pose":
            return db.poses + db.expressions
        if category == "location":
            return db.locations
        if category == "lighting":
            return db.lighting_effects
        if category == "effects":
            return db.rare_effects
        return []

    def add_random_tag(self, category):
        tags = self.get_tags_for_category(category)
        if tags:
            tag = random.choice(tags)
            self.current_tags[category].append(tag)
        else:
            messagebox.showwarning("Warning", f"No tags available in {category}")
        self.render_tags()
        self.update_preview()

    def render_tags(self):
        for w in self.tags_display.winfo_children():
            w.destroy()
        for cat, tags in self.current_tags.items():
            if tags:
                frame = ctk.CTkFrame(self.tags_display, fg_color=COLORS['bg_tertiary'])
                frame.pack(fill="x", pady=2)
                ctk.CTkLabel(frame, text=f"{cat.title()}:", font=FONTS['label']).pack(anchor="w", padx=10)
                for t in tags:
                    row = ctk.CTkFrame(frame, fg_color=COLORS['accent_primary'])
                    row.pack(fill="x", padx=20, pady=2)
                    ctk.CTkLabel(row, text=t, font=FONTS['button']).pack(side="left", padx=10)
                    ctk.CTkButton(row, text="×", width=25, fg_color="#DC2626",
                                  command=lambda x=t, c=cat: self.remove_tag(c, x)).pack(side="right", padx=5)

    def remove_tag(self, category, tag):
        if tag in self.current_tags[category]:
            self.current_tags[category].remove(tag)
        self.render_tags()
        self.update_preview()

    def clear_all_tags(self):
        for k in self.current_tags:
            self.current_tags[k] = []
        self.render_tags()
        self.update_preview()

    def randomize_all(self):
        self.clear_all_tags()
        for cat in self.current_tags:
            tags = self.get_tags_for_category(cat)
            for _ in range(min(3, len(tags))):
                self.current_tags[cat].append(random.choice(tags))
        self.render_tags()
        self.update_preview()

    def update_preview(self):
        all_tags = sum(self.current_tags.values(), [])
        if all_tags:
            preview = "\nBREAK\n".join([", ".join(all_tags[i:i+5]) for i in range(0, len(all_tags), 5)])
        else:
            preview = "No tags selected."
        self.prompt_preview.delete("0.0", "end")
        self.prompt_preview.insert("0.0", preview)