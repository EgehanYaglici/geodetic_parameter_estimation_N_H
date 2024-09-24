import numpy as np

"""
# Geodetic Parameter Estimation Script

This script performs geodetic parameter estimation using known station data. 
It calculates the orthometric height (N) and the adjusted height (H) for 
specified points by employing the least squares method to fit a polynomial 
model to the data. The code normalizes the coordinates, constructs matrices, 
computes coefficients, and verifies the results by comparing calculated and 
actual heights.

Each station is defined by its coordinates and heights as follows:
- x: Easting coordinate (in meters)
- y: Northing coordinate (in meters)
- h: Ellipsoidal height (in meters)
- H: Orthometric height (in meters)
- N: Geoid height (in meters)
"""

# Define station data with x, y, h, H, and N values
stations = [
    [531121.569, 4171060.477, 1223.482, 1188.611, 34.872],
    [522139.007, 4175249.228, 986.836, 952.226, 34.610],
    [521965.772, 4177055.988, 929.367, 894.796, 34.571],
    [525985.901, 4181645.566, 888.526, 853.816, 34.710],
    [527321.854, 4177938.485, 1008.752, 973.975, 34.777],
    [532702.166, 4184439.027, 915.429, 880.430, 35.000],
    [531409.083, 4183177.180, 918.169, 883.249, 34.920],
    [528687.730, 4181432.714, 928.932, 894.141, 34.790],
    [530800.931, 4182399.516, 927.869, 892.995, 34.874],
    [524599.277, 4181624.668, 889.236, 854.547, 34.690],
    [530080.624, 4174023.790, 1190.143, 1155.250, 34.893],
    [527448.386, 4180150.776, 933.986, 899.226, 34.760],
    [522187.785, 4180966.223, 883.935, 849.251, 34.685],
    [523840.797, 4181543.848, 891.823, 857.109, 34.710],
    [533721.734, 4172811.346, 1260.599, 1225.547, 35.052],
    [530128.716, 4182144.569, 930.177, 895.307, 34.870],
    [533041.683, 4170351.896, 1253.464, 1218.518, 34.946],
    [518442.199, 4174291.701, 892.537, 858.126, 34.410],
    [532328.018, 4170762.774, 1229.461, 1194.539, 34.922],
    [530030.643, 4172850.093, 1256.650, 1221.744, 34.910]
]

# Calculate mean coordinates for normalization
mean_x = np.mean([station[0] for station in stations])
mean_y = np.mean([station[1] for station in stations])

# Initialize matrices for the least squares method
A = []  # Design matrix
l = []  # Observations vector

# Populate the design matrix A and observations vector l
for station in stations:
    x, y, h, H, N = station
    xn = (x - mean_x) / 1000  # Normalize x coordinate
    yn = (y - mean_y) / 1000  # Normalize y coordinate
    A.append([1, xn, yn, xn**2, xn*yn, yn**2, xn**3, xn**2*yn, xn*yn**2, yn**3])
    l.append(N)  # Add geoid height to observations vector

# Convert lists to numpy arrays for further calculations
A = np.array(A)
l = np.array(l)

# Perform least squares adjustment to compute coefficients
coefficients = np.linalg.lstsq(A, l, rcond=None)[0]

# Print the computed coefficients
print("Coefficients:")
for i, coef in enumerate(coefficients):
    print(f"A{i} = {coef}")

# Function to calculate geoid height (N) using the polynomial model
def calculate_N(x, y, mean_x, mean_y, coeffs):
    xn = (x - mean_x) / 1000  # Normalize x coordinate
    yn = (y - mean_y) / 1000  # Normalize y coordinate
    return (coeffs[0] + coeffs[1] * xn + coeffs[2] * yn + coeffs[3] * xn**2 +
            coeffs[4] * xn * yn + coeffs[5] * yn**2 + coeffs[6] * xn**3 +
            coeffs[7] * xn**2 * yn + coeffs[8] * xn * yn**2 + coeffs[9] * yn**3)

# Verification of calculated N values against known values
print("\nVerification for known points:")
for station in stations:
    x, y, h, H, N_real = station  # Unpack station data
    N_calculated = calculate_N(x, y, mean_x, mean_y, coefficients)  # Calculate N
    print(f"Point ({x}, {y}): Real N = {N_real}, Calculated N = {N_calculated:.4f}, Difference = {N_real - N_calculated:.4f}")

# New points for which to calculate N and H
points = [
    [521850.000, 4173360.000, 1056.880],
    [522220.000, 4175000.000, 998.887]
]

# Calculate and print N and H for the new points
for point in points:
    x, y, h = point  # Unpack point data
    N = calculate_N(x, y, mean_x, mean_y, coefficients)  # Calculate N
    H = h - N  # Calculate adjusted height H
    print(f"\nFor point ({x}, {y}):")
    print(f"N = {N:.4f}")  # Print calculated N
    print(f"H = {H:.4f}")  # Print calculated H
