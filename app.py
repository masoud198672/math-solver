import streamlit as st
from sympy import symbols, Eq, solve

st.title("حل‌کن ریاضی")

options = ["معادله درجه اول", "معادله درجه دوم", "معادله درجه سوم"]
choice = st.selectbox("نوع معادله رو انتخاب کن:", options)

if choice == options[0]:
    equation_text = st.text_input("معادله رو وارد کن (مثلاً 2*x + 3 = 7):")

    if equation_text:
        if "=" not in equation_text:
            st.error("لطفاً معادله را با علامت = بنویسید، مثال: 2*x + 3 = 7")
        else:
            try:
                x = symbols('x')
                left_side, right_side = equation_text.split("=")
                equation = Eq(eval(left_side), eval(right_side))
                answer = solve(equation, x)
                st.success(f"جواب: {answer}")
            except:
                st.error("معادله رو درست وارد نکردی. این شکل بنویس: 2*x + 3 = 7")

elif choice == options[1]:
    equation_text = st.text_input("معادله رو وارد کن (مثلاً x**2 - 5*x + 6 = 0):")

    if equation_text:
        if "=" not in equation_text:
            st.error("لطفاً معادله را با علامت = بنویسید")
        else:
            try:
                x = symbols('x')
                left_side, right_side = equation_text.split("=")
                equation = Eq(eval(left_side), eval(right_side))
                answer = solve(equation, x)
                st.success(f"جواب: {answer}")
            except:
                st.error("معادله رو درست وارد نکردی. مثال: x**2 - 5*x + 6 = 0")

elif choice == options[2]:
    equation_text = st.text_input("معادله رو وارد کن (مثلاً x**3 - 6*x**2 + 11*x - 6 = 0):")

    if equation_text:
        if "=" not in equation_text:
            st.error("لطفاً معادله را با علامت = بنویسید")
        else:
            try:
                x = symbols('x')
                left_side, right_side = equation_text.split("=")
                equation = Eq(eval(left_side), eval(right_side))
                answer = solve(equation, x)
                st.success(f"جواب: {answer}")
            except:
                st.error("معادله رو درست وارد نکردی. مثال: x**3 - 6*x**2 + 11*x - 6 = 0")
