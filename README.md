## Overview

The script normalizes the coordinates of the known stations, constructs matrices, computes coefficients, and verifies the results by comparing calculated and actual heights.

### Key Features

- **Input Data**: Utilizes known geodetic station data (X, Y, h, H, N).
- **Least Squares Method**: Applies a polynomial fitting approach for parameter estimation.
- **Height Calculation**: Computes orthometric heights (N) and adjusted heights (H) for specified points.
- **Validation**: Verifies calculated heights against known values to ensure accuracy.