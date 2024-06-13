# import streamlit as st
# st.title("Stake")

# bet = st.number_input("Enter Bet: ",value=0.00)

# increase_on_loss = st.number_input("Percent increase on loss: ",value=0.00)

# no_of_bet = st.number_input("number of Bet: ",value=0)

# betting=[]

# for i in range(no_of_bet):
#     bet = bet + (increase_on_loss*bet/100)
#     betting.append(bet)
#     st.write(bet)

# if betting:
#     formatted_float = f"{betting[-1]:.6f}"
#     st.write(f"last bet : {formatted_float}")
    
# st.write(f"Total Sum of BET: {sum(betting):.4f}")



import streamlit as st

st.title("Stake")

wallet_balance = st.number_input("Enter Wallet Balance: ", value=0.00)
initial_bet = st.number_input("Enter Initial Bet: ", value=0.00)
increase_on_loss = st.number_input("Percent increase on loss: ", value=0.00)

betting = []
current_bet = initial_bet
remaining_balance = wallet_balance


# Calculate the number of bets you can play based on wallet balance
while remaining_balance >= current_bet:
    betting.append(current_bet)
    remaining_balance -= current_bet
    st.write(f"Bet {len(betting)}: {current_bet:.2f}")
    current_bet += (increase_on_loss * current_bet / 100)


if betting:
    formatted_float = f"{betting[-1]:.3f}"
    st.write(f"Last bet : {formatted_float}")
    
    
st.write(f"Total Sum of Bets: {sum(betting):.4f}")
st.write(f"Number of Bets: {len(betting)}")
st.write(f"Remaining Balance: {remaining_balance:.2f}")
