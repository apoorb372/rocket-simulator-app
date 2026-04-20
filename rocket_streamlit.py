import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title("🚀 Rocket Simulator (With Air Resistance)")

# Sidebar inputs
velocity = st.slider("Velocity (m/s)", 10, 200, 50)
angle = st.slider("Angle (degrees)", 0, 90, 45)
Cd = st.slider("Drag Coefficient (Cd)", 0.1, 1.5, 0.47)

# Constants
g = 9.81
dt = 0.1
rho = 1.225
A = 0.01
m = 1.0

theta = np.radians(angle)

# Initial velocity
vx = velocity * np.cos(theta)
vy = velocity * np.sin(theta)

x, y = 0, 0
x_vals = []
y_vals = []

# Simulation loop
while y >= 0:
    v = np.sqrt(vx**2 + vy**2)
    if v == 0:
        break

    Fd = 0.5 * Cd * rho * A * v**2

    Fdx = Fd * (vx / v)
    Fdy = Fd * (vy / v)

    ax = -Fdx / m
    ay = -g - (Fdy / m)

    vx += ax * dt
    vy += ay * dt

    x += vx * dt
    y += vy * dt

    x_vals.append(x)
    y_vals.append(y)

# Results
max_height = max(y_vals)
range_distance = max(x_vals)

st.write(f"### 📊 Max Height: {round(max_height,2)} m")
st.write(f"### 📏 Range: {round(range_distance,2)} m")

# Plot
fig, ax = plt.subplots()
ax.plot(x_vals, y_vals, label="Trajectory")

max_index = y_vals.index(max_height)
ax.scatter(x_vals[max_index], max_height)
ax.text(x_vals[max_index], max_height, " Max Height")

ax.set_title("Rocket Trajectory")
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Height (m)")
ax.legend()
ax.grid()

st.pyplot(fig)