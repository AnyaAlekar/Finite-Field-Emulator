This is a finite field emulator that functions as a arithmetic calculator for polynomials in the field Fp^m
#### Tech Stack
**Python**: The program has been written entirely in python. The GUI has been created using the library tkinter

#### GUI
![Start page](output/start_page.png)
1[](output/entering_irreducible_polynomial.png)
![](output/user_specifications.png)
![](output/calculator_view.png)
![](output/field_elements.png)
![](output/input_calculator.png)
![](output/output_calculator.png)

#### Working
- The program takes as input a prime number p, an integer m and an irreducible polynomial of degree m in the field Fp.
- Next, the program presents to the user a dropdown list of all polynomials in the field Fp^m i.e. polynomials of degree less than m in field Fp.
- The user can choose from the field elements and operators and enter an expression for the calculator to parse.
- The calculator displays the resulting polynomial on the screen.

#### Error Detection
![Error Detection](output/Error.png)
- The parser detects an invalid expression for example, unbalanced parenthesis, zero division, etc.
