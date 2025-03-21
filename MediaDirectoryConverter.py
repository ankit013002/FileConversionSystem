import os
import json
from datetime import datetime
from pillow_heif import register_heif_opener
from PIL import Image
from colorama import init, Fore, Style

init()

success_count = 0
warning_count = 0
error_count = 0

register_heif_opener()

folder_path = input(
    "Please enter your directory to declutter and convert files (HEIC -> JPG): ")
debug_enabled_user_input = ""
while debug_enabled_user_input not in ("y", "n"):
    debug_enabled_user_input = input("Would you like to enable debug? (y/n)")

debug_enabled = debug_enabled_user_input == "y"

for filename in os.listdir(folder_path):
    if filename.lower().endswith(".jpg"):
        json_path = os.path.join(
            folder_path, filename + ".supplemental-metadata.json")

        if os.path.exists(json_path):
            try:
                os.remove(json_path)
                debug_enabled and print(
                    f"Deleted metadata {os.path.basename(json_path)}" + Style.RESET_ALL)
                success_count += 1
            except Exception as e:
                debug_enabled and print(
                    Fore.RED + f"ERROR: Failed to delete metadata {os.path.basename(json_path)}: {e}" + Style.RESET_ALL)
                error_count += 1

    if filename.lower().endswith(".heic"):
        base_name = os.path.splitext(filename)[0]
        heic_path = os.path.join(folder_path, filename)
        json_path = os.path.join(
            folder_path, base_name + ".HEIC.supplemental-metadata.json")

        new_filename = base_name + ".jpg"

        if os.path.exists(json_path):
            try:
                with open(json_path, "r") as f:
                    metadata = json.load(f)

                timestamp = metadata.get("photoTakenTime", {}).get("timestamp")

                if timestamp:
                    dt = datetime.fromtimestamp(int(timestamp))
                    new_filename = dt.strftime("%Y%m%d_%H%M%S") + ".jpg"
            except Exception as e:
                debug_enabled and print(
                    Fore.YELLOW + f"WARNING: Could not read metadata for {filename}: {e}" + Style.RESET_ALL)
                warning_count += 1

        jpg_path = os.path.join(folder_path, new_filename)

        try:
            with Image.open(heic_path) as img:
                img.convert("RGB").save(jpg_path, "JPEG")
            debug_enabled and print(
                Fore.GREEN + f"SUCCESS: Converted {filename} → {new_filename}" + Style.RESET_ALL)

            os.remove(heic_path)
            debug_enabled and print(f"Deleted {filename}" + Style.RESET_ALL)

            if os.path.exists(json_path):
                os.remove(json_path)
                debug_enabled and print(
                    f"Deleted metadata {os.path.basename(json_path)}" + Style.RESET_ALL)
            success_count += 1

        except Exception as e:
            debug_enabled and print(
                Fore.RED + f"ERROR: Failed to convert {filename}: {e}" + Style.RESET_ALL)
            error_count += 1

print(Fore.GREEN + f"Successful conversions: {success_count}")
print(Fore.YELLOW + f"Warnings during conversion: {warning_count}")
print(Fore.RED + f"Errors during conversion: {error_count}")
