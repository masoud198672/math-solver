import re
from flask import Flask, render_template, request
from sympy import symbols, Eq, solve, sympify, Poly, sqrt
app = Flask(__name__)
def ltr(s):
    # Wrap math text so the browser keeps its left-to-right order
    return "\u2066" + s + "\u2069"
def quadratic_steps(left, right):
    # Returns a list of (text, math) pairs, or None if the equation is not quadratic
    x = symbols('x')
    expr = sympify(left) - sympify(right)
    poly = Poly(expr, x)
    if poly.degree() != 2:
        return None

    a = poly.coeff_monomial(x**2)
    b = poly.coeff_monomial(x)
    c = poly.coeff_monomial(1)
    d = b**2 - 4*a*c

    steps = []
    steps.append(("همه‌ی جمله‌ها را به یک طرف می‌بریم:", f"{expr} = 0"))
    steps.append(("ضرایب را مشخص می‌کنیم:", f"a = {a}, b = {b}, c = {c}"))
    steps.append(("دلتا را حساب می‌کنیم:", ltr(f"Δ = b² - 4ac = ({b})² - 4×({a})×({c}) = {d}")))

    if d > 0:
        r1 = (-b + sqrt(d)) / (2*a)
        r2 = (-b - sqrt(d)) / (2*a)
        steps.append(("فرمول ریشه‌ها را با عددها می‌نویسیم:", ltr(f"x = (-b ± √Δ) / 2a = (-({b}) ± √{d}) / (2×{a})")))        
        steps.append(("چون Δ بزرگ‌تر از صفر است، دو جواب متفاوت داریم:", f"x1 = {r1}, x2 = {r2}"))
    elif d == 0:
        r = -b / (2*a)
        steps.append(("چون Δ برابر صفر است، یک جواب (ریشه‌ی مضاعف) داریم:", f"x = -b / 2a = {r}"))
    else:
        steps.append(("چون Δ منفی است، معادله جواب حقیقی ندارد.", ""))
    return steps
def linear_steps(left, right):
    x = symbols('x')
    expr = sympify(left) - sympify(right)
    poly = Poly(expr, x)
    if poly.degree() != 1:
        return None

    a = poly.coeff_monomial(x)
    b = poly.coeff_monomial(1)
    r = -b / a

    steps = []
    steps.append(("همه‌ی جمله‌ها را به یک طرف می‌بریم:", f"{expr} = 0"))
    steps.append(("ضرایب را مشخص می‌کنیم:", f"a = {a}, b = {b}"))
    steps.append(("x را جدا می‌کنیم:", f"x = -b / a = {r}"))
    return steps


@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    error = None
    steps = None
    equation_text = ""

    if request.method == 'POST':
        equation_text = request.form.get('equation', '')

        if '=' not in equation_text:
            error = "لطفاً معادله را با علامت = بنویسید"
        elif len(equation_text) > 100 or not re.fullmatch(r'[0-9x+\-*/().=\s^]*', equation_text):
            error = "فقط از عدد، x و علامت‌های + - * / ** ( ) استفاده کن"
        else:
            try:
                x = symbols('x')
                fixed = equation_text.replace('^', '**')
                fixed = re.sub(r'(\d)\s*x', r'\1*x', fixed)
                left, right = fixed.split('=')                
                equation = Eq(sympify(left), sympify(right))
                result = ", ".join(f"x = {r}" for r in solve(equation, x))
                steps = quadratic_steps(left, right)
                if steps is None:
                    steps = linear_steps(left, right)
                if steps and "ندارد" in steps[-1][0]:
                    result = "این معادله ریشه‌ی حقیقی ندارد."
            except Exception:
                error = "معادله رو درست وارد نکردی. مثال: x**2 - 5*x + 6 = 0"
    return render_template('index.html', result=result, error=error, steps=steps, equation_text=equation_text)
if __name__ == '__main__':
    app.run(debug=True)