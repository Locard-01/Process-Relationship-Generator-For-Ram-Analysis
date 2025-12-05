# Process-Relationship-Generator-For-Ram-Analysis

### Script Overview
This script is designed to work with any CSV file, provided it contains process information, PID (Process ID), and PPID (Parent Process ID). It is therefore compatible with CSV output from tools like **Volatility**, **MemProcsFS**, and others.

### Key Configuration
The column names containing the PID and PPID data **must be specified manually** via the command-line arguments.

### Prerequisites
**! Important !:** Before using the script, install the required Python packages listed in the `requirements.txt` file.

### How to Use the Script
```
python .\ProcessRelationshipGenerator.py -h
```
```
Exécution 1 : Affichage de l'aide
bash
PS C:\Users\4N6\Desktop> python .\ProcessRelationshipGenerator.py -h

 __         ______     ______     ______     ______     _____
/\ \       /\  __ \   /\  ___\   /\  __ \   /\  == \   /\  __-.
\ \ \____  \ \ \/\ \  \ \ \____  \ \  __ \  \ \  __<   \ \ \/\ \
 \ \_____\  \ \_____\  \ \_____\  \ \_\ \_\  \ \_\ \_\  \ \____-
  \/_____/   \/_____/   \/_____/   \/_/\/_/   \/_/ /_/   \/____/


usage: ProcessRelationshipGenerator.py [-h] [--process_col] [--pid_col] [--ppid_col] [--path_col] [--createtime_col] [--exittime_col] csv_file output_dot

GENERATE A .DOT FILE FROM A CSV FILE DESCRIBING A PROCESS TREE.

positional arguments:
  csv_file           PATH TO THE SOURCE CSV FILE.
  output_dot         OUTPUT FILE NAME (WITH .DOT EXTENSION).

options:
  -h, --help         show this help message and exit
  --process_col
  --pid_col
  --ppid_col
  --path_col
  --createtime_col
  --exittime_col

USAGE EXAMPLES:
  python ProcessRelationshipGenerator.py data.csv output.dot --process_col "ProcessName" --pid_col "ProcessID" --ppid_col "ParentProcessPID" --path_col "FilePath" --createtime_col "CreateTime" --exittime_col "ExitTime"

NOTE:
  The arguments --process_col, --pid_col and --ppid_col are mandatory.
  
```

