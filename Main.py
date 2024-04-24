import tkinter as tk
from tkinter import ttk

# Field Algebra
def generate_polynomial(poly):
    ans = ""
    for i in range(len(poly)):
        if(poly[i] == 0): continue
        else: ans += f"{poly[i]} x^{i} + "
    if(ans): ans = ans[:-2]
    else: return '0'
    return ans.strip()

def define_field(p, m, irreducible_poly):
    def generate_field_elements(comb, sol, idx):
        if(idx == m):
          sol.add(tuple(comb))
          return
        for i in range(p):
          comb.append(i)
          generate_field_elements(comb, sol, idx + 1)
          comb.pop()
        return sol
    
    sol = generate_field_elements([], set(), 0)
    field_elements = list(map(list, sol))
    for i in range(p ** m):
      while(field_elements[i] and field_elements[i][-1] == 0): field_elements[i].pop()
      if(field_elements[i] == []): field_elements[i] = [0]
      
    def degree(poly):
        while poly and poly[-1] == 0:
            poly.pop()   # normalize
        return len(poly)-1

    #in a field mod p, n and n + p are congurent
    def congruence(n,m):
        while ((n % p) % m) != 0:
            n = n + p
        return n
    
    def rem(u, v):
        n, m = degree(u), degree(v)
        if m < 0: raise ZeroDivisionError
        if n >= m:
            while n >= m:
                d = [0] * (n - m) + v
                if u[-1] % float(v[-1]) != 0:
                    mult = congruence(u[-1],float(v[-1])) / float(v[-1])
                else:
                    mult = u[-1] / float(d[-1])
                d = [(coeff * mult) % p for coeff in d]
                u = [(coeffu - coeffd) % p for coeffu, coeffd in zip(u, d)]
                n = degree(u)
            r = u
        else:
            r = u
        return r
    
    def add(u, v):
        n, m = len(u), len(v)
        m_, ans = max(n, m), []
        u = u + [0] * (m_ - n)
        v = v + [0] * (m_ - m)
        for i in range(m_):
          ans.append((u[i] + v[i]) % p)
        while(ans and ans[-1] == 0):
          ans.pop()
        if(not ans): return [0]
        r = rem(ans, irreducible_poly)
        return r
  
    #  u(x) - v(x)
    def subtract(u, v):
        n, m = len(u), len(v)
        m_, ans = max(n, m), []
        u = u + [0] * (m_ - n)
        v = v + [0] * (m_ - m)
        for i in range(m_):
          ans.append((u[i] - v[i]) % p)
        while(ans and ans[-1] == 0):
          ans.pop()
        if(not ans): return [0]
        r = rem(ans, irreducible_poly)
        return r
    
    def multiply(u, v):
        n, m = len(u), len(v)
        ans = [0 for _ in range(n + m)]
        for i in range(n):
          for j in range(m):
            ans[i + j] += u[i] * v[j]
        for i in range(n + m):
          ans[i] %= p
        while(ans and ans[-1] == 0):
          ans.pop()
        if(not ans): return [0]
        r = rem(ans, irreducible_poly)
        return r
  
    def divide(u, v):
        q, r = [0], u
        divisorDeg = degree(v)
        divisorLC = v[-1]
    
        while degree(r) >= divisorDeg:
            monomialExponent = degree(r) - divisorDeg
            monomialZeros = [0 for _ in range(monomialExponent)]
            if r[-1] % divisorLC != 0:
                monomialDivisor = monomialZeros + [congruence(r[-1], divisorLC) // divisorLC]
            else:
                monomialDivisor = monomialZeros + [r[-1] // divisorLC]
    
            q = add(q, monomialDivisor)
            r = subtract(r, multiply(monomialDivisor, v))
    
        return q, r
           
    def find_inverse():
        d = {}
        for ele in field_elements:
          for ele2 in field_elements:
            if(tuple(ele2) in d): continue
            if(multiply(ele, ele2) == [1]):
              d[tuple(ele)] = tuple(ele2)
              d[tuple(ele2)] = tuple(ele)
        return d
    
    inverse = find_inverse()
    
    return field_elements, inverse

# GUI
def go_to_next_page(entry1, entry2):
    # Get the values from the entry widgets 
    p = entry1.get()
    m = entry2.get()
    
    # Validate the input
    if p.isdigit() and m.isdigit():
        # Open the next page with the values
        next_page(int(p), int(m))
    else:
        # Show error message and clear entry widgets
        tk.messagebox.showerror("Error", "Please enter valid numbers.")
        entry1.delete(0, tk.END)
        entry2.delete(0, tk.END)

def generate_irreducible_poly(p, m, entries):
    # Created the irreducible_poly format
    irreducible_poly = ""
    for i in range(m + 1):
        entries[i] %= p
        if(entries[i] == 0): continue
        else: irreducible_poly += f"{entries[i]} x^{m - i} + "
    if(irreducible_poly): irreducible_poly = irreducible_poly[:-2]
    else: return '0'
    return irreducible_poly

def next_page(p, m):
    # Created the next page 
    next_page_window = tk.Toplevel(root)
    next_page_window.title("Irreducible Polynomial")
    next_page_window.geometry('590x500')
    
    # Created heading label
    heading_label = ttk.Label(next_page_window, text="Enter Coefficients of Irreducible Polynomial", font=("Helvetica", 20, "bold"))
    heading_label.grid(row=0, column=0, columnspan=2, pady=5)
    
    # Created entry widgets 
    entries = []
    for i in range(m + 1):
        # Negative and 0 are allowed, if blank then assume 0 and throw error at which coefficients user did not enter correct value
        label = ttk.Label(next_page_window, text=f"Enter coefficient for x**{m - i}:")
        label.grid(row=i+1, column=0, padx=5, pady=5, sticky="e")
        entry = ttk.Entry(next_page_window)
        entry.grid(row=i+1, column=1, padx=5, pady=5)
        entries.append(entry)
            
    # Created button to generate irreducible_poly
    generate_button = ttk.Button(next_page_window, text="Generate Irreducible Polynomial", command=lambda: show_irreducible_poly(p, m, entries, next_page_window))
    generate_button.grid(row=m + 2, column=0, columnspan=2, padx=5, pady=10)

def show_irreducible_poly(p, m, entries, next_page_window):
    error = []
    values = []
    
    # Validation
    for i in range(m + 1):
        e = entries[i].get() 
        
        if(e == ''): e = 0    # Blank space considered as 0
        elif(e[0] == '-'):      # Negative coefficients allowed
            if(e[1:].isdigit()): e = -1 * int(e[1:])
            else: error.append(i)
        elif(e.isdigit()): e = int(e)  # Positive coefficients 
        else: error.append(i)        # Not a digit
        values.append(e)
 
    if(error): 
        tk.messagebox.showerror("Error", "Please enter valid coefficients")
        for i in error: entries[i].delete(0, tk.END)
    elif((values[0] % p) == 0): 
        tk.messagebox.showerror("Error", "Please enter degree m polynomial")
        entries[0].delete(0, tk.END)
    else: 
        # Generate the irreducible_poly
        irreducible_poly = generate_irreducible_poly(p, m, values)
        next_page_window.destroy()
        
        # Created label to display the irreducible_poly
        irreducible_poly_label = ttk.Label(root, text="Irreducible Polynomial Entered")
        irreducible_poly_label.pack()
        irreducible_poly_text = tk.Text(root, height=2, width=60)
        irreducible_poly_text.insert(tk.END, irreducible_poly)
        irreducible_poly_text.pack(pady=5)
        
        irreducible_poly = values[::-1]
        
        calc_button = ttk.Button(root, text="Calculator", command=lambda: calculator(irreducible_poly, p, m))
        calc_button.pack(pady=10)
        
def calculator(irreducible_poly, p, m):
    # Created the new popup window
    calculator_window = tk.Toplevel(root)
    calculator_window.title("Calculator")
    calculator_window.geometry("500x500")
    
    field_elements, inverse = define_field(p, m, irreducible_poly)
    field_elements_polynomials = {}
    for ele in field_elements:
        field_elements_polynomials[generate_polynomial(ele)] = ele
        
    # Created a heading for the calculator page
    heading_label = ttk.Label(calculator_window, text="Calculator", font=("Helvetica", 20, "bold"))
    heading_label.pack(pady=10)
    
    # Created a text box to display the input
    input_textbox = tk.Text(calculator_window, height=2, width=60)
    input_textbox.pack(pady=10)
    
    # Created a dropdown menu with p ** m elements    
    label_frame = ttk.Frame(calculator_window)
    label_frame.pack(pady=10)

    # Created a label for the dropdown menu
    label = ttk.Label(label_frame, text="Field Elements:   ")
    label.pack(side=tk.LEFT)

    # Created a Combobox with rounded corners
    combobox_style = ttk.Style()
    combobox_style.configure('Rounded.TCombobox', borderwidth=1, relief="solid", padding=5, bordercolor="gray", fieldbackground="white", foreground="black")
    field_element_combobox = ttk.Combobox(label_frame, style='Rounded.TCombobox')
    field_element_combobox['values'] = [i for i in field_elements_polynomials]   #zip of field elements in polynomial form and coefficient list for user and developer respectively
    field_element_combobox.current(0)  # Set the default value
    field_element_combobox.pack(side=tk.LEFT)
    
    def append_field_element():
        selected_element = field_element_combobox.get()
        current_input = input_textbox.get("1.0", tk.END).strip()  # Get current input text
        if(current_input == 'Error'): 
            all_clear()
            current_input = ""
        if(current_input in field_elements_polynomials):
            all_clear()
            current_input = field_elements_polynomials[current_input]
        new_input = f"{current_input} {field_elements_polynomials[selected_element]}"  # Append selected element
        input_textbox.delete("1.0", tk.END)  # Clear current input
        input_textbox.insert(tk.END, new_input)  # Set new input
    
    # Created "Enter" button for dropdown menu
    enter_button = ttk.Button(label_frame, text="Enter", command=append_field_element)
    enter_button.pack(side=tk.LEFT, padx=5)
    
    # Function to update input text box
    def append_operator(button_label):
        current_input = input_textbox.get("1.0", tk.END).strip()  # Get current input text
        if(current_input == 'Error'): 
            all_clear()
            current_input = ""
        if(current_input in field_elements_polynomials):
            all_clear()
            current_input = field_elements_polynomials[current_input]
        new_input = f"{current_input} {button_label}"  # Build new input
        input_textbox.delete("1.0", tk.END)  # Clear current input
        input_textbox.insert(tk.END, new_input)  # Set new input

    
    # Created buttons frame for operators
    operators_frame = ttk.Frame(calculator_window)
    operators_frame.pack(pady=10)
    
    # Button labels for operators
    operators = ['+', '-', '*', '/', '(', ')']
    
    # Created operator buttons and assign functions to them
    for label in operators:
        button = ttk.Button(operators_frame, text=label, command=lambda label=label: append_operator(label))
        button.pack(side=tk.LEFT, padx=5)
    
    def all_clear(): 
        input_textbox.delete("1.0", tk.END)  # Clear current input
        
    def backspace():
        current_input = input_textbox.get("1.0", tk.END).strip()  # Get current input text
        new_input = " ".join(current_input.split()[:-1])
        input_textbox.delete("1.0", tk.END)  # Clear current input
        input_textbox.insert(tk.END, new_input)  # Set new input
    
    def calculate(current_input):
        def operandStack(listNumbers: str):
            numbers = listNumbers[1:len(listNumbers) - 1].split(',')
            return list(map(int, numbers))

        def splitInputString(input: str) -> list:
            input = input.replace(' ', '')
            inputStack, inputOperand, index = [], [], 0
            # Check for balanced parentheses, otherwise throw error
            parenthesesArray = [char for char in input if char in ['(', ')']]
            balancedStack = []
            for element in parenthesesArray:
                if element == '(':
                    balancedStack.append(element)
                else:
                    if len(balancedStack) == 0: return 'Error'
                    else:
                        balancedStack.pop()
            if len(balancedStack) != 0: return 'Error'
        
            # Checking for balanced polynomial brackets
            bracketsArray = [char for char in input if char in ['[', ']']]
            balancedStack = []
            for element in bracketsArray:
                if element == '[':
                    balancedStack.append(element)
                    if len(balancedStack) > 1: return 'Error'
                else:
                    if len(balancedStack) == 0: return 'Error'
                    else:
                        balancedStack.pop()
            if len(balancedStack) != 0: return 'Error'
        
            while index < len(input):
                if input[index] in ['+', '-', '*', '/', '(', ')']:
                    inputStack.append(input[index])
                    index += 1
                else:
                    if input[index] == '[':
                        inputOperand = []
                        closingBracket = index + input[index:].index(']')
                        inputStack.append(operandStack(input[index:closingBracket + 1]))
                        index = closingBracket + 1
        
            # Two consecutive operators or two consecutive operands cannot be evaluated together (for example: a * + b, a b * c)
            for index in range(0, len(inputStack) - 1, 1):
                if inputStack[index] in ['+', '-', '*', '/'] and inputStack[index + 1] in ['+', '-', '*', '/']: return 'Error'
                if isinstance(inputStack[index], list) and isinstance(inputStack[index + 1], list): return 'Error'
            return inputStack
    
        def parse(inputString: str):
            a = splitInputString(inputString)
            if(a != 'Error'): tokenStack = ['('] + a + [')']
            else: return a
            positionIndex = 0
            
            def tokenStackElement():
                nonlocal positionIndex
                return tokenStack[positionIndex]
            
            def moveIndex():
                nonlocal positionIndex
                positionIndex += 1
            
            def parsePrimaryExpression():
                token = tokenStackElement()
                # If token type is a polynomial
                if isinstance(token, list) and positionIndex < len(tokenStack):
                    moveIndex()
                    return token
                elif token == '(' and positionIndex < len(tokenStack):
                    moveIndex()
                    expression = parseExpression()
                    moveIndex()
                    return expression
            
            def parseMulExpression():
                expression = parsePrimaryExpression()
                token = tokenStackElement()
                while (positionIndex < len(tokenStack) and (token == '*' or token == '/')):
                    moveIndex()
                    rightHandExpression = parsePrimaryExpression()
                    expression = (token, expression, rightHandExpression)
                    token = tokenStackElement()
                return expression 
            
            def parseExpression():
                expression = parseMulExpression()
                token = tokenStackElement()
                while (positionIndex < len(tokenStack) and (token == '+' or token == '-')):
                    moveIndex()
                    rightHandExpression = parseMulExpression()
                    expression = (token, expression, rightHandExpression)
                    token = tokenStackElement()
                return expression
            
            result = parsePrimaryExpression()
            
            return result
        
        def degree(poly):
            while poly and poly[-1] == 0:
                poly.pop()   # normalize
            return len(poly)-1

        def congruence(n,m):
            while ((n % p) % m) != 0:
                n = n + p
            return n
        
        def rem(u, v):
            n, m = degree(u), degree(v)
            if m < 0: raise ZeroDivisionError
            if n >= m:
                while n >= m:
                    d = [0] * (n - m) + v
                    if u[-1] % float(v[-1]) != 0:
                        mult = congruence(u[-1],float(v[-1])) / float(v[-1])
                    else:
                        mult = u[-1] / float(d[-1])
                    d = [(coeff * mult) % p for coeff in d]
                    u = [(coeffu - coeffd) % p for coeffu, coeffd in zip(u, d)]
                    n = degree(u)
                r = u
            else:
                r = u
            return r
        
        def add(u, v):
            n, m = len(u), len(v)
            m_, ans = max(n, m), []
            u = u + [0] * (m_ - n)
            v = v + [0] * (m_ - m)
            for i in range(m_):
              ans.append((u[i] + v[i]) % p)
            while(ans and ans[-1] == 0):
              ans.pop()
            if(not ans): return [0]
            r = rem(ans, irreducible_poly)
            return r
      
        #  u(x) - v(x)
        def subtract(u, v):
            n, m = len(u), len(v)
            m_, ans = max(n, m), []
            u = u + [0] * (m_ - n)
            v = v + [0] * (m_ - m)
            for i in range(m_):
              ans.append((u[i] - v[i]) % p)
            while(ans and ans[-1] == 0):
              ans.pop()
            if(not ans): return [0]
            r = rem(ans, irreducible_poly)
            return r
        
        def multiply(u, v):
            n, m = len(u), len(v)
            ans = [0 for _ in range(n + m)]
            for i in range(n):
              for j in range(m):
                ans[i + j] += u[i] * v[j]
            for i in range(n + m):
              ans[i] %= p
            while(ans and ans[-1] == 0):
              ans.pop()
            if(not ans): return [0]
            r = rem(ans, irreducible_poly)
            return r
      
        def divide(u, v):
            q, r = [0], u
            divisorDeg = degree(v)
            divisorLC = v[-1]
        
            while degree(r) >= divisorDeg:
                monomialExponent = degree(r) - divisorDeg
                monomialZeros = [0 for _ in range(monomialExponent)]
                if r[-1] % divisorLC != 0:
                    monomialDivisor = monomialZeros + [congruence(r[-1], divisorLC) // divisorLC]
                else:
                    monomialDivisor = monomialZeros + [r[-1] // divisorLC]
        
                q = add(q, monomialDivisor)
                r = subtract(r, multiply(monomialDivisor, v))
        
            return q, r
        
        def evaluateExpr(expressionTuple):
            if isinstance(expressionTuple, list):
                return expressionTuple
            elif isinstance(expressionTuple, tuple):
                operator, operator1, operator2 = expressionTuple
                if(operator1 == None or operator2 == None or evaluateExpr(operator2) == 'Error' or evaluateExpr(operator1) == 'Error' or evaluateExpr(operator2) == [] or evaluateExpr(operator2) == ''): return 'Error'
                if operator == '+':
                    return add(evaluateExpr(operator1), evaluateExpr(operator2))
                elif operator == '-':
                    return subtract(evaluateExpr(operator1), evaluateExpr(operator2))
                elif operator == '*':
                    return multiply(evaluateExpr(operator1), evaluateExpr(operator2))
                elif operator == '/':
                    if(evaluateExpr(operator2) == [0] or evaluateExpr(operator2) == [0.0] or evaluateExpr(operator2) == [] or evaluateExpr(operator2) == ''): return 'Error'
                    return multiply(evaluateExpr(operator1), inverse[tuple(evaluateExpr(operator2))])
                
        e = parse(current_input)
        if(e != 'Error'): new_input = evaluateExpr(e)
        else: new_input = 'Error'
        return new_input
    
    def submit():
        current_input = input_textbox.get("1.0", tk.END).strip()  # Get current input text
        ans = calculate(current_input)
        if(ans != 'Error'): 
            for i in field_elements_polynomials:
                if(field_elements_polynomials[i] == ans): 
                    ans = i
                    break            
        input_textbox.delete("1.0", tk.END)  # Clear current input
        input_textbox.insert(tk.END, ans)  # Set new input
    
    # Created buttons frame for special buttons (AC, Backspace, Submit)
    special_buttons_frame = ttk.Frame(calculator_window)
    special_buttons_frame.pack(pady=10)
    
    # Created an All Clear button
    AC_button = ttk.Button(special_buttons_frame, text='AC', command=all_clear)
    AC_button.pack(side=tk.LEFT, padx=5)
    
    # Created a backspace button with Unicode symbol
    backspace_button = ttk.Button(special_buttons_frame, text='\u21e6', command=backspace)
    backspace_button.pack(side=tk.LEFT, padx=5)
    
    # Created a Enter button with Unicode symbol
    submit_button = ttk.Button(special_buttons_frame, text='=', command=submit)
    submit_button.pack(side=tk.LEFT, padx=5)

        
# Created the main window
root = tk.Tk()
root.title("User Input")
root.geometry("500x500")

# Created heading label
heading_label = ttk.Label(root, text="Specifications for Calculator", font=("Helvetica", 20, "bold"))
heading_label.pack(pady=10)

# Created frame for first set of entry widgets
top_frame1 = ttk.Frame(root)
top_frame1.pack(pady=10)

# Created frame for second set of entry widgets
top_frame2 = ttk.Frame(root)
top_frame2.pack(pady=10)

# Created entry widgets for numbers
p_label = ttk.Label(top_frame1, text="Enter Prime Number p:")
p_label.grid(row=0, column=0, pady=(10, 0), padx=10, sticky="e")
entry1 = ttk.Entry(top_frame1)
entry1.grid(row=0, column=1, pady=(10, 0), padx=10)

m_label = ttk.Label(top_frame2, text="Enter degree m:")
m_label.grid(row=0, column=0, pady=(10, 0), padx=10, sticky="e")
entry2 = ttk.Entry(top_frame2)
entry2.grid(row=0, column=1, pady=(10, 0), padx=10)

# Created button to go to next page
next_button = ttk.Button(root, text="Next", command=lambda: go_to_next_page(entry1, entry2))
next_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
