from functions.get_file_content import get_file_content

lorem_content = get_file_content("calculator", "lorem.txt")

print(len(lorem_content))
print(lorem_content.endswith('[...File "lorem.txt" truncated at 10000 characters]'))
print(f"Result for current file:\n{get_file_content("calculator", "main.py")}")
print(f"Result for 'pkg/calculator.py' file:\n{get_file_content("calculator", "pkg/calculator.py")}")
print(f"Result for '/bin/cat' file:\n{get_file_content("calculator", "/bin/cat")}")
print(f"Result for 'pkg/does_not_exist.py' file:\n{get_file_content("calculator", "pkg/does_not_exist.py")}")