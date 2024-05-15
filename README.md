This is a finite field emulator that functions as an arithmetic calculator for polynomials in the field F<sub>p<sup>m</sup></sub>
## Tech Stack
**Python**: The program has been written entirely in Python. The GUI has been created using the library Tkinter

## How to Run
- Download the [main.exe](https://github.com/AnyaAlekar/Finite-Field-Emulator/blob/main/main.exe)
  ![image](https://github.com/AnyaAlekar/Finite-Field-Emulator/assets/98590820/6008c0eb-f3b0-48b7-b251-d07ae1999899)

- Run the downloaded file on your machine (Windows)
- The application is ready to use

## GUI
![Start page](output/start_page.png)
1[](output/entering_irreducible_polynomial.png)
![](output/user_specifications.png)
![](output/calculator_view.png)
![](output/field_elements.png)
![](output/input_calculator.png)
![](output/output_calculator.png)

## Working
- The program takes as input a prime number p, an integer m, and an irreducible polynomial of degree m in the field F<sub>p</sub>
- Next, the program presents to the user a dropdown list of all polynomials in the field F<sub>p<sup>m</sup></sub> i.e. polynomials of degree less than m in field F<sub>p</sub>
- The user can choose from the field elements and operators and enter an expression for the calculator to parse.
- The calculator displays the resulting polynomial on the screen.

## Error Detection
![Error Detection](output/Error.png)
- The parser detects an invalid expression, for example, unbalanced parenthesis, zero division, etc.

## Update (Display Multiplication Table)
![image](https://github.com/AnyaAlekar/Finite-Field-Emulator/assets/98590820/f1316fe1-68ae-4431-951c-538966e3c7fd)
- The display button generates a multiplication table showcasing the products of various field elements with every other field element


