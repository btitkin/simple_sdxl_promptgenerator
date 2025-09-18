import random

class PromptGenerator:

    def __init__(self, tags_db):
        self.tags_db = tags_db
        self.history = set()

    def generate_single(self, subject, nudity, acts, artstyle, charstyle,
                        custom_intensity=1.0, scene_type="single", roleplays=None):
        # Helpers
        def safe_sample(lst, n):
            return random.sample(lst, min(len(lst), n)) if lst else []

        def unique(seq):
            seen = set()
            out = []
            for x in seq:
                if x not in seen and x:
                    out.append(x)
                    seen.add(x)
            return out

        def split_lighting(effects):
            env_keys = {"golden hour", "blue hour", "candle", "ambient", "natural", "window"}
            tech_keys = {"rim", "back", "flash", "spot", "gel"}
            env, tech = [], []
            for e in effects or []:
                s = e.lower()
                if any(k in s for k in env_keys) or "hour" in s:
                    env.append(e)
                elif any(k in s for k in tech_keys):
                    tech.append(e)
                elif "lighting" in s:
                    env.append(e)
                else:
                    env.append(e)
            return env, tech

        roleplays = roleplays or []

        # Pools
        quality = self.tags_db.quality_tags or []
        technical = self.tags_db.technical_styles or []
        body_types = self.tags_db.body_types or []
        hair_styles = self.tags_db.hair_styles or []
        lingerie = (self.tags_db.clothing_lingerie or [])
        revealing = (self.tags_db.clothing_revealing or [])
        nude_pool = (self.tags_db.clothing_nude or [])
        intimate = (self.tags_db.intimate_details or [])
        poses = self.tags_db.poses or []
        exprs = self.tags_db.expressions or []
        locations = self.tags_db.locations or []
        all_light = self.tags_db.lighting_effects or []
        env_light, tech_light = split_lighting(all_light)
        rare = self.tags_db.rare_effects or []
        negatives = self.tags_db.negative_prompts or []
        acts_pool = getattr(self.tags_db, "sexual_acts", []) or []

        # Roleplay mapping (safe, adult)
        rp_map = {
            "Dom/Sub": "dominant/submissive dynamic",
            "Professor/Student (adult roleplay)": "professor/student roleplay (adult)",
            "Boss/Employee": "office power dynamic",
            "Friends": "friends with benefits",
            "Childhood Friends": "childhood friends reunion",
            "Roommates": "roommates scenario",
            "Neighbors": "neighbors romance",
            "Bodyguard/Client": "bodyguard and client",
            "Nurse/Patient (adult)": "nurse/patient roleplay (adult)"
        }

        rp_tags = [rp_map[r] for r in roleplays if r in rp_map]

        # Scene type phrase
        scene_map = {
            "single": "solo portrait",
            "couple": "intimate duo",
            "threesome": "threesome composition",
            "group": "group scene"
        }

        scene_phrase = scene_map.get((scene_type or "single").lower(), "solo portrait")

        # Subject/character label
        subjects = self.tags_db.get_subjects(subject) if hasattr(self.tags_db, "get_subjects") else []

        if subject in ("female", "male", "couple"):
            subj = random.choice(subjects) if subjects else subject
        else:
            # For extended subjects, use the label directly
            subj = subject.replace("/", " ").replace("-", " ").strip()

        # Filter sexual acts by subject
        acts_subject_map = {
            "female": [act for act in acts_pool if "female" in act or "woman" in act or "girl" in act],
            "male": [act for act in acts_pool if "male" in act or "man" in act or "boy" in act],
            "couple": acts_pool,
        }

        filtered_acts_pool = acts_subject_map.get(subject, acts_pool)

        # Sections (content only, no labels)

        # 0: IMAGE QUALITY / META-TAGS
        section1 = unique(safe_sample(quality, 3) + safe_sample(technical, 2))

        # 1: MAIN SUBJECT (character) + scene phrase
        section2 = unique([f"{subj}, {charstyle}", scene_phrase])

        # 2: BODY FEATURES
        section3 = unique(safe_sample(body_types, 4) + safe_sample(hair_styles, 1))

        # 3: CLOTHING / NUDITY
        if nudity:
            section4 = unique(safe_sample(nude_pool, 1) + safe_sample(intimate, 2))
        else:
            clothing_pool = lingerie + revealing
            section4 = unique(safe_sample(clothing_pool, 3))

        # 4: POSE / ACTION (+ roleplay context)
        section5 = unique(
            safe_sample(poses, 2) +
            safe_sample(exprs, 1) +
            (safe_sample(filtered_acts_pool, 1) if acts else []) +
            rp_tags
        )

        # 5: SCENE / ENVIRONMENT
        section6 = unique(safe_sample(locations, 2) + safe_sample(env_light, 2))

        # 6: PHOTOGRAPHIC STYLE / TECHNIQUE
        section7 = unique(
            [artstyle, "photorealistic", "realistic skin texture"] +
            safe_sample(tech_light, 2) +
            safe_sample(technical, 1)
        )

        # 7: POST-PROCESSING / FINAL MOOD
        section8 = unique(safe_sample(rare, 2)) if random.random() < 0.6 * custom_intensity else []

        ordered = [section1, section2, section3, section4, section5, section6, section7, section8]
        sections = [", ".join(s) for s in ordered if s]

        positive_prompt = "\nBREAK\n".join(sections)

        negative_prompt = ", ".join(safe_sample(negatives, 12)) or "low quality, blurry, bad anatomy, deformed"

        pid = hash(positive_prompt)

        if pid in self.history:
            random.shuffle(sections)
            positive_prompt = "\nBREAK\n".join(sections)

        self.history.add(pid)

        return positive_prompt, negative_prompt

    # Enhance (bez zmian względem ostatniej stabilnej wersji)
    def enhance_prompt(self, positive_text: str, focus: str = "auto", intensity: int = 2) -> str:
        def to_sections(txt: str):
            parts = [p.strip() for p in txt.split("\nBREAK\n")]
            return [p for p in parts if p]

        def from_sections(sections):
            return "\nBREAK\n".join([s for s in sections if s and s.strip()])

        def add_terms_allow_repeats(section: str, additions: list):
            exist = [t.strip() for t in section.split(",") if t.strip()]
            exist.extend(additions)
            return ", ".join(exist)

        # Pools for enhance (as previously implemented)

        face_pool = [
            "symmetrical face", "defined jawline", "high cheekbones", "smooth complexion",
            "subtle blush", "glossy lips", "full lips", "cat eyeliner", "long eyelashes",
            "neatly groomed eyebrows", "beauty mark", "freckled cheeks"
        ]

        body_pool = [
            "soft skin texture", "natural skin pores", "defined collarbones",
            "toned midriff", "subtle muscle definition", "hourglass silhouette",
            "elegant posture", "graceful hands", "natural skin sheen"
        ]

        clothing_enrich = [
            "delicate lace details", "intricate strapwork", "sheer fabric texture",
            "subtle fabric wrinkles", "matching accessories", "minimal jewelry",
            "pearlescent accents", "polished high heels"
        ]

        pose_enrich = [
            "subtle weight shift", "contrapposto stance", "gentle hip tilt",
            "soft hand gesture", "chin tilt", "shoulder drop", "elegant posture"
        ]

        scene_pool = [
            "depth cues", "foreground bokeh", "soft haze", "subtle dust motes",
            "reflections on surfaces", "rich ambient detail", "textured backdrop"
        ]

        light_pool = [
            "gentle backlight", "soft rim light", "practical lights in frame",
            "light falloff on background", "subtle color gel accents"
        ]

        post_enrich = [
            "cinematic color grading", "fine film grain", "gentle bloom",
            "balanced sharpening", "micro-contrast", "soft vignetting"
        ]

        comp_pool = [
            "rule of thirds", "leading lines", "balanced framing",
            "subject separation", "shallow depth of field"
        ]

        sections = to_sections(positive_text)

        # Index map: 0 quality, 1 subject, 2 body, 3 clothing, 4 pose, 5 scene, 6 photo/tech, 7 post
        idx_subject = 1 if len(sections) > 1 else None
        idx_body = 2 if len(sections) > 2 else None
        idx_cloth = 3 if len(sections) > 3 else None
        idx_pose = 4 if len(sections) > 4 else None
        idx_scene = 5 if len(sections) > 5 else None
        idx_light = 6 if len(sections) > 6 else None
        idx_post = 7 if len(sections) > 7 else None

        if focus == "auto":
            targets = [
                ("subject", idx_subject, face_pool),
                ("body", idx_body, body_pool),
                ("clothes", idx_cloth, clothing_enrich),
                ("pose", idx_pose, pose_enrich),
                ("scene", idx_scene, scene_pool),
                ("light", idx_light, light_pool),
                ("post", idx_post, post_enrich),
            ]
        elif focus == "face":
            targets = [("subject", idx_subject, face_pool)]
        elif focus == "body":
            targets = [("body", idx_body, body_pool)]
        elif focus == "scene":
            targets = [("scene", idx_scene, scene_pool)]
        elif focus == "lighting":
            targets = [("light", idx_light, light_pool)]
        elif focus == "composition":
            targets = [("photo", idx_light, comp_pool)]
        elif focus == "clothing":
            targets = [("clothes", idx_cloth, clothing_enrich)]
        elif focus == "pose":
            targets = [("pose", idx_pose, pose_enrich)]
        elif focus == "post":
            targets = [("post", idx_post, post_enrich)]
        else:
            targets = [("body", idx_body, body_pool)]

        add_n = 2 if intensity <= 1 else 3 if intensity == 2 else 4

        for _, idx, pool in targets:
            if idx is None or idx >= len(sections) or not pool:
                continue
            additions = random.sample(pool, add_n) if len(pool) >= add_n else [random.choice(pool) for _ in range(add_n)]
            sections[idx] = add_terms_allow_repeats(sections[idx], additions)

        return from_sections(sections)

    def generate_multiple(self, count=5, **kwargs):
        return [
            (f"=== PROMPT {i+1} ===", *self.generate_single(**kwargs))
            for i in range(count)
        ]
