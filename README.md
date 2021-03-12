# Solving Linear Programming Problems in Python
**_(The naive way)_**

## 1. Setup the Environment
This assumes that you already have python installed.  
The Program was tested using Python 3.9.1 installed using Anaconda Distrubution.
<br>  

### **If you are using Anaconda Distrubution**

* Create the environment and install the requirements
```python
conda create --name lpp_env --file requirements.txt
```

* Activate the Enviroment
```python
conda activate lpp_env
```

### **If you are using python virtual environment**
Basically, please make sure that all the dependencies are installed before running the main.py file.

* Create a Virtualenv
```python
python3 -m venv env_name
```

* Activate the env
```python
.\env_name\Scripts\activate
```

* Install the Dependencies
```python
pip install -r requirements.txt
```

**_Note: If pip install fails for some reason (e.g. Due to not having proper build tools to install numpy, matplotlib, etc), you can also run:_**
```
easy_install numpy scipy matplotlib tabulate
```
**_The virtual environment has the script easy_install.exe in ./env_name/Scripts which can be used to install the required packages packages_**
   
<br>

## 2. To run the program run the command in the terminal

```python
python main.py -i input_filename
```
eg:
```python
python main.py -i input.txt
```

When a plot is displayed, Please close the plot window to proceed the next problem.

<br>

## Changing the inputs to the program

All the input problems are stored in a text file which we pass to the main.py when we run the program.

### Rules for the input text file

* A line beginning with a # is treated as a comment and will be ignored.
* Leave a single blank line between two LPPs.
* The variables can be anything. eg: x_1 and x_2, x1 and x2, a and b, or x and y, etc.
* Please leave no space between the coefficient and the variable. Anything after a number will be treated as a variable.  
  eg:  
  5x_1: coefficient 5 , variable x_1  
  5x1: coefficient 5 , variable x1
* Please use the signs  >=, <= or = for the constraints.  
  Do not use unicode symbols like, ≥ or ≤, because the program won't parse these symbols.

* Example Format of LPP:
  ```
    Maximize: z = 5x_1 + 4x_2
    Subject to:
        6x_1 + 4x_2 <= 24
        x_1 + 2x_2 <= 6
        -x_1 + x_2 <= 1
        x_2 <= 2
        x_1 >= 0
        x_2 >= 0
  ```

**_Note: The program can also handle LPPs with three or more variables. A sample input file _input.txt_ is included with a three variable LPP at the end._**