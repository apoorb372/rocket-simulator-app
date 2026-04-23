import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Rocket Simulator Pro", layout="centered")

st.title("🚀 Rocket Simulator PRO")

# -----------------------
# INPUTS
# -----------------------
velocity = st.slider("Velocity (m/s)", 10, 200, 50)
angle = st.slider("Angle (degrees)", 0, 90, 45)
Cd = st.slider("Drag Coefficient", 0.1, 1.5, 0.47)

g = 9.81
theta = np.radians(angle)

# -----------------------
# WITHOUT AIR RESISTANCE
# -----------------------
t = np.linspace(0, (2 * velocity * np.sin(theta)) / g, 200)

x1 = velocity * np.cos(theta) * t
y1 = velocity * np.sin(theta) * t - 0.5 * g * t**2

# -----------------------
# WITH AIR RESISTANCE
# -----------------------
dt = 0.1
rho = 1.225
A = 0.01
m = 1.0

vx = velocity * np.cos(theta)
vy = velocity * np.sin(theta)

x, y = 0, 0
x2, y2 = [], []

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

    x2.append(x)
    y2.append(y)

# -----------------------
# RESULTS
# -----------------------
max_h1 = np.max(y1)
range1 = np.max(x1)

max_h2 = max(y2)
range2 = max(x2)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 No Air Resistance")
    st.write(f"Max Height: {round(max_h1,2)} m")
    st.write(f"Range: {round(range1,2)} m")

with col2:
    st.subheader("🌪️ With Air Resistance")
    st.write(f"Max Height: {round(max_h2,2)} m")
    st.write(f"Range: {round(range2,2)} m")

# -----------------------
# BEST ANGLE PREDICTOR
# -----------------------
def find_best_angle(v, Cd):
    best_range = 0
    best_angle = 0

    for ang in range(10, 80):
        theta = np.radians(ang)
        vx = v * np.cos(theta)
        vy = v * np.sin(theta)

        x, y = 0, 0
        dt = 0.1
        x_temp = []

        while y >= 0:
            vel = np.sqrt(vx**2 + vy**2)
            if vel == 0:
                break

            Fd = 0.5 * Cd * rho * A * vel**2

            Fdx = Fd * (vx / vel)
            Fdy = Fd * (vy / vel)

            ax = -Fdx / m
            ay = -g - (Fdy / m)

            vx += ax * dt
            vy += ay * dt

            x += vx * dt
            y += vy * dt

            x_temp.append(x)

        if len(x_temp) > 0 and max(x_temp) > best_range:
            best_range = max(x_temp)
            best_angle = ang

    return best_angle

best_angle = find_best_angle(velocity, Cd)

st.success(f"🚀 Best Angle for Maximum Range ≈ {best_angle}°")

# -----------------------
# PLOT
# -----------------------
fig, ax = plt.subplots()

ax.plot(x1, y1, label="No Air Resistance")
ax.plot(x2, y2, label="With Air Resistance")

ax.set_title("Trajectory Comparison")
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Height (m)")
ax.legend()
ax.grid()

st.pyplot(fig)