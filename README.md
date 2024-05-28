### Compilation examples
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
