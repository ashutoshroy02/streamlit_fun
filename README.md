# Python Applications

This repository contains three Streamlit-based applications:

## 1. **YouTube Playlist Downloader (`ytdown.py`)**
- **Description**: A tool to download videos from a YouTube playlist.
- **Features**:
  - Specify a playlist link.
  - Select the range of episodes to download.
  - Define the download location.
- **Usage**:
  Run the script, input required details in the Streamlit interface, and click "Download Videos."

---

## 2. **Betting Calculator (`qwq.py`)**
- **Description**: A calculator for simulating progressive betting strategies.
- **Features**:
  - Set wallet balance, initial bet, and percentage increase on loss.
  - Simulate consecutive bets until the wallet balance is depleted.
  - View total bets, number of bets, and remaining balance.
- **Usage**:
  Input the required parameters in the Streamlit interface to see detailed results.

---

## 3. **Intrusive Calculators (`intrusive.py`)**
- **Description**: A multi-functional application with:
  - **Binomial Calculator**: Calculate probabilities for binomial distributions.
  - **Poisson Calculator**: Compute probabilities for Poisson distributions.
  - **Birthday Facts**: Discover fun facts based on your birthday.
- **Usage**:
  Select a calculator from the sidebar, provide inputs, and view the results.

---

### Requirements
- Python 3.x
- Streamlit
- Additional dependencies:
  - `pytube-fix` (for `ytdown.py`)

### How to Run
1. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
2. Run any script using Streamlit:  
   ```bash
   streamlit run <script_name>.py
   ```

### License
This project is open-source under the MIT License.

---
