import typer
import time
import subprocess
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from rich import print
from datetime import datetime


app = typer.Typer()


def t():
    current_time = datetime.now().strftime("%I:%M %p")
    return current_time


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, local_file, remote_dest):
        self.local_file = local_file
        self.remote_dest = remote_dest

    def on_modified(self, event):
        if Path(event.src_path) == Path(self.local_file):
            print()
            print(f"{t()}: {event}")
            self.sync_file()

    def sync_file(self):
        command = ["rsync", "-avz", self.local_file, self.remote_dest]
        subprocess.check_output(command, stderr=subprocess.STDOUT)
        print(f"{t()}: Synced {self.local_file} to {self.remote_dest}")


@app.command()
def watch_and_sync(local_file: str, host: str):
    """
    Watch a local file and sync it to the home directory of a remote destination whenever it changes.

    Args:
    local_file (str): Path to the local file to be monitored.
    host (str): SSH destination of the remote machine to sync to e.g. ubuntu@129.1.1.1 or an SSH shortcut
                such as ubuntulambda
    """
    local_path = Path(local_file)
    file_name = local_path.name

    remote_path = f"/home/ubuntu/{file_name}"

    remote_dest = f"{host}:{remote_path}"

    event_handler = ChangeHandler(local_file, remote_dest)
    # event_handler = LoggingEventHandler()
    observer = PollingObserver()
    watch = local_path.absolute()
    # watch = local_path.parent.absolute()
    watch = "."
    observer.schedule(event_handler, path=str(watch), recursive=True)

    print(f"Watching {local_path.absolute()} and syncing to {remote_dest}")
    print()
    observer.start()
    observer.is_alive()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        typer.echo("Stopped watching.")
    observer.join()


if __name__ == "__main__":
    app()
