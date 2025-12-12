import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="CPI Calculator",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    </style>
""", unsafe_allow_html=True)

# Grade points mapping
GRADE_POINTS = {
    'A+': 10, 'A': 9, 'B+': 8, 'B': 7, 
    'C+': 6, 'C': 5, 'F': 0
}

def calculate_spi(df):
    """Calculate Semester Performance Index"""
    if df.empty or df['Credits'].sum() == 0:
        return 0.0
    
    total_credit_grade = 0
    total_credits = 0
    
    for _, row in df.iterrows():
        if row['Grade'] in GRADE_POINTS:
            credit = float(row['Credits']) if row['Credits'] else 0
            grade_point = GRADE_POINTS[row['Grade']]
            total_credit_grade += credit * grade_point
            total_credits += credit
    
    return round(total_credit_grade / total_credits, 2) if total_credits > 0 else 0.0

def calculate_cpi_from_spi(semester_data):
    """Calculate CPI from SPI values"""
    numerator = 0
    denominator = 0
    
    for i, row in semester_data.iterrows():
        spi = float(row['SPI']) if row['SPI'] else 0
        credits = float(row['Total Credits']) if row['Total Credits'] else 0
        
        if i < 2:  # First two semesters (index 0 and 1)
            numerator += 0.5 * credits * spi
            denominator += 0.5 * credits
        else:
            numerator += credits * spi
            denominator += credits
    
    return round(numerator / denominator, 2) if denominator > 0 else 0.0

def get_classification(percentage):
    """Get class based on percentage"""
    if percentage >= 75:
        return "Distinction or Honours", "🏆"
    elif percentage >= 60:
        return "Class I", "🥇"
    elif percentage >= 50:
        return "Class II", "🥈"
    else:
        return "Fail", "❌"

# Title
st.title("🎓 Semester Performance & CPI Calculator")
st.markdown("### Choose your input method:")

# Mode selection
mode = st.radio(
    "Select Mode:",
    ["📊 Enter Subjects (Calculate SPI automatically)", "⚡ Enter SPI directly (Quick CPI calculation)"],
    horizontal=True
)

st.markdown("---")

if mode == "⚡ Enter SPI directly (Quick CPI calculation)":
    st.header("⚡ Quick CPI Calculator")
    st.write("Enter the SPI and total credits for each semester to calculate CPI")
    
    # Initialize session state for quick mode
    if 'quick_semesters' not in st.session_state:
        st.session_state.quick_semesters = pd.DataFrame({
            'Semester': ['Semester 1', 'Semester 2'],
            'Total Credits': [0.0, 0.0],
            'SPI': [0.0, 0.0]
        })
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Add Semester"):
            new_sem_num = len(st.session_state.quick_semesters) + 1
            new_row = pd.DataFrame({
                'Semester': [f'Semester {new_sem_num}'],
                'Total Credits': [0.0],
                'SPI': [0.0]
            })
            st.session_state.quick_semesters = pd.concat([st.session_state.quick_semesters, new_row], ignore_index=True)
            st.rerun()
    
    # Editable table
    edited_semesters = st.data_editor(
        st.session_state.quick_semesters,
        column_config={
            "Semester": st.column_config.TextColumn("Semester", width="medium"),
            "Total Credits": st.column_config.NumberColumn("Total Credits", min_value=0.0, max_value=50.0, step=0.5),
            "SPI": st.column_config.NumberColumn("SPI", min_value=0.0, max_value=10.0, step=0.01, format="%.2f")
        },
        hide_index=True,
        num_rows="dynamic",
        use_container_width=True
    )
    
    st.session_state.quick_semesters = edited_semesters
    
    # Calculate CPI
    cpi = calculate_cpi_from_spi(edited_semesters)
    
    st.markdown("---")
    
    # Display CPI
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%); 
                    padding: 40px; 
                    border-radius: 20px; 
                    text-align: center;
                    box-shadow: 0 8px 16px rgba(0,0,0,0.2);'>
            <h2 style='color: white; margin: 0; font-size: 24px;'>Cumulative Performance Index</h2>
            <h1 style='color: white; font-size: 84px; margin: 20px 0; font-weight: bold;'>{cpi}</h1>
            <p style='color: rgba(255,255,255,0.95); margin: 0; font-size: 16px;'>Based on {len(edited_semesters)} semester(s)</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Show formula
    with st.expander("📐 How CPI is Calculated"):
        st.markdown("""
        **CPI Formula:**
        ```
        CPI = [0.5(C₁×SPI₁) + 0.5(C₂×SPI₂) + Σ(Cᵢ×SPIᵢ) for i≥3] / [0.5(C₁) + 0.5(C₂) + Σ(Cᵢ) for i≥3]
        ```
        
        **Explanation:**
        - First two semesters get 0.5 weightage each
        - From 3rd semester onwards, full weightage is given
        - C = Total Credits for that semester
        - SPI = Semester Performance Index
        """)

else:  # Detailed mode with subjects
    st.header("📊 Detailed Semester Calculator")
    
    # Initialize session state
    if 'semesters_data' not in st.session_state:
        st.session_state.semesters_data = {
            'Semester 1': pd.DataFrame({
                'Subject': [''],
                'Credits': [0.0],
                'Grade': [''],
                'Marks': [0.0]
            })
        }
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Manage Semesters")
        
        # Add new semester
        new_sem_name = st.text_input("New Semester Name", f"Semester {len(st.session_state.semesters_data) + 1}")
        if st.button("➕ Add Semester"):
            if new_sem_name and new_sem_name not in st.session_state.semesters_data:
                st.session_state.semesters_data[new_sem_name] = pd.DataFrame({
                    'Subject': [''],
                    'Credits': [0.0],
                    'Grade': [''],
                    'Marks': [0.0]
                })
                st.success(f"Added {new_sem_name}")
                st.rerun()
        
        st.markdown("---")
        
        # Display grade point system
        st.subheader("📊 Grading System")
        for grade, points in GRADE_POINTS.items():
            st.text(f"{grade}: {points} points")
        
        st.markdown("---")
        st.subheader("📐 SPI Formula")
        st.latex(r"SPI = \frac{\sum(C_i \times G_i)}{\sum C_i}")
        st.caption("C = Credits, G = Grade Points")
    
    # Main content - Semester tabs
    if st.session_state.semesters_data:
        semester_names = list(st.session_state.semesters_data.keys())
        tabs = st.tabs(semester_names)
        
        all_semester_spis = []
        
        for tab, sem_name in zip(tabs, semester_names):
            with tab:
                st.subheader(f"📚 {sem_name}")
                
                # Data editor for subjects
                df = st.session_state.semesters_data[sem_name]
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write("**Enter Subject Details:**")
                with col2:
                    if st.button(f"➕ Add Subject", key=f"add_{sem_name}"):
                        new_row = pd.DataFrame({
                            'Subject': [''],
                            'Credits': [0.0],
                            'Grade': [''],
                            'Marks': [0.0]
                        })
                        st.session_state.semesters_data[sem_name] = pd.concat([df, new_row], ignore_index=True)
                        st.rerun()
                
                # Editable dataframe
                edited_df = st.data_editor(
                    df,
                    column_config={
                        "Subject": st.column_config.TextColumn("Subject Name", width="medium"),
                        "Credits": st.column_config.NumberColumn("Credits", min_value=0.0, max_value=10.0, step=0.5),
                        "Grade": st.column_config.SelectboxColumn("Grade", options=list(GRADE_POINTS.keys())),
                        "Marks": st.column_config.NumberColumn("Marks (out of 100)", min_value=0, max_value=100)
                    },
                    hide_index=True,
                    num_rows="dynamic",
                    use_container_width=True,
                    key=f"editor_{sem_name}"
                )
                
                # Update session state
                st.session_state.semesters_data[sem_name] = edited_df
                
                # Calculate metrics for this semester
                total_marks = edited_df['Marks'].sum()
                max_marks = len(edited_df) * 100
                percentage = (total_marks / max_marks * 100) if max_marks > 0 else 0
                spi = calculate_spi(edited_df)
                total_credits = edited_df['Credits'].sum()
                classification, icon = get_classification(percentage)
                
                all_semester_spis.append({
                    'Semester': sem_name,
                    'Total Credits': total_credits,
                    'SPI': spi
                })
                
                st.markdown("---")
                
                # Display results in columns
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("📝 Total Marks", f"{total_marks:.0f} / {max_marks}")
                
                with col2:
                    st.metric("📊 Percentage", f"{percentage:.2f}%")
                
                with col3:
                    st.metric("🎯 SPI", f"{spi}")
                
                with col4:
                    st.metric(f"{icon} Classification", classification)
        
        # Calculate CPI from all semesters
        semester_df = pd.DataFrame(all_semester_spis)
        cpi = calculate_cpi_from_spi(semester_df)
        
        # Overall CPI Display
        st.markdown("---")
        st.header("🏆 Overall Performance")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 40px; 
                        border-radius: 20px; 
                        text-align: center;
                        box-shadow: 0 8px 16px rgba(0,0,0,0.2);'>
                <h2 style='color: white; margin: 0; font-size: 24px;'>Cumulative Performance Index (CPI)</h2>
                <h1 style='color: white; font-size: 84px; margin: 20px 0; font-weight: bold;'>{cpi}</h1>
                <p style='color: rgba(255,255,255,0.95); margin: 0; font-size: 16px;'>Overall performance across all semesters</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Summary table
        st.markdown("---")
        st.subheader("📋 Semester-wise Summary")
        
        summary_data = []
        for sem_name, df in st.session_state.semesters_data.items():
            total_marks = df['Marks'].sum()
            max_marks = len(df) * 100
            percentage = (total_marks / max_marks * 100) if max_marks > 0 else 0
            spi = calculate_spi(df)
            total_credits = df['Credits'].sum()
            
            summary_data.append({
                'Semester': sem_name,
                'Total Credits': total_credits,
                'Total Marks': f"{total_marks:.0f}/{max_marks}",
                'Percentage': f"{percentage:.2f}%",
                'SPI': spi
            })
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

# Formula reference
with st.expander("📐 Complete Formula Reference"):
    st.markdown("""
    **SPI (Semester Performance Index):**
    ```
    SPI = Σ(Credit × Grade Point) / Σ(Credit)
    ```
    
    **CPI (Cumulative Performance Index):**
    ```
    CPI = [0.5(N₁ + N₂) + ΣNᵢ (i≥3)] / [0.5(D₁ + D₂) + ΣDᵢ (i≥3)]
    ```
    where:
    - N = Total Credits × SPI for each semester
    - D = Total Credits for each semester
    - Semester 1 and 2 are given 0.5 weightage each
    - From Semester 3 onwards, full weightage is given
    
    **Grade Points:**
    - A+: 10, A: 9, B+: 8, B: 7, C+: 6, C: 5, F: 0
    
    **Classification:**
    - Distinction or Honours: ≥75%
    - Class I: 60% - 74%
    - Class II: 50% - 59%
    - Fail: <50%
    """)

st.markdown("---")
st.caption("💡 Tip: Use Quick mode if you already know your SPI for each semester. Use Detailed mode to calculate SPI from subject grades.")
