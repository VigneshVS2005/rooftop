# ☀️ Rooftop Solar PV System Designer Dashboard

An interactive, web-based dashboard built with Python and Streamlit that digitizes and automates the manual calculations from **Experiment – 2: Design of a Rooftop Solar PV System**. 

Instead of calculating system requirements by hand, this app allows users to input their daily energy needs and instantly get the precise hardware requirements for an off-grid solar power system, while also comparing conventional textbook designs against modern technological innovations.

## 🚀 Features

*   **Automated System Sizing:** Instantly calculates the three most critical components of a solar setup based on the user's load profile:
    *   **Inverter Rating (kW):** To handle peak power draw.
    *   **Battery Bank Capacity (Ah):** To store sufficient energy for nighttime or cloudy days.
    *   **PV Array Size (Number of Panels):** To generate enough power during peak sunshine hours.
*   **Dynamic Inputs:** Use interactive sliders and input boxes to adjust sunshine hours, panel wattage, system voltage, and daily energy requirements to see real-time updates.
*   **Lab vs. Real-World Innovations:** Toggle modern technologies to see how they directly improve the baseline conventional design taught in the lab:
    *   *MPPT Charge Controllers* vs. Standard PWM
    *   *Lithium-Ion Batteries (90% DoD)* vs. Lead-Acid (70% DoD)
    *   *Smart Inverters* & *AI Energy Management*
*   **Interactive Visualizations:** Powered by Plotly, the app provides visual proof (via dynamic bar charts) of how modern upgrades reduce the physical footprint of the panels and battery banks.

## 🛠️ Built With

*   [Streamlit](https://streamlit.io/) - The web framework used
*   [Pandas](https://pandas.pydata.org/) - For data manipulation and tables
*   [Plotly](https://plotly.com/python/) - For interactive charting

## 💻 How to Run Locally

If you want to run this project on your own machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/solar-pv-dashboard.git](https://github.com/yourusername/solar-pv-dashboard.git)
   cd solar-pv-dashboard
