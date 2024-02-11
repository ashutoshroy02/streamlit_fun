import streamlit as st

def fact(a):
    if a==0:
        return 0        
    elif a==1:
        return 1
    else:
        return a*fact(a-1)

def com(n,x):
    if n == 0 or  x == 0:
        return 0
    up = fact(n)
    down = fact(x) * fact(n-x)
    return int(up/down)


def binomial_distribution(n, x, p):
    # Calculate the binomial coefficient
    binomial_coefficient = com(n,x)
    
    # Calculate the probability mass function
    probability = binomial_coefficient * (p ** x) * ((1 - p) ** (n - x))
    
    return probability

def main():
    st.title("Binomial Distribution Calculator")
    
    # Input fields for user to enter values
    n = st.number_input("Enter the number of trials (n)", min_value=0, step=1, value=10)
    x = st.number_input("Enter the number of successes (x)", min_value=0, step=1, value=5)
    p = st.slider("Enter the probability of success (p)", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
    
    # Calculate the binomial distribution
    probability = binomial_distribution(n, x, p)
    
    # Display the result
    st.write(f"The probability of getting {x} successes in {n} trials with a success probability of {p} is **{probability:.4f}**")
   
    st.header(f"b({x};{n},{p}) = {probability}")
    
if __name__ == "__main__":
    main()
