#!/usr/bin/env python3
import psutil
import time
import psutil, time
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.live import Live
import sys

if "--kill" in sys.argv:
    pid = int(input("Enter PID to kill: "))
    try:
        p = psutil.Process(pid)
        name = p.name()
        p.kill()
        print(f"Killed {name} ({pid})")
    except:
        print("Could not kill that process!")
    sys.exit()

console = Console()

def make_bar(percent):
    filled = int((percent / 100) * 20)
    return "█" * filled + "░" * (20 - filled)

def make_process_table():
    table = Table(title="⚡ Top Processes")
    table.add_column("PID", style="cyan")
    table.add_column("Name", style="white")
    table.add_column("CPU %", style="yellow")
    table.add_column("RAM %", style="green")
    
    procs = sorted(
        psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']),
        key=lambda p: p.info['cpu_percent'] or 0,
        reverse=True
    )[:5]
    
    for p in procs:
        table.add_row(
            str(p.info['pid']),
            p.info['name'][:20],
            str(round(p.info['cpu_percent'], 1)),
            str(round(p.info['memory_percent'] or 0, 1))
        )
    return table


boot_time = psutil.boot_time()
uptime_seconds = time.time() - boot_time
hours = int(uptime_seconds // 3600)
minutes = int((uptime_seconds % 3600) // 60)




def make_dashboard():
    cpu_panel = Panel(f"[{cpu_color}]{make_bar(cpu)} {cpu}%[/]", title="🖥 CPU")
    ram_panel = Panel(f"[{ram_color}]{make_bar(ram)} {ram}%[/]", title="🧠 RAM")
    disk_panel = Panel(f"[{disk_color}]{make_bar(disk)} {disk}%[/]", title="💾 Disk")
    battery_panel = Panel(f"{status}\n{round(battery_percent, 1)}%",title="🔋️ Battery")
    uptime_panel=Panel(f"{hours}h {minutes}m",title="🕒️ Uptime")
    return Columns([cpu_panel, ram_panel, disk_panel, make_process_table(), battery_panel,uptime_panel])

with Live(refresh_per_second=2) as live:
    while True:
        disk = psutil.disk_usage('/').percent
        ram = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent(interval=0.5)
        battery = psutil.sensors_battery()
        battery_percent = battery.percent
        plugged = battery.power_plugged
        
        if disk < 50:
            disk_color = "green"
        elif disk < 80:
            disk_color = "yellow"
        else:
            disk_color = "red"

        if ram < 50:
            ram_color = "green"
        elif ram < 80:
            ram_color = "yellow"
        else:
            ram_color = "red"

        if cpu < 50:
            cpu_color = "green"
        elif cpu < 80:
            cpu_color = "yellow"
        else:
            cpu_color = "red"
        if plugged:
           status = "🔌️ Charging"
        else:
           status = "🔋️ On Battery"
        live.update(make_dashboard())
        time.sleep(0.5)
