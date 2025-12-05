# Process-Relationship-Generator-For-Ram-Analysis
<img width="1846" height="587" alt="Screenshot 2025-12-06 002421" src="https://github.com/user-attachments/assets/9c358bc7-a8c7-45f9-97df-4f732820f614" />
### Script Overview

This script is designed to work with any CSV file, provided it contains process information, PID (Process ID), and PPID (Parent Process ID). It is therefore compatible with CSV output from tools like **Volatility**, **MemProcsFS**, and others.

### Key Configuration
The column names containing the PID and PPID data **must be specified manually** via the command-line arguments.

### Prerequisites
**! Important ! :** Before using the script, install the required Python packages listed in the `requirements.txt` file.

### HOW TO
#### Command-line to list avaible colums in CSV file :
```
python .\ProcessRelationshipGenerator.py process.csv process.dot
```
#### Command-line to generate the DOT file :
```
python ProcessRelationshipGenerator.py data.csv output.dot --process_col "ProcessName" --pid_col "ProcessID" --ppid_col "ParentProcessPID" --path_col "FilePath" --createtime_col "CreateTime" --exittime_col "ExitTime"
```
#### To view or convert the DOT file online:
Visit: https://dreampuf.github.io/GraphvizOnline/

#### To convert the DOT file to an image using Graphviz:
```
dot -Tpng process.dot -o process.png
```





