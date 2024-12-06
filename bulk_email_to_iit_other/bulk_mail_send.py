import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import pandas as pd
import streamlit as st

st.markdown("""
<style>
    .css-1d391kg {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

st.title("Automatic/Bulk Email sender to IIT Professors/Other")

sender_email = st.text_input("Enter your Email address ")

if sender_email:
    password = st.text_input("Enter your App Password ")
    st.markdown("[FIND YOUR APP PASSWORD](https://www.youtube.com/watch?v=N_J3HCATA1c)")

    if password:
        # Choose file upload or prelist option
        upload_option = st.radio("Choose how to provide recipients", ("Upload File (Excel/CSV)", "Predefined IIT List", "Enter Other Emails"))

        recipients = []

        if upload_option == "Upload File (Excel/CSV)":
            uploaded_file = st.file_uploader("Choose your File (Excel/CSV) with Name and Email", type=["csv", "xlsx"])

            if uploaded_file is not None:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith('.xlsx'):
                    df = pd.read_excel(uploaded_file)

                if "name" in df.columns and "email" in df.columns:
                    recipients = df[['name', 'email']].values.tolist()
                else:
                    st.error("The file must contain 'name' and 'email' columns.")

        elif upload_option == "Predefined IIT List":
            # Predefined IIT email list
            iit_recipients = [
            "shwetaag@cse.iitm.ac.in", "sanjiva@cse.iitd.ac.in", "adsul@cse.iitb.ac.in", "bala@cs.iitr.ac.in", 
            "bhij@cse.iitkgp.ac.in", "anand.ashish@iitg.ac.in", "antony.franklin@cse.iith.ac.in", 
            "aktripathi.cse@iitbhu.ac.in", "ananthap@cse.iitm.ac.in", "aseth@cse.iitd.ac.in", 
            "varsha@cse.iitb.ac.in", "sugata.gangopadhyay@cs.iitr.ac.in", "abhijnan@cse.iitkgp.ac.in", 
            "awekar@iitg.ac.in", "mishraashish@cse.iith.ac.in", "sks.cse@iitbhu.ac.in", "sutanuc@cse.iitm.ac.in", 
            "ajindal@cse.iitd.ac.in", "kavi@cse.iitb.ac.in", "sandeep.garg@cs.iitr.ac.in", "abir@cse.iitkgp.ac.in", 
            "r.duttabaruah@iitg.ac.in", "tbr@cse.iith.ac.in", "aksingh.cse@iitbhu.ac.in", "sdas@cse.iitm.ac.in", 
            "amitk@cse.iitd.ac.in", "suyash@cse.iitb.ac.in", "chetan.gupta@cs.iitr.ac.in", "animeshm@cse.iitkgp.ac.in", 
            "pbhaduri@iitg.ac.in", "ckm@cse.iith.ac.in", "bhaskar.cse@iitbhu.ac.in", "djram@cse.iitm.ac.in", 
            "bagchi@cse.iitd.ac.in", "umesh@cse.iitb.ac.in", "shahbaz.khan@cs.iitr.ac.in", "aritrah@cse.iitkgp.ac.in", 
            "sukantab@iitg.ac.in", "saketha@cse.iith.ac.in", "bidyut.cse@iitbhu.ac.in", "miteshk@cse.iitm.ac.in", 
            "ashishc@cse.iitd.ac.in", "pb@cse.iitb.ac.in", "aparajita.khan@cs.iitr.ac.in", "agupta@cse.iitkgp.ac.in", 
            "samit@iitg.ac.in", "jyothiv@cse.iith.ac.in", "ravi.cse@iitbhu.ac.in", "psk@cse.iitm.ac.in", 
            "chetan@cse.iitd.ac.in", "sujoy@cse.iitb.ac.in", "sateesh@cs.iitr.ac.in", "ayanc@cse.iitkgp.ac.in", 
            "pkdas@iitg.ac.in", "kotaro@cse.iith.ac.in", "rchowdary.cse@iitbhu.ac.in", "amitta@cse.iitm.ac.in", 
            "saran@cse.iitd.ac.in", "soumen@cse.iitb.ac.in", "neetesh@cs.iitr.ac.in", "bivas@cse.iitkgp.ac.in", 
            "jatin@iitg.ac.in", "mvp@cse.iith.ac.in", "rgupta.cse@iitbhu.ac.in", "madhu@cse.iitm.ac.in", 
            "kbeedkar@cse.iitd.ac.in", "supratik@cse.iitb.ac.in", "manoj.misra@cs.iitr.ac.in", 
            "chitta@cse.iitkgp.ac.in", "dgoswami@iitg.ac.in", "msingh@cse.iith.ac.in", "spal.cse@iitbhu.ac.in", 
            "nvk@cse.iitm.ac.in", "keerti@cse.iitd.ac.in", "sharat@cse.iitb.ac.in", "rajdeep.niyogi@cs.iitr.ac.in", 
            "dsamanta@cse.iitkgp.ac.in", "rinkulu@iitg.ac.in", "mariaf@cse.iith.ac.in", "tanima.cse@iitbhu.ac.in", 
            "swamy@cse.iitm.ac.in", "kolin@cse.iitd.ac.in", "paragc@cse.iitb.ac.in", "ap@cs.iitr.ac.in", 
            "debdeep@cse.iitkgp.ac.in", "johnjose@iitg.ac.in", "maunendra@cse.iith.ac.in", "ajay.cse@iitbhu.ac.in", 
            "meghana@cse.iitm.ac.in", "madhukar@cse.iitd.ac.in", "chebrolu@cse.iitb.ac.in", "rajdeep.niyogi@cs.iitr.ac.in", 
            "drc@cse.iitkgp.ac.in", "ben@iitg.ac.in", "aravind@cse.iith.ac.in", "prashla@cse.iitm.ac.in", 
            "mausam@cse.iitd.ac.in", "damani@cse.iitb.ac.in", "partha@cs.iitr.ac.in", "isg@cse.iitkgp.ac.in", 
            "hemangee@iitg.ac.in", "nitin@cse.iith.ac.in", "amrita.cse@iitbhu.ac.in", "bvrr@cse.iitm.ac.in", 
            "ramanath@cse.iitd.ac.in", "abir@cse.iitb.ac.in", "sudip.roy@cs.iitr.ac.in", "jay@cse.iitkgp.ac.in", 
            "ckarfa@iitg.ac.in", "praveent@cse.iith.ac.in", "indra.cse@iitbhu.ac.in", "chester@cse.iitm.ac.in", 
            "naveen@cse.iitd.ac.in", "aad@cse.iitb.ac.in", "rajat.sadhukhan@cs.iitr.ac.in", "jibesh@cse.iitkgp.ac.in", 
            "sushantak@iitg.ac.in", "rkedia@cse.iith.ac.in", "oslbhavana.cse@iitbhu.ac.in", "chandra@cse.iitm.ac.in", 
            "nbalaji@cse.iitd.ac.in", "dgosain@cse.iitb.ac.in", "raksha.sharma@cs.iitr.ac.in", "ksrao@cse.iitkgp.ac.in", 
            "deepkesh@iitg.ac.in", "rakesh@cse.iith.ac.in", "prasenjit.cse@iitbhu.ac.in", "sgopal@cse.iitm.ac.in", 
            "parags@cse.iitd.ac.in", "ashwin@cse.iitb.ac.in", "pravendra.singh@cs.iitr.ac.in", "mainack@cse.iitkgp.ac.in", 
            "manaskhatua@iitg.ac.in", "ramakrishna@cse.iith.ac.in", "pratik.cse@iitbhu.ac.in", "yadu@cse.iitm.ac.in", 
            "panda@cse.iitd.ac.in", "akg@cse.iitb.ac.in", "dharmfec@cs.iitr.ac.in", "monosij@cse.iitkgp.ac.in", 
            "pinaki@iitg.ac.in", "rameshwar@cse.iith.ac.in", "vignesh.cse@iitbhu.ac.in", "akanksha@cse.iitm.ac.in", 
            "pgolia@cse.iitd.ac.in", "rgurjar@cse.iitb.ac.in", "jsingla@cs.iitr.ac.in", "niloy@cse.iitkgp.ac.in", 
            "sbnair@iitg.ac.in", "rogers@cse.iith.ac.in", "vsrivastava.cse@iitbhu.ac.in", "augustine@cse.iitm.ac.in", 
            "jaiswal@cse.iitd.ac.in", "rkj@cse.iitb.ac.in", "rahul.thakur@cs.iitr.ac.in", "pabitra@cse.iitkgp.ac.in", 
            "sukumar@iitg.ac.in", "sathya_p@cse.iith.ac.in", "ayon@cse.iitm.ac.in", "rahulgarg@cse.iitd.ac.in", 
            "pjyothi@cse.iitb.ac.in", "durga.toshniwal@cs.iitr.ac.in", "palash.dey@cse.iitkgp.ac.in", 
            "moumita.patra@iitg.ac.in", "saurabhkr@cse.iith.ac.in", "hariguru@cse.iitm.ac.in", "narain@cse.iitd.ac.in", 
            "shivaram@cse.iitb.ac.in", "pallab@cse.iitkgp.ac.in", "svrao@iitg.ac.in", "shirshendu@cse.iith.ac.in", 
            "kama@cse.iitm.ac.in", "r_kumar@cse.iitd.ac.in", "ckamath@cse.iitb.ac.in", "pb@cse.iitkgp.ac.in", 
            "asahu@iitg.ac.in", "sobhan@cse.iith.ac.in", "nishad@cse.iitm.ac.in", "riju@cse.iitd.ac.in", 
            "uday@cse.iitb.ac.in", "ppchak@cse.iitkgp.ac.in", "sajith@iitg.ac.in", "srijith@cse.iith.ac.in", 
            "chandrasheka@cse.iitm.ac.in", "rohan@cse.iitd.ac.in", "puru@cse.iitb.ac.in", "pawang@cse.iitkgp.ac.in", 
            "saradhi@iitg.ac.in", "subruk@cse.iith.ac.in", "murthy@cse.iitm.ac.in", "rvaish@cse.iitd.ac.in", 
            "akash@cse.iitb.ac.in", "pralay@cse.iitkgp.ac.in", "ranbir@iitg.ac.in", "vineethnb@cse.iith.ac.in", 
            "nagark@cse.iitm.ac.in", "sayanranu@cse.iitd.ac.in", "nutan@cse.iitb.ac.in", 
            "rschakraborty@cse.iitkgp.ac.in", "arijit@iitg.ac.in", "nmanik@cse.iitm.ac.in", "srsarangi@cse.iitd.ac.in", 
            "krishnas@cse.iitb.ac.in", "sandipc@cse.iitkgp.ac.in", "phrangboklang@iitg.ac.in", "rupesh@cse.iitm.ac.in", 
            "sbansal@cse.iitd.ac.in", "swaprava@cse.iitb.ac.in", "saptarshi@cse.iitkgp.ac.in", "t.venkat@iitg.ac.in", 
            "shreyas@cse.iitm.ac.in", "srikanta@cse.iitd.ac.in", "biswa@cse.iitb.ac.in", "sarani@cse.iitkgp.ac.in", 
            "arunr@cse.iitm.ac.in", "subodh@cse.iitd.ac.in", "mp@cse.iitb.ac.in", "shamik@cse.iitkgp.ac.in", 
            "ravi@cse.iitm.ac.in", "svs@cse.iitd.ac.in", "ajitvr@cse.iitb.ac.in", "saditya@cse.iitkgp.ac.in", 
            "jayalal@cse.iitm.ac.in", "tmangla@cse.iitd.ac.in", "br@cse.iitb.ac.in", "somindu@cse.iitkgp.ac.in", 
            "skrishnam@cse.iitm.ac.in", "vaishnavi@cse.iitd.ac.in", "ganesh@cse.iitb.ac.in", "skg@cse.iitkgp.ac.in", 
            "aishwarya@cse.iitm.ac.in", "kvenkata@cse.iitd.ac.in", "ranade@cse.iitb.ac.in", "soumya@cse.iitkgp.ac.in", 
            "viresh@cse.iitd.ac.in", "vinayr@cse.iitb.ac.in", "sourangshu@cse.iitkgp.ac.in", "akshayss@cse.iitb.ac.in", 
            "ssp@cse.iitkgp.ac.in", "sayandeepsaha@cse.iitb.ac.in", "sudeshna@cse.iitkgp.ac.in", "sunita@cse.iitb.ac.in", 
            "skolay@cse.iitkgp.ac.in", "sruthi@cse.iitb.ac.in", "smisra@cse.iitkgp.ac.in", "surajs@cse.iitb.ac.in"]
            
            recipients = [(email.split('@')[0], email) for email in iit_recipients]

        elif upload_option == "Enter Other Emails":
            other_recipients = st.text_input("Enter the Recipient Emails (separated by commas)")
            if other_recipients:
                recipients = [(email.strip(), email.strip()) for email in other_recipients.split(',')]
        print(recipients)
        # Subject and body inputs
        subject = st.text_input("Enter your Subject ")
        body = st.text_area("Write the Body", height=300)

        uploaded_file_attach = st.file_uploader("Choose a file to attach", type=["pdf"])

        if st.button("CLICK TO SEND 👌") and len(recipients) > 0:
            try:
                # Setting up the SMTP server and login
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()  
                server.login(sender_email, password)

                # Send email
                for i, (name, recipient_email) in enumerate(recipients, 1):
                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = recipient_email
                    msg['Subject'] = subject

                    msg.attach(MIMEText(body, 'plain'))

                    if uploaded_file_attach is not None:
                        part = MIMEApplication(uploaded_file_attach.read(), _subtype="pdf")
                        part.add_header('Content-Disposition', 'attachment', filename=uploaded_file_attach.name)
                        msg.attach(part)

                    # Send the email
                    server.sendmail(sender_email, recipient_email, msg.as_string())
                    st.write(f"{i} mail sent to {name}.")

                st.success("All Emails sent successfully!")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                server.quit()

        st.write("Special thanks to Baibhav for providing IIT Emails.")
