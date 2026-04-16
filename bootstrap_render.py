import json
import os
import zipfile


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def ensure_connected_export_ready():
    manifest_path = os.path.join(BASE_DIR, "deploy_manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as input_file:
        manifest = json.load(input_file)

    marker_path = os.path.join(BASE_DIR, *manifest["extractMarker"].split("/"))
    if os.path.isfile(marker_path):
        return manifest

    archive_path = os.path.join(BASE_DIR, manifest["archiveName"])
    if not os.path.isfile(archive_path):
        with open(archive_path, "wb") as archive_file:
            for part_name in manifest["archiveParts"]:
                with open(os.path.join(BASE_DIR, "bundle", part_name), "rb") as part_file:
                    archive_file.write(part_file.read())

    with zipfile.ZipFile(archive_path, "r") as zip_file:
        zip_file.extractall(BASE_DIR)

    return manifest


if __name__ == "__main__":
    state = ensure_connected_export_ready()
    print(f"Prepared connected export for site {state['siteId']}")
