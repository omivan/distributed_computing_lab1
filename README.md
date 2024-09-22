This program shows the difference in execution of threads with differrent  priorities(niceness value) and POSIX scheduling policies.

1. Install the required Python package for plotting:
```bash
pip install matplotlib
```
2. Compile and run the C program:
```bash
gcc main.c -o main -lpthread && ./main
```

3. Once the C program has finished executing, run the Python script to visualize the result:
```bash
python main.py
```