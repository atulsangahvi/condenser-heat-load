import streamlit as st
from CoolProp.CoolProp import PropsSI

st.title("Refrigerant Heat Load Calculator (R134a & R407C)")

# User Inputs
fluid = st.selectbox("Select Refrigerant", ["R134a", "R407C"])
P_cond_bar = st.number_input("Condensing Pressure (bar abs)", value=23.52, min_value=1.0, max_value=35.0, step=0.1)
T_superheat = st.number_input("Inlet Superheated Temp (°C)", value=95.0)
T_subcool = st.number_input("Outlet Subcooled Liquid Temp (°C)", value=52.7)
m_dot = st.number_input("Mass Flow Rate (kg/s)", value=0.599)

# Convert to required units
P_cond = P_cond_bar * 1e5  # Pa
T1 = T_superheat + 273.15  # K
T3 = T_subcool + 273.15    # K

try:
    # Enthalpies from CoolProp
    h1 = PropsSI("H", "P", P_cond, "T", T1, fluid)          # Superheated vapor
    h2 = PropsSI("H", "P", P_cond, "Q", 1, fluid)           # Saturated vapor
    h3 = PropsSI("H", "P", P_cond, "Q", 0, fluid)           # Saturated liquid
    h4 = PropsSI("H", "P", P_cond, "T", T3, fluid)          # Subcooled liquid

    # Heat loads (J/kg)
    q_sensible = h1 - h2
    q_latent = h2 - h3
    q_subcool = h3 - h4

    # Convert to kW
    Q_sensible = m_dot * q_sensible / 1000
    Q_latent = m_dot * q_latent / 1000
    Q_subcool = m_dot * q_subcool / 1000
    Q_total = Q_sensible + Q_latent + Q_subcool

    # Display results
    st.subheader("Heat Load Results")
    st.write(f"**Sensible Cooling:** {Q_sensible:.2f} kW")
    st.write(f"**Latent Condensation:** {Q_latent:.2f} kW")
    st.write(f"**Subcooling:** {Q_subcool:.2f} kW")
    st.write(f"**Total Heat Removed:** {Q_total:.2f} kW")

except Exception as e:
    st.error(f"Calculation error: {e}")
