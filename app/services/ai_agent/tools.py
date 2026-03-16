import os
from langchain_core.tools import tool

# The AI uses these tools to do real work.

@tool
def list_data_files(directory: str = "data"):
    """
    Use this tool to see the names of all files in the 'data' folder.
    It returns a list like ['counter.v', 'constraints.sdc'].
    """
    try:
        if not os.path.exists(directory):
            return f"Directory '{directory}' not found."
        files = os.listdir(directory)
        return files if files else "The directory is empty."
    except Exception as e:
        return f"Error reading directory: {str(e)}"

@tool
def verilog_syntax_check(code: str):
    """
    Use this tool to check if a Verilog code has basic parts.
    It looks for 'module', 'input', 'output', and 'endmodule'.
    """
    code_lower = code.lower()
    required = ["module", "input", "output", "endmodule"]
    missing = [word for word in required if word not in code_lower]
    
    if not missing:
        return "SUCCESS: The code has basic Verilog structure."
    else:
        return f"ERROR: Missing Verilog keywords: {', '.join(missing)}"

@tool
def timing_calculator(value: float, convert_to: str):
    """
    Use this tool to convert Frequency to Period or Period to Frequency.
    'value' is a number. 'convert_to' can be 'period' or 'frequency'.
    Example: 100MHz to period is 10ns. 10ns to frequency is 100MHz.
    """
    # Formula: T = 1/f or f = 1/T
    if value <= 0:
        return "Error: Value must be greater than 0."
    
    result = 1000 / value # Simple calc for ns and MHz
    
    if convert_to.lower() == "period":
        return f"Frequency {value} MHz is equal to Period {result} ns."
    elif convert_to.lower() == "frequency":
        return f"Period {value} ns is equal to Frequency {result} MHz."
    else:
        return "Error: Please specify 'period' or 'frequency'."