import math
import matplotlib.pyplot as plt

# Constants
g = 9.81  # Acceleration due to gravity (m/s^2)
air_density = 1.225  # Air density at sea level and 15 degrees Celsius (kg/m^3)

# Gun and bullet properties
gun_height = 1  # Height of the gun (m)
initial_bullet_velocity = 365  # Initial speed of the bullet (m/s)
bullet_mass = 0.0095  # Mass of the bullet (kg)
bullet_diameter = 0.009  # Diameter of the bullet (m)
bullet_drag_coefficient = 0.05  # Drag coefficient of the bullet (dimensionless)

# Target properties
target_distance = 100  # Horizontal distance to the target (m)
target_size = 10  # Diameter of the target (m)

# Calculate the bullet's cross-sectional area
bullet_area = math.pi * (bullet_diameter / 2)**2

# Wind properties
wind_speed = 10  # Speed of the wind (m/s)
wind_direction = math.radians(0)  # Direction of the wind (radians)

# Initial conditions
firing_angle = math.radians(60)  # Firing angle (radians)
x = 0  # Initial horizontal position (m)
y = gun_height  # Initial vertical position (m)
v = initial_bullet_velocity  # Initial velocity (m/s)
θ = firing_angle  # Initial angle (radians)

# Time settings
t = 0  # Initial time (s)
dt = 0.01  # Time step (s)

# Lists to store the bullet's trajectory for plotting
x_values = [x]
y_values = [y]

# Function to calculate the derivatives using the Runge-Kutta method
def calculate_derivatives(t, x, y, v, θ):
    # Calculate the wind effect
    wind_effect = wind_speed * math.cos(wind_direction - θ)

    # Calculate the derivatives of the variables
    dxdt = v * math.cos(θ) + wind_effect
    dydt = v * math.sin(θ)
    dvdt = -g * math.sin(θ) - 0.5 * air_density * v**2 * bullet_drag_coefficient * bullet_area / bullet_mass
    dθdt = -g * math.cos(θ) / v

    return dxdt, dydt, dvdt, dθdt

# Function to perform one step of the Runge-Kutta method
def runge_kutta_step(t, dt, x, y, v, θ):
    # Calculate the k1 values
    k1_x, k1_y, k1_v, k1_θ = calculate_derivatives(t, x, y, v, θ)

    # Calculate the k2 values
    k2_x, k2_y, k2_v, k2_θ = calculate_derivatives(t + dt/2, x + k1_x*dt/2, y + k1_y*dt/2, v + k1_v*dt/2, θ + k1_θ*dt/2)

    # Calculate the k3 values
    k3_x, k3_y, k3_v, k3_θ = calculate_derivatives(t + dt/2, x + k2_x*dt/2, y + k2_y*dt/2, v + k2_v*dt/2, θ + k2_θ*dt/2)

    # Calculate the k4 values
    k4_x, k4_y, k4_v, k4_θ = calculate_derivatives(t + dt, x + k3_x*dt, y + k3_y*dt, v + k3_v*dt, θ + k3_θ*dt)

    # Update the variables
    x = x + dt * (k1_x + 2*k2_x + 2*k3_x + k4_x) / 6
    y = y + dt * (k1_y + 2*k2_y + 2*k3_y + k4_y) / 6
    v = v + dt * (k1_v + 2*k2_v + 2*k3_v + k4_v) / 6
    θ = θ + dt * (k1_θ + 2*k2_θ + 2*k3_θ + k4_θ) / 6

    return x, y, v, θ

# Main simulation loop
while y > 0:
    x, y, v, θ = runge_kutta_step(t, dt, x, y, v, θ)
    t = t + dt

    # Check if the bullet hits the target
    if target_distance - target_size/2 <= x <= target_distance + target_size/2 and y <= target_size:
        # Calculate the impact force
        delta_t = 0.001  # Assumed stopping time in seconds
        delta_p = bullet_mass * v  # Change in momentum
        impact_force = delta_p / delta_t  # Impact force
        print(f"The bullet covered a distance of {x} m and hit the target with an impact force of {impact_force} N!")
        break

    # Store the position for plotting
    x_values.append(x)
    y_values.append(y)

if y > 0:
    print("The bullet missed the target.")
else:
    print(f"The bullet covered a distance of {x} m before hitting the ground.")

# Plot the trajectory
plt.figure(figsize=(10, 5))
plt.plot(x_values, y_values)
plt.title('Bullet Trajectory')
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.grid(True)
plt.show()