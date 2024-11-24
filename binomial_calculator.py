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
        "which to use?",
   ("Binomial calculator","Poisson calculator","Birthdate Fact")
   )
    if choice == "Binomial calculator":
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
    elif choice == "Poisson calculator":
            st.title("Poisson Distribution Calculator")

            x = st.number_input("Enter the number of trials ", min_value=0, step=1, value=5)
            μ = float(st.number_input("Enter the mean ", min_value=0, value=10))

            #calculation
            e = 2.71828182845
            poisson = (e**(-μ) * (μ)**x)/fact(x)
            st.write(f"The probability is **{poisson:.4f}**")
            st.header(f"p({x};{μ}) = {poisson}")
    elif choice == "Birthdate Fact":
        st.title("🎉 Birthday Calculator - Fun Facts About You!")

        # Input: User's birthday
        birth_date = st.date_input("Enter your birthday:", value=datetime(2003, 6, 22).date())
    
        # Ensure today's date is a `date` object
        today = datetime.now().date()
    
        # Create next_birthday as a `date` object
        next_birthday = datetime(today.year, birth_date.month, birth_date.day).date()
        if next_birthday < today:
            next_birthday = datetime(today.year + 1, birth_date.month, birth_date.day).date()
    
        # Calculate days to next birthday
        days_to_next_birthday = (next_birthday - today).days
        days_since_last_birthday = (today - (next_birthday - timedelta(days=365))).days
    
        # Calculate age
        age_days = (today - birth_date).days
        age_years = age_days // 365
        age_months = age_years * 12 + today.month - birth_date.month
    
        # Outputs
        st.write(f"🎂 **Days to Next Birthday:** {days_to_next_birthday} days")
        st.write(f"🗓️ **Days Since Last Birthday:** {days_since_last_birthday} days")
        st.write(f"📆 **Age in Days:** {age_days} days")
        st.write(f"👶 **Age in Years:** {age_years} years")
        
        # Output: Birthday stats
        st.subheader(f"You were born on {birth_date.strftime('%A, %B %d, %Y')}.")
        st.write(f"🎂 **Days to Next Birthday:** {days_to_next_birthday} days")
        st.write(f"🗓️ **Days Since Last Birthday:** {days_since_last_birthday} days")
        st.write(f"👶 **Your Exact Age:** {age_years} years, {floor(age_months % 12)} months, and {today.day - birth_date.day} days")
        st.write(f"📆 Or in other formats:")
        st.write(f"- {age_months} months old")
        st.write(f"- {age_weeks} weeks old")
        st.write(f"- {age_days} days old")
        st.write(f"- {age_hours:,} hours old")
        st.write(f"- {age_minutes:,} minutes old")
        st.write(f"- {age_seconds:,} seconds old")
        
        # Animal ages
        dog_years = age_years * 7
        cat_years = age_years * 5
        rabbit_years = age_years * 12
        elephant_years = age_years * 0.5
        bee_years = age_years * 1000
        
        st.subheader("🐾 If you were an animal, you'd be:")
        st.write(f"- **{dog_years} years old as a dog**")
        st.write(f"- **{cat_years} years old as a cat**")
        st.write(f"- **{rabbit_years} years old as a rabbit**")
        st.write(f"- **{elephant_years:.1f} years old as an elephant**")
        st.write(f"- **{bee_years:,} years old as a bee**")
        
        # Zodiac signs and attributes
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
        
        for sign, (start_month, start_day, end_month, end_day) in zodiac_signs.items():
            if (birth_date.month == start_month and birth_date.day >= start_day) or (
                birth_date.month == end_month and birth_date.day <= end_day
            ):
                horoscope_sign = sign
                break
        
        st.subheader("🔮 Your Zodiac Sign")
        st.write(f"Your sign is **{horoscope_sign}**.")
        
        # Fun facts
        breaths_taken = age_days * 20 * 60 * 24
        heartbeats = age_days * 80 * 60 * 24
        laughter = age_days * 10
        st.subheader("✨ Fun Facts About You")
        st.write(f"💨 You have taken approximately **{breaths_taken:,} breaths.**")
        st.write(f"❤️ Your heart has beaten around **{heartbeats:,} times.**")
        st.write(f"😂 You have laughed about **{laughter:,} times.**")
        
        # Generations
        generation = "Generation Z (Post-Millennial)" if birth_date.year >= 1997 else "Millennial"
        st.subheader("👨‍👩‍👧 Your Generation")
        st.write(f"You are part of **{generation}**.")
        
        # Age on other planets
        planets = {
            "Mercury": 0.24,
            "Venus": 0.62,
            "Mars": 1.88,
            "Jupiter": 11.86,
            "Saturn": 29.46,
            "Uranus": 84.01,
            "Neptune": 164.79,
            "Pluto": 248.59,
        }
        st.subheader("🌌 Your Age on Other Planets")
        for planet, orbit_years in planets.items():
            planet_age = age_years / orbit_years
            st.write(f"- **{planet}:** {planet_age:.2f} years old")
        
        # Footer
        st.info("🎉 Have fun exploring these fun facts about your birthday and age!")
    
        


if __name__ == "__main__":
    main()
