# Process-Relationship-Generator-For-Ram-Analysis

### Script Overview
This script is designed to work with any CSV file, provided it contains process information, PID (Process ID), and PPID (Parent Process ID). It is therefore compatible with CSV output from tools like **Volatility**, **MemProcsFS**, and others.

### Key Configuration
The column names containing the PID and PPID data **must be specified manually** via the command-line arguments.

### Prerequisites
**! Important ! :** Before using the script, install the required Python packages listed in the `requirements.txt` file.

### How to Use the Script
List avaible colums in CSV file
```
python .\ProcessRelationshipGenerator.py process.csv process.dot
```
### Output
```
 __         ______     ______     ______     ______     _____
/\ \       /\  __ \   /\  ___\   /\  __ \   /\  == \   /\  __-.
\ \ \____  \ \ \/\ \  \ \ \____  \ \  __ \  \ \  __<   \ \ \/\ \
 \ \_____\  \ \_____\  \ \_____\  \ \_\ \_\  \ \_\ \_\  \ \____-
  \/_____/   \/_____/   \/_____/   \/_/\/_/   \/_/ /_/   \/____/


AVAILABLE COLUMNS IN CSV FILE:
   1. PID
   2. PPID
   3. State
   4. ShortName
   5. Name
   6. IntegrityLevel
   7. User
   8. CreateTime
   9. ExitTime
  10. Wow64
  11. EPROCESS
  12. PEB
  13. PEB32
  14. DTB
  15. UserDTB
  16. UserPath
  17. Path
  18. CommandLine
  19. Flag

ERROR: The following arguments are mandatory:
  --process_col : COLUMN NAME CONTAINING PROCESS NAME
  --pid_col : COLUMN NAME CONTAINING ProcessID
  --ppid_col : COLUMN NAME CONTAINING ParentProcessID

Example: python .\ProcessRelationshipGenerator.py process.csv process.dot --process_col "ProcessName" --pid_col "ProcessID" --ppid_col "ParentProcessPID"
  
```

