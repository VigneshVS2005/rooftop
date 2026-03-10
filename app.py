import streamlit as st
import pandas as pd
import math
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Pro Solar PV Designer", 
    page_icon="☀️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
# Adds a bit of styling to make metrics pop
st.markdown("""
    <style>
    div[data-testid="metric-container"] {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    [data-theme="dark"] div[data-testid="metric-container"] {
        background-color: #262730;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: INPUTS & CONTROLS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3565/3565400.png", width=80) # Generic solar icon
    st.title("System Controls")
    
    with st.expander("🛠️ 1. Load Profile", expanded=True):
        daily_energy_wh = st.number_input("Daily Energy (Wh/day)", value=3800, step=100)
        peak_load_w = st.number_input("Peak Load (W)", value=875, step=25)

    with st.expander("🌤️ 2. Solar & Site Details", expanded=True):
        sunshine_hours = st.slider("Sunshine Hours", 1.0, 10.0, 5.0, 0.5)
        panel_rating_w = st.number_input("Panel Rating (W)", value=80, step=10)
        system_voltage = st.selectbox("System Voltage (V)", options=[12, 24, 48], index=1)

    st.markdown("---")
    st.header("🚀 Technological Innovations")
    st.markdown("Toggle modern components to optimize the lab's base design.")
    use_mppt = st.toggle("Use MPPT Controller", help="Improves operating factor from 0.8 to 0.95")
    use_lithium = st.toggle("Use Lithium-Ion Battery", help="Improves Depth of Discharge (DoD) from 70% to 90%")
    use_smart_inv = st.toggle("Use Smart Inverter", help="Improves grid support and efficiency")
    use_ai_ems = st.toggle("AI Energy Management", help="Shifts non-critical loads to peak sun hours")

# --- CORE CALCULATIONS ENGINE ---
# Constant Efficiencies
inv_eff = 0.95
bat_eff = 0.85
ctrl_eff = 0.95

# 1. Inverter Math
inv_safety_margin = 1.25
inverter_kw = round((peak_load_w * inv_safety_margin) / 1000, 1)
inverter_input_energy = daily_energy_wh / inv_eff

# 2. Battery Math (Baseline vs Optimized)
baseline_dod = 0.70
current_dod = 0.90 if use_lithium else baseline_dod

required_ah_total = inverter_input_energy / system_voltage
baseline_battery_ah = required_ah_total / baseline_dod
current_battery_ah = required_ah_total / current_dod

# 3. Panel Math (Baseline vs Optimized)
baseline_op_factor = 0.80
current_op_factor = 0.95 if use_mppt else baseline_op_factor

pv_energy_req = inverter_input_energy / (bat_eff * ctrl_eff)
pv_power_req_w = pv_energy_req / sunshine_hours

baseline_array_w = pv_power_req_w / baseline_op_factor
current_array_w = pv_power_req_w / current_op_factor

baseline_panels = math.ceil(baseline_array_w / panel_rating_w)
current_panels = math.ceil(current_array_w / panel_rating_w)


# --- MAIN UI AREA ---
st.title("☀️ Rooftop Solar PV System Designer")
st.caption("Interactive modeling tool based on conventional design principles vs. modern technological innovations.")

# Create Navigation Tabs
tab1, tab2, tab3 = st.tabs(["📊 Executive Dashboard", "📈 Visual Comparisons", "📝 Load & Lab Data"])

with tab1:
    st.subheader("System Sizing Summary")
    st.markdown("Real-time sizing based on your selected parameters and innovations.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="⚡ Required Inverter", 
            value=f"{inverter_kw} kW", 
            delta="Smart Inverter Active" if use_smart_inv else "Standard Inv.",
            delta_color="normal" if use_smart_inv else "off"
        )
        
    with col2:
        # Calculate Ah saved
        ah_saved = math.ceil(baseline_battery_ah) - math.ceil(current_battery_ah)
        st.metric(
            label=f"🔋 Battery Capacity ({system_voltage}V)", 
            value=f"{math.ceil(current_battery_ah)} Ah",
            delta=f"-{ah_saved} Ah saved vs Lead-Acid" if use_lithium else "Standard Lead-Acid (70% DoD)",
            delta_color="inverse" if use_lithium else "off" # Inverse because lower is better
        )
        
    with col3:
        # Calculate panels saved
        panels_saved = baseline_panels - current_panels
        st.metric(
            label=f"☀️ Total PV Panels ({panel_rating_w}W)", 
            value=f"{current_panels}",
            delta=f"-{panels_saved} panels vs PWM" if use_mppt else "Standard PWM (0.8 OF)",
            delta_color="inverse" if use_mppt else "off" # Inverse because lower is better
        )
        
    # Impact Notification
    if any([use_mppt, use_lithium, use_smart_inv, use_ai_ems]):
        st.success("**🚀 System Optimized!** You are viewing an advanced setup. Check the *Visual Comparisons* tab to see the material savings.")
    else:
        st.info("**💡 Baseline Design Active.** Toggle the switches in the sidebar to see how modern technology reduces component sizes!")

with tab2:
    st.subheader("Conventional vs. Innovative Sizing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Panel Comparison Chart
        df_panels = pd.DataFrame({
            "Design Type": ["Conventional (Lab)", "Optimized (Current)"],
            "Number of Panels": [baseline_panels, current_panels]
        })
        fig_panels = px.bar(
            df_panels, x="Design Type", y="Number of Panels", 
            color="Design Type", text="Number of Panels",
            color_discrete_map={"Conventional (Lab)": "#ef553b", "Optimized (Current)": "#00cc96"},
            title="PV Array Size Reduction"
        )
        fig_panels.update_traces(textposition='auto')
        st.plotly_chart(fig_panels, use_container_width=True)

    with col2:
        # Battery Comparison Chart
        df_battery = pd.DataFrame({
            "Design Type": ["Conventional (Lab)", "Optimized (Current)"],
            "Battery Capacity (Ah)": [math.ceil(baseline_battery_ah), math.ceil(current_battery_ah)]
        })
        fig_battery = px.bar(
            df_battery, x="Design Type", y="Battery Capacity (Ah)", 
            color="Design Type", text="Battery Capacity (Ah)",
            color_discrete_map={"Conventional (Lab)": "#636efa", "Optimized (Current)": "#ab63fa"},
            title="Battery Bank Size Reduction"
        )
        fig_battery.update_traces(textposition='auto')
        st.plotly_chart(fig_battery, use_container_width=True)

with tab3:
    st.subheader("📋 Laboratory Load Details")
    st.write("This table represents the baseline connected load from Experiment 2.")
    
    # Static Data from Lab
    load_data = {
        "Appliance": ["CFL", "Fan", "TV", "Computer", "Refrigerator"],
        "Power Rating (W)": [75, 300, 100, 250, 150],
        "Usage (Hours/day)": [4, 3, 3, 2, 12],
        "Energy Consumed (Wh)": [300, 900, 300, 500, 1800]
    }
    df_load = pd.DataFrame(load_data)
    
    st.dataframe(df_load, use_container_width=True, hide_index=True)
    
    st.markdown("""
    ### 🧮 Mathematical Breakdown
    *   **Total Daily Energy:** $\sum (Power \\times Hours) = 3800 \\text{ Wh/day}$
    *   **Inverter Input Energy:** $3800 \\text{ Wh} / 0.95 \\text{ (efficiency)} = 4000 \\text{ Wh}$
    *   **Energy from PV to Controller:** $4000 \\text{ Wh} / (0.85 \\times 0.95) = 4954 \\text{ Wh}$
    """)