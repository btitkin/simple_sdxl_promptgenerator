"""
tags_db.py

Topical tag databases for NSFW SDXL Prompt Generator.

Contains lists:
- quality_tags
- technical_styles
- subjects_female, subjects_male, subjects_couple
- character_styles
- body_types
- hair_styles
- clothing_lingerie, clothing_revealing, clothing_nude
- intimate_details
- poses
- expressions
- locations
- lighting_effects
- sexual_acts
- rare_effects
- negative_prompts
"""

class TagsDB:
    def __init__(self):
        # quality_tags and technical_styles are simplified: full databases moved to PromptGenerator
        self.quality_tags = []
        self.technical_styles = []
        self.subjects_female = []
        self.subjects_male = []
        self.subjects_couple = []
        self.character_styles = []
        self.body_types = []
        self.hair_styles = []
        self.clothing_lingerie = []
        self.clothing_revealing = []
        self.clothing_nude = []
        self.clothing_accessories = []
        self.intimate_details = []
        self.poses = []
        self.expressions = []
        self.locations = []
        self.lighting_effects = []
        self.sexual_acts = []
        self.bodily_fluids = []
        self.rare_effects = []
        self.fantasy_elements = []
        self.negative_prompts = []
        self.emotional_atmosphere = []
        self.scene_types = []
        self.roleplay_scenarios = []
        self.time_of_day = []
        self.props = []
        self.sensory_details = []
        self.narrative_elements = []
        self.hair_colors = []
        self.hair_styles_female = []
        self.hair_styles_male = []
        self.subjects_futanari = []
        self.subjects_femboy = []
        self.subjects_trans_female = []
        self.subjects_trans_male = []
        self.subjects_nonbinary_genderfluid = []
        self.subjects_anthro_furry = []
        self.subjects_monster_creature = []
        self.subjects_alien_scifi = []

        self.load_tags()

    def load_tags(self):
        import json, os
        path = os.path.join(os.path.dirname(__file__), 'tags_db.json')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.__dict__.update(data)
        else:
            raise FileNotFoundError(f"Missing tags_db.json file: {path}")

    def get_subjects(self, subject_type):
        if subject_type == 'female':
            return self.subjects_female
        elif subject_type == 'male':
            return self.subjects_male
        else:
            return self.subjects_couple
