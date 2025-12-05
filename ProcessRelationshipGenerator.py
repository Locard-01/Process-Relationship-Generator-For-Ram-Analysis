import pandas as pd
import networkx as nx
import argparse
import sys

# ASCII ART DISPLAY
print("""
 __         ______     ______     ______     ______     _____    
/\ \       /\  __ \   /\  ___\   /\  __ \   /\  == \   /\  __-.  
\ \ \____  \ \ \/\ \  \ \ \____  \ \  __ \  \ \  __<   \ \ \/\ \ 
 \ \_____\  \ \_____\  \ \_____\  \ \_\ \_\  \ \_\ \_\  \ \____- 
  \/_____/   \/_____/   \/_____/   \/_/\/_/   \/_/ /_/   \/____/ 
                                                                   
""")

# ARGUMENT CONFIGURATION
parser = argparse.ArgumentParser(
    description="GENERATE A .DOT FILE FROM A CSV FILE DESCRIBING A PROCESS TREE.",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
USAGE EXAMPLES:
  python %(prog)s data.csv output.dot --process_col "ProcessName" --pid_col "ProcessID" --ppid_col "ParentProcessPID" --path_col "FilePath" --createtime_col "CreateTime" --exittime_col "ExitTime"

NOTE:
  The arguments --process_col, --pid_col and --ppid_col are mandatory.
  Other arguments are optional.
"""
)

parser.add_argument("csv_file", type=str, help="PATH TO THE SOURCE CSV FILE.")
parser.add_argument("output_dot", type=str, help="OUTPUT FILE NAME (WITH .DOT EXTENSION).")

# ADD MANDATORY ARGUMENTS FOR COLUMN NAMES
parser.add_argument("--process_col", metavar="")
parser.add_argument("--pid_col", metavar="")
parser.add_argument("--ppid_col", metavar="")

# OPTIONAL ARGUMENTS
parser.add_argument("--path_col", metavar="")
parser.add_argument("--createtime_col", metavar="")
parser.add_argument("--exittime_col", metavar="")

# Parse arguments
args = parser.parse_args()

# LOAD CSV FILE
try:
    df = pd.read_csv(args.csv_file, encoding="utf-8-sig")
except FileNotFoundError:
    print(f"ERROR: FILE '{args.csv_file}' NOT FOUND. ENSURE THE PATH IS CORRECT.")
    sys.exit(1)
except UnicodeDecodeError:
    try:
        df = pd.read_csv(args.csv_file, encoding="utf-8")
    except:
        print("ERROR: UNABLE TO READ FILE. CHECK ITS ENCODING.")
        sys.exit(1)

# DISPLAY AVAILABLE COLUMNS
print("AVAILABLE COLUMNS IN CSV FILE:")
for i, col in enumerate(df.columns.tolist(), 1):
    print(f"  {i:2d}. {col}")
print()

# VERIFY MANDATORY ARGUMENTS ARE PROVIDED
if not args.process_col or not args.pid_col or not args.ppid_col:
    print("ERROR: The following arguments are mandatory:")
    if not args.process_col:
        print("  --process_col : COLUMN NAME CONTAINING PROCESS NAME")
    if not args.pid_col:
        print("  --pid_col : COLUMN NAME CONTAINING ProcessID")
    if not args.ppid_col:
        print("  --ppid_col : COLUMN NAME CONTAINING ParentProcessID")
    print(f"\nExample: python {sys.argv[0]} {args.csv_file} {args.output_dot} --process_col \"ProcessName\" --pid_col \"ProcessID\" --ppid_col \"ParentProcessPID\"")
    sys.exit(1)

# VERIFY MANDATORY COLUMNS EXIST
required_columns = {
    'Process (name)': args.process_col,
    'PID': args.pid_col,
    'PPID': args.ppid_col
}

all_columns_exist = True
for col_type, col_name in required_columns.items():
    if col_name not in df.columns:
        print(f"ERROR: Column '{col_name}' (for {col_type}) does not exist in CSV file.")
        print(f"       Available columns: {', '.join(df.columns.tolist())}")
        all_columns_exist = False

if not all_columns_exist:
    sys.exit(1)

# VERIFY OPTIONAL COLUMNS (warning only if specified but not found)
optional_columns = {
    'Path': args.path_col,
    'Creation time': args.createtime_col,
    'Exit time': args.exittime_col
}

for col_type, col_name in optional_columns.items():
    if col_name is not None and col_name not in df.columns:
        print(f"WARNING: Column '{col_name}' (for {col_type}) does not exist in CSV file. It will be ignored.")
        # Set to None to indicate column doesn't exist
        setattr(args, col_type.replace(' ', '_').replace('(', '').replace(')', '').lower() + '_col', None)

# CREATE GRAPH
G = nx.DiGraph()

# FUNCTION TO ESCAPE BACKSLASHES AND QUOTES
def escape_string(text):
    if pd.isna(text):
        return "N/A"
    text = str(text)
    # Escape backslashes for Graphviz
    text = text.replace('\\', '\\\\')
    # Escape quotes for Graphviz
    text = text.replace('"', '\\"')
    return text

# ADD NODES AND EDGES TO GRAPH
for _, row in df.iterrows():
    # RETRIEVE AND FORMAT DATA (only available data)
    process_name = escape_string(row[args.process_col])
    pid_value = escape_string(row[args.pid_col])
    
    # Build label step by step
    label_parts = [process_name, pid_value]
    
    # Add status ONLY if exittime_col is available
    if args.exittime_col and args.exittime_col in df.columns:
        status_value = "running" if pd.isna(row[args.exittime_col]) or str(row[args.exittime_col]).strip() == "" else "stopped"
        label_parts.append(status_value)
    
    # Add path if available
    if args.path_col and args.path_col in df.columns:
        path_value = escape_string(row[args.path_col])
        label_parts.append(path_value)
    
    # Format final label
    node_label = "{ " + " | ".join(label_parts) + " }"
    
    G.add_node(row[args.pid_col], label=node_label, shape="record")

    # ADD EDGES (check if PPID exists in PID values)
    if not pd.isna(row[args.ppid_col]) and row[args.ppid_col] in df[args.pid_col].values:
        G.add_edge(row[args.ppid_col], row[args.pid_col])

# WRITE DOT FILE DIRECTLY
try:
    with open(args.output_dot, 'w', encoding='utf-8') as f:
        f.write('digraph G {\n')
        f.write('    rankdir=LR;\n')  # HORIZONTAL LAYOUT
        f.write('    node [shape=record, fontsize=10];\n')
        
        # WRITE NODES
        for node in G.nodes():
            label = G.nodes[node]['label']
            f.write(f'    {node} [label="{label}"];\n')
        
        # WRITE EDGES
        for edge in G.edges():
            f.write(f'    {edge[0]} -> {edge[1]};\n')
        
        f.write('}\n')
    
    print("CONFIGURATION USED:")
    print(f"  - Process: {args.process_col} (mandatory)")
    print(f"  - PID: {args.pid_col} (mandatory)")
    print(f"  - PPID: {args.ppid_col} (mandatory)")
    
    if args.path_col and args.path_col in df.columns:
        print(f"  - Path: {args.path_col}")
    
    if args.createtime_col and args.createtime_col in df.columns:
        print(f"  - Creation time: {args.createtime_col}")
    
    if args.exittime_col and args.exittime_col in df.columns:
        print(f"  - Exit time: {args.exittime_col}")
    
    print(f"\n.dot file generated: {args.output_dot}")
    print(f"Processes: {len(df)}")
    print(f"Relationships: {len(G.edges())}")
    
    print(f"\nTo convert to image:")
    print(f"  - dot -Tpng {args.output_dot} -o {args.output_dot.replace('.dot', '.png')}")
    print(f"\nTo view or convert to image:")
    print(f"  - Visit site: https://dreampuf.github.io/")
    
except Exception as e:
    print(f"ERROR while writing .dot file: {e}")
    sys.exit(1)