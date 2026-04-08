# ⚡ syswatch

A live terminal system monitor for Linux built in Python.

## Features
- 🖥 Live CPU usage with progress bar
- 🧠 RAM monitoring with color alerts
- 💾 Disk usage tracking
- ⚡ Top processes table
- 🔋 Battery status
- 🕐 System uptime
- 💀 Kill processes with `--kill` flag

## Installation
```bash
git clone https://github.com/Suchi5567/syswatch.git
cd syswatch
pip3 install psutil rich --break-system-packages
sudo cp syswatch.py /usr/local/bin/syswatch
chmod +x /usr/local/bin/syswatch
```

## Usage
```bash
# Run dashboard
syswatch

# Kill a process
syswatch --kill
```

## Built With
- Python 3
- psutil
- rich
