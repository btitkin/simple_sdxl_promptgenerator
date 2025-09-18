# Ultra Detailed NSFW SDXL Prompt Suite

### Project Description

This is a modular generator for creating ultra-detailed NSFW prompts for Stable Diffusion XL (SDXL). The application includes a CustomTkinter user interface and a robust prompt generation engine. The suite provides a comprehensive set of tools for prompt creation and management, including a Preset Manager, Playground, Scene Composer, Export Manager, and Reference Panel. The launcher automates the installation and startup process.

### Requirements

* Python 3.8+
* `customtkinter`
* `pyperclip`
* (Optional) Discord/webhook client, SDXL backend, and JSON tag files

### Installation

1.  Clone or unzip the project into a local folder.
2.  Run `launcher.bat` to automatically install the required dependencies (`customtkinter` and `pyperclip`).
3.  The launcher will then start the main application (`main.py`).

### Package Structure

* `main.py`: The primary user interface and application routing.
* `prompt_generator.py`: The core engine for prompt generation.
* `tags_db.py`: Handles loading the tag database.
* `tags_db.json`: A comprehensive database of NSFW tags, with over 100 entries per category.
* `preset_manager.py`: Manages the saving and loading of presets.
* `playground.py`: A prompt builder and editor for manual tag mixing.
* `scene_composer.py`: Used for creating multi-scene narratives and sequences.
* `export_manager.py`: Provides utilities for exporting, copying to clipboard, and sharing prompts.
* `reference_panel.py`: A panel for browsing example prompts and image references.
* `launcher.bat`: A batch script for project setup and launch.
* `resources/`: An optional directory for additional resources, galleries, and presets.

### Usage

1.  Select a module from the interface: Generator, Presets, Playground, Scene Composer, Reference, or Export.
2.  In the Generator module, configure options for style, subject, character, nudity, and acts.
3.  Click the **Generate** button to create a prompt.
4.  Copy the generated prompt to the clipboard or export it as a `.txt` or `.json` file.
5.  Use the Playground to manually edit prompts and mix tags.
6.  The Scene Composer allows for creating sets of prompts for multi-scene narratives.
7.  The Reference panel contains example prompts and image references.

### Future Development

* Direct integration with Stable Diffusion XL for immediate image generation.
* REST API for external prompt generation requests.
* Discord and Telegram bot interfaces to facilitate prompt sharing.
* UI improvements, including a real-time usage statistics dashboard.
* Functionality to export and import tag packs and presets as `.zip` archives.

### Support and Issues

For any questions, bug reports, or feature requests, please contact `support@example.com`.
