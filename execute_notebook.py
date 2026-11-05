#!/usr/bin/env python3
"""
execute_notebook.py - Executes notebooks/01_source_profiling.ipynb and saves output cells.
"""

import os
import sys
import io
import contextlib
import nbformat as nbf

notebook_path = os.path.join("notebooks", "01_source_profiling.ipynb")
with open(notebook_path, "r", encoding="utf-8") as f:
    nb = nbf.read(f, as_version=4)

# Create an execution namespace (simulating running inside notebooks/ folder)
notebook_dir = os.path.abspath("notebooks")
current_dir = os.getcwd()
os.chdir(notebook_dir)

exec_globals = {
    "__file__": os.path.abspath(notebook_path),
    "__name__": "__main__",
}

# Dummy display function for CLI execution capture
def display_capture(*args):
    for a in args:
        print(a)
exec_globals["display"] = display_capture

cell_counter = 1
for cell in nb.cells:
    if cell.cell_type == "code":
        code = cell.source
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
                exec(code, exec_globals)
            out_text = stdout_capture.getvalue()
            err_text = stderr_capture.getvalue()
            
            outputs = []
            if out_text:
                outputs.append(nbf.v4.new_output(output_type="stream", name="stdout", text=out_text))
            if err_text:
                outputs.append(nbf.v4.new_output(output_type="stream", name="stderr", text=err_text))
                
            cell.outputs = outputs
            cell.execution_count = cell_counter
            cell_counter += 1
            print(f"Cell {cell_counter - 1} executed successfully.")
        except Exception as e:
            print(f"Error in cell {cell_counter}: {e}")
            err_output = nbf.v4.new_output(output_type="error", ename=type(e).__name__, evalue=str(e), traceback=[str(e)])
            cell.outputs = [err_output]
            cell.execution_count = cell_counter
            break

os.chdir(current_dir)

with open(notebook_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"\nNotebook successfully executed and saved with all outputs to {notebook_path}!")
