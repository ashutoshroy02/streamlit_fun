import streamlit as st
from datetime import datetime, timedelta
from math import floor
st.balloons()
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
    choice = st.sidebar.selectbox(
        "Choose a calculator:",
        ("Birthday Facts","Binomial Calculator", "Poisson Calculator")
    )

    if choice == "Binomial Calculator":
        st.title("Binomial Distribution Calculator")

        n = st.number_input("Number of trials (n):", min_value=0, step=1, value=10)
        x = st.number_input("Number of successes (x):", min_value=0, step=1, value=5)
        p = st.slider("Probability of success (p):", min_value=0.0, max_value=1.0, value=0.5, step=0.01)

        probability = binomial_distribution(n, x, p)
        st.write(f"The probability of {x} successes in {n} trials with a success probability of {p} is **{probability:.4f}**")
        st.header(f"b({x}; {n}, {p}) = {probability:.4f}")

    elif choice == "Poisson Calculator":
        st.title("Poisson Distribution Calculator")

        x = st.number_input("Number of events (x):", min_value=0, step=1, value=5)
        μ = st.number_input("Mean (μ):", min_value=0.0, value=10.0)

        e = 2.71828182845
        poisson = (e**(-μ) * μ**x) / factorial(x)
        st.write(f"The probability is **{poisson:.4f}**")
        st.header(f"P({x}; {μ}) = {poisson:.4f}")

    elif choice == "Birthday Facts":
        st.title("🎉 Birthday Calculator - Fun Facts About You!")

        birth_date = st.date_input("Enter your birthday:", value=datetime(2003, 2, 24).date())
        today = datetime.now().date()

        next_birthday = datetime(today.year, birth_date.month, birth_date.day).date()
        if next_birthday < today:
            next_birthday = datetime(today.year + 1, birth_date.month, birth_date.day).date()

        days_to_next_birthday = (next_birthday - today).days
        age_days = (today - birth_date).days
        age_years = age_days // 365
        age_weeks = age_days // 7
        age_months = age_years * 12 + today.month - birth_date.month
        age_hours = age_days * 24
        age_minutes = age_hours * 60
        age_seconds = age_minutes * 60

        st.write(f"🎂 **Days to Next Birthday:** {days_to_next_birthday} days")
        st.write(f"📆 **Your Age in Days:** {age_days}")
        st.write(f"👶 **Exact Age:** {age_years} years, {floor(age_months % 12)} months, and {today.day - birth_date.day} days")
        st.write(f"- **{age_weeks} weeks**")
        st.write(f"- **{age_days} days**")
        st.write(f"- **{age_hours:,} hours**")
        st.write(f"- **{age_minutes:,} minutes**")
        st.write(f"- **{age_seconds:,} seconds**")

        dog_years = age_years * 7
        cat_years = age_years * 5
        rabbit_years = age_years * 12
        st.write(f"🐶 If you were a dog, you'd be **{dog_years} years old.**")

        zodiac_signs = {
            "Aries": (3, 21, 4, 19),
            "Taurus": (4, 20, 5, 20),
            "Gemini": (5, 21, 6, 20),
            "Cancer": (6, 21, 7, 22),
            "Leo": (7, 23, 8, 22),
            "Virgo": (8, 23, 9, 22),
            "Libra": (9, 23, 10, 22),
            "Scorpio": (10, 23, 11, 21),
            "Sagittarius": (11, 22, 12, 21),
            "Capricorn": (12, 22, 1, 19),
            "Aquarius": (1, 20, 2, 18),
            "Pisces": (2, 19, 3, 20),
        }

        horoscope_sign = "Unknown"
        for sign, (start_month, start_day, end_month, end_day) in zodiac_signs.items():
            if (birth_date.month == start_month and birth_date.day >= start_day) or (
                birth_date.month == end_month and birth_date.day <= end_day
            ):
                horoscope_sign = sign
                break

        st.write(f"🔮 Your Zodiac Sign is **{horoscope_sign}.**")

        st.subheader("🎉 Fun Facts")
        st.write(f"💨 Estimated Breaths Taken: **{age_days * 20 * 60 * 24:,}**")
        st.write(f"❤️ Heartbeats: **{age_days * 80 * 60 * 24:,}**")

if __name__ == "__main__":
    main()
