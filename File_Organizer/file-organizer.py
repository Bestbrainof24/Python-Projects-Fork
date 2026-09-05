from pathlib import Path
import shutil

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CURRENT_WORKING_DIR = Path.cwd()
FILE_TYPES: dict[str, list[str]] = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "videos": [".mp4", ".mkv", ".avi", ".mov"],
    "audio": [".mp3", ".wav", ".flac", ".m4a"],
    "documents": [".pdf", ".docx", ".txt"],
    "archives": [".zip", ".rar", ".7z"],
}

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = Path(event.src_path)
            file_name = file_path.name
            file_extension = file_path.suffix.lower()
            category = ""

            for category_name, extensions in FILE_TYPES.items():
                if file_extension in extensions:
                    category = category_name
                    break
            else:
                category = "others"

            destination_mapping = {
                "images": CURRENT_WORKING_DIR / "Images",
                "videos": CURRENT_WORKING_DIR / "Videos",
                "audio": CURRENT_WORKING_DIR / "Audio Files",
                "documents": CURRENT_WORKING_DIR / "Documents",
                "archives": CURRENT_WORKING_DIR / "Archives",
                "others": CURRENT_WORKING_DIR / "Others"
            }
            
            destination = destination_mapping[category]
            # Move the file to the determined destination
            # Check if file already exists in destination & delete it. 
            if Path(destination).joinpath(file_name).exists():
                print(f"File {file_name} already exists in the destination. Deleting it.")
                Path(destination).joinpath(file_name).unlink()
            # Move the file to the determined destination
            shutil.move(file_path, destination)

if __name__ == "__main__":
    folder_to_watch = CURRENT_WORKING_DIR / "monitor"
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=folder_to_watch, recursive=False)  # Set recursive to True if you want to monitor subdirectories
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
