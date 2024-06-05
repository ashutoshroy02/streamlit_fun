import streamlit as st
st.title("Stake")

bet = st.number_input("Enter Bet: ",value=0.00)

increase_on_loss = st.number_input("Percent increase on loss: ",value=0.00)

no_of_bet = st.number_input("number of Bet: ",value=0)

betting=[]

for i in range(no_of_bet):
    bet = bet + (increase_on_loss*bet/100)
    betting.append(bet)
    
if betting:
    formatted_float = f"{betting[-1]:.6f}"
    st.write(f"last bet : {formatted_float}")
    
st.write(f"Total Sum of BET: {sum(betting):.4f}")