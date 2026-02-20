import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class XBioHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"📡 [SYNC] اكتشاف تغيير في: {event.src_path}")
            self.sync()

    def on_created(self, event):
        print(f"🆕 [VAULT] ملف جديد مضاف: {event.src_path}")
        self.sync()

    def sync(self):
        # تنفيذ المزامنة السيادية
        cmd = "rclone sync /root/X-BIO_Vault XBioDrive:X-BIO_Sovereign_Vault"
        subprocess.run(cmd, shell=True)
        print("✅ [CLOUD] تم تأمين التغييرات في سحابة X-BIO.")

if __name__ == "__main__":
    event_handler = XBioHandler()
    observer = Observer()
    observer.schedule(event_handler, path='/root/X-BIO_Vault', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
