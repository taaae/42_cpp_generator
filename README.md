<h2 align="center">
  C++ Modules Generator
</h2>
A small Python script for 42 C++ modules, saving you from tedious manual work. Will generate makefile, classes, header guards, orthodox canonical form definitions etc.

<h2 align="center">
  Demo
</h2>

https://github.com/user-attachments/assets/d0c8306c-d7ad-4a3a-8664-067f0660f9ea

<h2 align="center">
Usage
</h2>

Copy `generator.py` in your C++ module repository:
```
wget https://raw.githubusercontent.com/taaae/42_cpp_generator/main/generator.py
# or
curl -O https://raw.githubusercontent.com/taaae/42_cpp_generator/main/generator.py
```
Run the script passing the module and exercise number as arguments:
```
python3 generator.py cpp05 ex03
```
Generating the whole module works as well (note that you will need to manually copy-paste the code afterwards):
```
python3 generator.py cpp05
```
To view list of options:
```
python3 generator.py --help
```
