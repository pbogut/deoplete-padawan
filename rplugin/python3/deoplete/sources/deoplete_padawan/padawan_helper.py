# =============================================================================
# FILE: padawan_helper.py
# AUTHOR: Pawel Bogut
# =============================================================================
from os import path


class Helper:

    def get_project_root(self, file_path):
        current_path = path.dirname(file_path)
        while current_path != '/' and not path.exists(
            path.join(current_path, 'composer.json')
        ):
            current_path = path.dirname(current_path)

        if current_path == '/':
            current_path = path.dirname(file_path)

        return current_path
