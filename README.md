# Ultra Detailed NSFW SDXL Prompt Suite

### Project Description

[cite_start]This is a modular generator for creating ultra-detailed NSFW prompts for Stable Diffusion XL (SDXL)[cite: 470]. [cite_start]The application includes a CustomTkinter user interface and a robust prompt generation engine[cite: 471]. [cite_start]The suite provides a comprehensive set of tools for prompt creation and management, including a Preset Manager, Playground, Scene Composer, Export Manager, and Reference Panel[cite: 471]. [cite_start]The launcher automates the installation and startup process[cite: 471].

### Requirements

* Python 3.8+
* `customtkinter`
* `pyperclip`
* (Optional) Discord/webhook client, SDXL backend, and JSON tag files

### Installation

1.  Clone or unzip the project into a local folder.
2.  [cite_start]Run `launcher.bat` to automatically install the required dependencies (`customtkinter` and `pyperclip`)[cite: 471].
3.  [cite_start]The launcher will then start the main application (`main.py`)[cite: 471].

### Package Structure

* `main.py`: The primary user interface and application routing.
* `prompt_generator.py`: The core engine for prompt generation.
* `tags_db.py`: Handles loading the tag database.
* [cite_start]`tags_db.json`: A comprehensive database of NSFW tags, with over 100 entries per category[cite: 471].
* `preset_manager.py`: Manages the saving and loading of presets.
* `playground.py`: A prompt builder and editor for manual tag mixing.
* `scene_composer.py`: Used for creating multi-scene narratives and sequences.
* `export_manager.py`: Provides utilities for exporting, copying to clipboard, and sharing prompts.
* `reference_panel.py`: A panel for browsing example prompts and image references.
* `launcher.bat`: A batch script for project setup and launch.
* `resources/`: An optional directory for additional resources, galleries, and presets.

### Usage

1.  [cite_start]Select a module from the interface: Generator, Presets, Playground, Scene Composer, Reference, or Export[cite: 473].
2.  [cite_start]In the Generator module, configure options for style, subject, character, nudity, and acts[cite: 473].
3.  [cite_start]Click the **Generate** button to create a prompt[cite: 473].
4.  [cite_start]Copy the generated prompt to the clipboard or export it as a `.txt` or `.json` file[cite: 473].
5.  [cite_start]Use the Playground to manually edit prompts and mix tags[cite: 473].
6.  [cite_start]The Scene Composer allows for creating sets of prompts for multi-scene narratives[cite: 473].
7.  [cite_start]The Reference panel contains example prompts and image references[cite: 473].

### Future Development

* [cite_start]Direct integration with Stable Diffusion XL for immediate image generation[cite: 474].
* [cite_start]REST API for external prompt generation requests[cite: 474].
* [cite_start]Discord and Telegram bot interfaces to facilitate prompt sharing[cite: 474].
* [cite_start]UI improvements, including a real-time usage statistics dashboard[cite: 474].
* [cite_start]Functionality to export and import tag packs and presets as `.zip` archives[cite: 474].

### Support and Issues

[cite_start]For any questions, bug reports, or feature requests, please contact `support@example.com`[cite: 475].