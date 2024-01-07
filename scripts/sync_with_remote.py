import typer
import time
import subprocess
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from rich import print
from rich.console import Console


app = typer.Typer()


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, local_directory, remote_dest):
        self.local_directory = local_directory
        self.remote_dest = remote_dest

    def on_any_event(self, event):
        # Trigger the sync if the change is within the local_directory or its subdirectories
        if Path(self.local_directory) in Path(event.src_path).parents:
            console = Console()
            console.log()
            console.log(f"{event}")
            self.sync_directory()

    def sync_directory(self):
        command = [
            "rsync",
            "-avz",
            "--delete",
            "--exclude",
            "./.ignore/venv/",
            "--exclude",
            "./.idea",
            f"{self.local_directory}/",
            self.remote_dest,
        ]
        # Show a rich loading indicator while the next line runs
        console = Console()
        with console.status(
            f"[bold green]Syncing {self.local_directory} to {self.remote_dest}...[/]",
            spinner="dots",
        ):
            try:
                subprocess.check_output(command, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                console.log(
                    f"[bold red]Error syncing {self.local_directory} to {self.remote_dest}[/]"
                )
                console.log(f"[bold red]{e.output}[/]")
                return

        console.log(f"Synced {self.local_directory} to {self.remote_dest}")


@app.command()
def watch_and_sync(local_directory: str, host: str):
    """
    Watch a local directory and sync it to the remote destination whenever it changes.

    Args:
    local_directory (str): Path to the local directory to be monitored.
    host (str): SSH destination of the remote machine to sync to, e.g. ubuntu@129.1.1.1 or an SSH shortcut.
    """
    local_path = Path(local_directory)
    directory_name = local_path.name

    # TODO: Add support beyond ubuntu
    remote_path = f"/home/ubuntu/synced/{directory_name}"

    remote_dest = f"{host}:{remote_path}"

    event_handler = ChangeHandler(local_directory, remote_dest)
    observer = PollingObserver()
    observer.schedule(event_handler, path=str(local_path), recursive=True)

    print(f"Watching {local_path.absolute()} and syncing to {remote_dest}")
    print()
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        typer.echo("Stopped watching.")
    observer.join()


if __name__ == "__main__":
    app()
