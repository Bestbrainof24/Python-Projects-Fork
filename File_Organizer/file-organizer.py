from pathlib import Path
import shutil

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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
            # A dictionary takes file extensions & folder to move each formats to. 
            destination_mapping = {
                # Key = Format/extension to handle : Value = Folder to move file format. 
                ".zip": r"C:\Users\Precious pc\Documents\Zip files",
                ".png": r"C:\Users\Precious pc\Documents\png_files",
                ".psd": r"C:\Users\Precious pc\Documents\psd_destination",
                ".pdf": r"C:\Users\Precious pc\Documents\pdf_files",
            }
            # Default destination for unknown extensions
            other_files = r"C:\Users\Precious pc\Documents\other_files"
            # Get the destination directory for the file extension or use the default
            destination = destination_mapping.get(file_extension, other_files)
            # Move the file to the determined destination
            # Check if file already exists in destination & delete it. 
            if Path.exists(Path(destination).joinpath(file_name)):
                print(f"File {file_name} already exists in the destination. Deleting it.")
                Path.unlink(Path(destination).joinpath(file_name))
            # Move the file to the determined destination
            shutil.move(file_path, destination)

if __name__ == "__main__":
    folder_to_watch = r"C:\Users\Precious pc\Documents\monitor"  # Replace with the directory you want to monitor
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
