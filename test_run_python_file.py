from functions.run_python_file import run_python_file

print(f"Result from running calculator.py:\n{run_python_file("calculator", "main.py")}")
print(f"Result from running calculator.py with 3 + 5:\n{run_python_file("calculator", "main.py", ["3 + 5"])}")
print(f"Result from running tests.py:\n{run_python_file("calculator", "tests.py")}")
print(f"Result from running ../main.py:\n{run_python_file("calculator", "../main.py")}")
print(f"Result from running nonexistent.py:\n{run_python_file("calculator", "nonexistent.py")}")
print(f"Result from running lorem.txt:\n{run_python_file("calculator", "lorem.txt")}")