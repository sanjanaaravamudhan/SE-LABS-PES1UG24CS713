# Lab 5 – Static Code Analysis Reflection

## 1. What did you learn about static code analysis?

Static code analysis helps identify potential bugs, security vulnerabilities, and coding standard violations without executing the program. Through this lab, I understood how tools like Pylint, Bandit, and Flake8 examine different aspects of Python code and help improve its overall quality.

## 2. What issues did you identify and fix?

The original program contained several issues, including the use of `eval()`, weak MD5 hashing, insecure random number generation, shell command execution, mutable default arguments, broad exception handling, unused variables, and formatting violations.

I addressed these by using safer alternatives, improving exception handling, following Python naming conventions, adding function docstrings, and correcting formatting issues.

## 3. What was the contribution of each analysis tool?

- **Bandit:** Identified security vulnerabilities and unsafe coding practices. All reported security issues were resolved.
- **Flake8:** Identified formatting and PEP 8 style violations. The updated code passed without violations.
- **Pylint:** Identified code quality issues such as missing docstrings, invalid naming conventions, and mutable default arguments. The final score improved to 10.00/10.

## 4. How does static analysis improve software quality?

Static analysis improves software quality by identifying problems early in development, making code more secure, readable, maintainable, and consistent. It also reduces the possibility of bugs and encourages developers to follow good programming practices.

## Conclusion

This lab helped me understand the importance of using multiple static analysis tools during software development. By applying Bandit, Flake8, and Pylint, I was able to improve the assigned program and verify the corrections through their reports.