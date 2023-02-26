"""
Creating a Program to sort a folder on basis of file types 
Compressed: contains zip, rar type files
Images: contains images obviously
Videos: contains videos obvsly
Documents: Contains other document formats other than pdf like pptx xlsx docx
Executables: contains executable files like exe sh msi etc
Audio: contains audio files
Others: contains anything other than the above

BluePrint:
1. Scan the folder and check if it has the necessary folders if not then create them
2. create a sorting algorithm to sort the folder
3. use watchdogs to continuously monitor the folder for any changes
4. act on every change accordingly
"""

# Create folders for different file types if not already present

import os
Directory = "Directory/Path/to/sort"
folders = ["Compressed", "Images", "Videos", "PDFs", "Documents", "Executables", "Audio", "Others"]

Files = os.listdir(Directory)
for name in folders:
    if name not in Files:
        New_Directory = Directory+name
        os.mkdir(New_Directory)

# Sorting algorithm

def Sort():
    # Defining different file types

    File_Types = {
        "Images":[".tif",".tiff", ".bmp", ".jpg", ".jpeg", ".gif", ".png", ".eps", ".raw", ".cr2", ".nef", ".orf", ".sr2",
        ".avif", ".svg", ".webp", ".ico", ".cur", ".jfif", ".JPG"], 
        "Compressed":[".rar", ".pkg.tar.xz", ".gzip", ".tar.xz", ".7z", ".gza", ".zip", ".tar.gz", ".gz", ".tar"],
        "Videos":[".mkv", ".flv", "	.vob", ".mng", ".avi", ".wmv", ".mp4", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".webm"],
        "PDFs":[".pdf"], 
        "Documents":[".doc", ".docx", ".html", ".xls", ".xlsx", ".txt", ".pptx"],
        "Executables":[".exe", ".sh", ".bat", ".cmd", ".com", ".run", ".msi"], 
        "Audio":[".m4a", ".mp3", ".wav", ".aiff", ".aac", ".ogg", ".wma"]
    }

    #Verifying type of files

    import shutil

    Files = os.listdir(Directory)
    Files = [f for f in Files if os.path.isfile(Directory+'/'+f)]

    for name in Files:

        Files = os.listdir(Directory)
        Files = [f for f in Files if os.path.isfile(Directory+'/'+f)]

        extension = name.split(".")
        extension = "."+extension[-1]

        for types in File_Types:
            found = False

            Files = os.listdir(Directory)   
            Files = [f for f in Files if os.path.isfile(Directory+'/'+f)]
            
            if extension in File_Types.get(types):
                found = True
                Old_path = Directory+name
                New_path = Directory+types
                try:
                    shutil.move(Old_path, New_path)
                except Exception as E:
                    print("Some error occurred!!")
                    print(f"Error:\n{E}")

                Files = os.listdir(Directory)   
                Files = [f for f in Files if os.path.isfile(Directory+'/'+f)]

        if found==False:
            Old_path = Directory+name
            New_path = Directory+"Others"

            try:
                shutil.move(Old_path, New_path)
            except Exception as E:
                print("Some error occurred!!")
                print(f"Error:\n{E}")
                
            Files = os.listdir(Directory)   
            Files = [f for f in Files if os.path.isfile(Directory+'/'+f)]

# Scan the specified folder for changes in the file System

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
    # Set the directory on watch
    watchDirectory = Directory
  
    def __init__(self):
        self.observer = Observer()
    
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive = False)
        self.observer.start()
        try:
            while True:
                Sort()
                time.sleep(5)
        except Exception as E:
            self.observer.stop()
            print("Observer Stopped")
            print(E)
  
        self.observer.join()
  
  
class Handler(FileSystemEventHandler):
  
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
  
        elif event.event_type == 'created':
            # Event is created, you can process it now
            print("Watchdog received created event - % s." % event.src_path)
        elif event.event_type == 'modified':
            # Event is modified, you can process it now
            print("Watchdog received modified event - % s." % event.src_path)
              
  
if __name__ == '__main__':
    watch = Watcher()
    watch.run()



