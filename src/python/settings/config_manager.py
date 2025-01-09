import configparser
import os

class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        if os.path.exists(config_file):
            with open(config_file, "r", encoding="utf-8") as file:
                self.config.read_file(file)
        self.theme = self.get_theme()

    def get(self, section, key, fallback=None):
        return self.config.get(section, key, fallback=fallback)

    def set(self, section, key, value):
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = str(value)
        self._save_config()

    def _save_config(self):
        with open(self.config_file, "w", encoding="utf-8") as file:
            self.config.write(file)

    def reload_config(self):
        self.config.read(self.config_file, encoding='utf-8')

    @property
    def translations(self):
        language = self.get("General", "language", "en")
        section = f"Translations_{language}"
        if section not in self.config:
            raise ValueError(f"Translations for language '{language}' not found in configuration.")
        return {key: value for key, value in self.config[section].items()}

    @property
    def screen_width(self):
        return int(self.get("General", "screen_width", 800))

    @property
    def screen_height(self):
        return int(self.get("General", "screen_height", 600))

    def get_theme(self):
        return self.get("General", "theme", "light")

    def set_theme(self, theme):
        self.set("General", "theme", theme)

    def set_language(self, language):
        self.set("General", "language", language)

    def set_screen_size(self, width, height):
        self.set("General", "screen_width", width)
        self.set("General", "screen_height", height)