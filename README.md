# Python to C++ Compiler

This project is a Python to C++ compiler that utilizes ANTLR4 for parsing. The implementation is in Python and generates a `output.cpp` file from a given Python source file.

## Getting Started

### Prerequisites

To run this compiler, you need the following dependencies:

- Python 3.x
- ANTLR runtime 4.11.1
- FastAPI
- Uvicorn

### Installation

1. **Clone the repository:**

    ```sh
    git@github.com:Kompilatory-Projekt/kompilatory-projekt.git
    cd kompilatory-projekt
    ```

2. **Install the dependencies:**

    ```sh
    pip install antlr4-python3-runtime==4.11.1 fastapi uvicorn
    uvicorn app:app
    ```

    Got to localhost `http://127.0.0.1:8000`

### Usage

To compile a Python file to C++, run the following command:

```sh
python main.py FILE_TO_CONVERT.py
```

## Compilation examples
- Variable assignment
    - `a=2` -> `int a = 2;`
    - More complex types:   
        ```python
        a = [{1,2,3}, {456}]
        ```
        ```c++
        vector<map<int>> a = {{1,2,3},{4,5,6}};
        ```

- If/else statement

  Input:
    ```python
    if '2' is not 2:
        pass
    else:
        pass
    ```
    Output:
    ```c++
    if ("2" != 2) {
    }
    else {
    }
    ```

- For loops
    - Basic for loop
  
        Input:
        ```python
        for i in range(1, 10, 1):
            pass
        ```
        Output:
      ```c++
      for(int i = 1; i <  10; i += 1) {
      }
      ```
    - Range based for loop
        Input:
        ```python
        for i in range(1, 10, 1):
            pass
        ```
        Output:
        ```c++
        vector<int> a = {1,2,3,4};
        for(auto i : a) {
        }
        ```

- While loop

    Input:
    ```python
    while True:
    pass
    ```
    Output:
    ```python
    while (True) {
    }
    ```
- Try/catch statements

    Input
    ```python
    try:
        pass
    except ValueError as error:
        pass
    ```
    Output:
    ```c++
    try {
    }
    catch (std::invalid_argument& e) {
    }
    ```

- Function declaration

    Input
    ```python
    def funkcja(a: str, b: bool, c) -> str:
        return a + b * b + 10
    ```
    Output:
    ```c++
    string funkcja(string a, bool b, auto c) {
        return a + b * b + 10;
    }
    ```

- Print statement

    Input
    ```python
    print()
    print('Hello World!')
    ```
    Output:
    ```c++
    cout << endl;
    cout << "Hello World!" << endl;
    ```

- Auto library inclusion
    `2**3` -> 
    ```c++
    #include <cmath>
    using namespace std;
    pow(2, 3)
    ```

- main function 

    Input
    ```python
    def b() -> None:
        pass

    a = 2
    ```
    Output
    ```c++
    void b() {}

    int main() {
        int a = 2;
    }
    ```

- Scopes

    Input:
    ```python
    def funkcja(a: int) -> int:
        return a

    print(a)
    ```
    Output
    ```
    NameError: a does not exist in any scope
    ```
