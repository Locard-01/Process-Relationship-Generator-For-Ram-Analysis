# Process-Relationship-Generator-For-Ram-Analysis

### | Script Overview
This script is designed to work with any CSV file, provided it contains process information, PID (Process ID), and PPID (Parent Process ID). It is therefore compatible with CSV output from tools like **Volatility**, **MemProcsFS**, and others.

###  | Key Configuration
The column names containing the PID and PPID data **must be specified manually** via the command-line arguments.

### | Prerequisites
**! Important ! :** Before using the script, install the required Python packages listed in the `requirements.txt` file.

### | How to Use the Script
#### Command-line to list avaible colums in CSV file :
```
python .\ProcessRelationshipGenerator.py process.csv process.dot
```
#### Command-line to generate the DOT file :
```
python .\ProcessRelationshipGenerator.py process.csv process.dot --process_col "ProcessName" --pid_col "ProcessID" --ppid_col "ParentProcessPID"
```



