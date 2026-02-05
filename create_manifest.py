import os
import json
import hashlib

# Папка, где лежит готовая сборка программы
DIST_FOLDER = "./dist/main"
MANIFEST_FILE = "manifest.json"


def get_hash(filepath):
    """Считает хеш файла, чтобы понять, менялся ли он."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def create_manifest():
    manifest = {"files": {}}

    # Проходим по всем файлам в папке
    for root, _, files in os.walk(DIST_FOLDER):
        for filename in files:
            # Не включаем сам манифест в список
            if filename == MANIFEST_FILE:
                continue

            full_path = os.path.join(root, filename)
            # Получаем путь относительно папки dist (например, data/config.ini)
            rel_path = os.path.relpath(full_path, DIST_FOLDER).replace("\\", "/")

            manifest["files"][rel_path] = get_hash(full_path)

    # Сохраняем результат
    output_path = os.path.join(f"{DIST_FOLDER}/..", MANIFEST_FILE)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)

    print(f"Манифест создан: {output_path}")


if __name__ == "__main__":
    create_manifest()
