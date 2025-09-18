"""
scene_composer.py
Multi-scene story composer - generates sets of prompts for narratives,
scenarios, comics with the same character in different situations.
"""

import customtkinter as ctk
import random
from datetime import datetime

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
    'text': ('Consolas', 11)
}

class SceneComposer:
    def __init__(self, prompt_generator):
        self.prompt_gen = prompt_generator
        self.current_story = []
        
        # Story templates
        self.story_templates = {
            "Romantic Evening": [
                ("Scene 1: Arrival", "getting ready, bedroom, soft lighting"),
                ("Scene 2: Dinner", "restaurant, candlelight, intimate conversation"),
                ("Scene 3: Dance", "dancing, close embrace, romantic mood"),
                ("Scene 4: Passion", "kissing, bedroom, passionate embrace"),
                ("Scene 5: Climax", "intimate moment, ecstasy, satisfaction")
            ],
            "Beach Day": [
                ("Scene 1: Arrival", "beach, bikini, sun, walking on sand"),
                ("Scene 2: Swimming", "water, wet body, playful, splashing"),
                ("Scene 3: Sunbathing", "lying on towel, tan lines, relaxed"),
                ("Scene 4: Beach House", "shower, washing sand, intimate"),
                ("Scene 5: Sunset", "romantic sunset, nude, passionate")
            ],
            "Office Fantasy": [
                ("Scene 1: Work", "office, business attire, professional"),
                ("Scene 2: After Hours", "late night, empty office, tension"),
                ("Scene 3: Temptation", "desk, removing clothes, forbidden"),
                ("Scene 4: Passion", "office sex, risky, intense"),
                ("Scene 5: Satisfaction", "afterglow, disheveled, satisfied")
            ],
            "Gothic Romance": [
                ("Scene 1: Castle", "gothic setting, dark atmosphere, mysterious"),
                ("Scene 2: Seduction", "candlelit room, vampire theme, allure"),
                ("Scene 3: Transformation", "dark magic, supernatural, intense"),
                ("Scene 4: Dark Passion", "gothic sex, intense, dramatic"),
                ("Scene 5: Eternal Bond", "blood bond, supernatural climax, forever")
            ]
        }

    def view(self, parent):
        """Creates the Scene Composer view"""
        frame = ctk.CTkFrame(parent, fg_color=COLORS['bg_primary'])
        
        # Header
        ctk.CTkLabel(frame, text="🎬 Scene Composer", 
                    font=FONTS['header'], text_color=COLORS['accent_primary']).pack(pady=15)
        
        # Main container
        main_container = ctk.CTkFrame(frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left side - Story templates and controls
        left_frame = ctk.CTkFrame(main_container, fg_color=COLORS['bg_secondary'], width=350)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        
        ctk.CTkLabel(left_frame, text="Story Templates:", font=FONTS['label']).pack(pady=10)
        
        # Template selection
        self.template_var = ctk.StringVar(value="Romantic Evening")
        template_menu = ctk.CTkOptionMenu(left_frame, variable=self.template_var,
                                         values=list(self.story_templates.keys()),
                                         width=300, font=FONTS['label'])
        template_menu.pack(pady=10, padx=10)
        
        # Character settings
        char_frame = ctk.CTkFrame(left_frame, fg_color=COLORS['bg_tertiary'])
        char_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(char_frame, text="Character Settings:", font=FONTS['label']).pack(pady=10)
        
        # Subject type
        ctk.CTkLabel(char_frame, text="Subject:", font=FONTS['button']).pack()
        self.subject_var = ctk.StringVar(value="female")
        subject_menu = ctk.CTkOptionMenu(char_frame, variable=self.subject_var,
                                        values=["female", "male", "couple"],
                                        width=200)
        subject_menu.pack(pady=5)
        
        # Character style
        ctk.CTkLabel(char_frame, text="Character Style:", font=FONTS['button']).pack(pady=(10,0))
        self.charstyle_var = ctk.StringVar(value="goth")
        charstyle_menu = ctk.CTkOptionMenu(char_frame, variable=self.charstyle_var,
                                          values=["goth", "cyberpunk", "military", "pin-up", 
                                                 "retro", "magical girl", "vampire", "angel"],
                                          width=200)
        charstyle_menu.pack(pady=5)
        
        # Options
        options_frame = ctk.CTkFrame(char_frame, fg_color="transparent")
        options_frame.pack(pady=10)
        
        self.nudity_var = ctk.BooleanVar(value=True)
        nudity_cb = ctk.CTkCheckBox(options_frame, text="Nudity", 
                                   variable=self.nudity_var, font=FONTS['button'])
        nudity_cb.pack(pady=2)
        
        self.acts_var = ctk.BooleanVar(value=True)
        acts_cb = ctk.CTkCheckBox(options_frame, text="Sexual Acts", 
                                 variable=self.acts_var, font=FONTS['button'])
        acts_cb.pack(pady=2)
        
        # Generate button
        generate_btn = ctk.CTkButton(left_frame, text="🎬 Generate Story",
                                    fg_color=COLORS['accent_primary'],
                                    font=FONTS['button'], height=40,
                                    command=self.generate_story)
        generate_btn.pack(pady=20, padx=10)
        
        # Scene count
        scene_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        scene_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(scene_frame, text="Number of Scenes:", font=FONTS['button']).pack(side="left")
        self.scene_count_var = ctk.StringVar(value="5")
        scene_spin = ctk.CTkOptionMenu(scene_frame, variable=self.scene_count_var,
                                      values=["3", "4", "5", "6", "7", "8"],
                                      width=60)
        scene_spin.pack(side="right")
        
        # Right side - Generated story
        right_frame = ctk.CTkFrame(main_container, fg_color=COLORS['bg_secondary'])
        right_frame.pack(side="right", fill="both", expand=True)
        
        ctk.CTkLabel(right_frame, text="Generated Story:", font=FONTS['label']).pack(pady=10)
        
        # Story display
        self.story_display = ctk.CTkTextbox(right_frame, font=FONTS['text'])
        self.story_display.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Action buttons
        btn_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        copy_btn = ctk.CTkButton(btn_frame, text="📋 Copy",
                                fg_color=COLORS['accent_secondary'],
                                command=self.copy_story)
        copy_btn.pack(side="left", padx=5)
        
        save_btn = ctk.CTkButton(btn_frame, text="💾 Save",
                                fg_color=COLORS['accent_primary'],
                                command=self.save_story)
        save_btn.pack(side="left", padx=5)
        
        clear_btn = ctk.CTkButton(btn_frame, text="🗑️ Clear",
                                 fg_color="#DC2626",
                                 command=self.clear_story)
        clear_btn.pack(side="left", padx=5)
        
        return frame
    
    def generate_story(self):
        """Generates a story consisting of multiple scenes"""
        template_name = self.template_var.get()
        template = self.story_templates[template_name]
        scene_count = int(self.scene_count_var.get())
        
        # Generate scenes
        self.current_story = []
        story_text = f"=== {template_name.upper()} ===\n"
        story_text += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for i in range(min(scene_count, len(template))):
            scene_name, scene_hints = template[i]
            
            # Generate prompt for this scene
            pos, neg = self.prompt_gen.generate_single(
                subject=self.subject_var.get(),
                nudity=self.nudity_var.get(),
                acts=self.acts_var.get() and i >= 2,  # Acts only in later scenes
                artstyle="cinematic",
                charstyle=self.charstyle_var.get(),
                custom_intensity=1.0
            )
            
            # Add scene hints to prompt
            enhanced_prompt = f"{pos}\nBREAK\n{scene_hints}"
            
            self.current_story.append({
                'scene': scene_name,
                'positive': enhanced_prompt,
                'negative': neg
            })
            
            story_text += f"{scene_name}\n{'-'*50}\n"
            story_text += f"POSITIVE:\n{enhanced_prompt}\n\n"
            story_text += f"NEGATIVE:\n{neg}\n\n"
            story_text += "="*80 + "\n\n"
        
        # Display story
        self.story_display.delete("0.0", "end")
        self.story_display.insert("0.0", story_text)
    
    def copy_story(self):
        """Copies the story to the clipboard"""
        import pyperclip
        content = self.story_display.get("0.0", "end").strip()
        if content:
            pyperclip.copy(content)
            print("Story copied to clipboard!")
    
    def save_story(self):
        """Saves the story to a file"""
        content = self.story_display.get("0.0", "end").strip()
        if content:
            filename = f"story_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Story saved to {filename}")
    
    def clear_story(self):
        """Clears the displayed story"""
        self.story_display.delete("0.0", "end")
        self.current_story = []