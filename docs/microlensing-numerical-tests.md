# Microlensing Numerical Tests and Regression Fixes

| **Test or Fix** | **Configuration** | **Expected Behavior** | **Validation Criterion** | **Purpose** |
|---|---|---|---|---|
| Binary-lens point-source consistency | $s=1.8$, $q=10^{-8}$; Witt–Mao 1995 and VBMicrolensing methods | Both algorithms return a magnification near $A=3.6868957$ | Agreement with the reference value to three decimal places | Cross-method numerical validation |
| Hexadecapole finite-source test | $s=1.35$, $q=0.00578$, $\rho=0.001$; $\Gamma=0,\ 0.5,\ 1.0$ | Hexadecapole, quadrupole, and point-source approximations reproduce stored reference magnifications | Array-valued magnifications must agree with the reference results using numerical equality assertions | Validate higher-order finite-source approximations |
| Quadrupole finite-source test | Same planetary configuration with $\Gamma=0,\ 0.5,\ 1.0$ | Quadrupole magnification reproduces the corresponding reference term | Computed result must match each stored quadrupole value | Validate quadrupole approximation and limb darkening |
| Integer-separation input regression | Binary lens evaluated once with $s=1.0$ and once with $s=1$ | Integer and floating-point inputs produce identical magnification | Agreement to 12 decimal places | Prevent input-type-dependent numerical behavior |
| VBMicrolensing baseline test | $s=0.8$, $q=0.1$, $\rho=0.01$, $(x,y)=(0.01,0.01)$ | Finite-source magnification $A=18.2834436$ | Agreement to three decimal places | Baseline binary finite-source verification |
| VBMicrolensing v3.5 regression fix | $s=0.3121409538$, $q=0.0018654669$, $\rho=0.002966663$; three neighboring trajectory positions | The central magnification must be smooth and consistent with neighboring samples rather than the erroneous pre-v3.5 result | Third sample must equal $1.3442264706$ to five decimals; central sample must agree with the mean of its neighbors to four decimals | Detect and prevent the historical VBBL finite-source anomaly |
| Relative-accuracy propagation | $s=0.8$, $q=0.1$, $\rho=0.01$; relative tolerance $10^{-10}$ and limb darkening $u=0.5$ | The requested relative accuracy is passed to the underlying VBMicrolensing calculation | Magnification must equal $18.288975003$ | Validate solver-accuracy control |
| No-limb-darkening tolerance fix | $s=1.1$, $q=0.005$, $\rho=0.001$; tight tolerance $10^{-10}$ versus loose tolerance $0.5$ | Changing the relative tolerance must alter the no-limb-darkening result | Difference between tight and loose results must exceed $0.01$ | Regression test for issue 162: tolerance was previously accepted but ignored |
| Limb-darkened finite-source test | $s=0.8$, $q=0.001$, $\rho=0.001$; $u=0.51$ | Limb-darkened and uniform-source calculations return distinct validated magnifications | $A_{\mathrm{LD}}=683.31177335$ and $A_{\mathrm{uniform}}=687.80333614$ | Validate limb-darkening integration |

## Roman Survey Simulation Test Extensions

The following cases should be implemented in the Roman simulation and fitting workflow:

- High-cadence F146 sampling and season-window masking
- Low-cadence inter-season coverage
- Magnitude-dependent photometric-noise injection
- Crowding and source/blend-flux separation
- Multiband color-dependent blending
- Finite-source caustic crossings and method switching
- Annual and Roman–ground parallax
- Joint photometric and astrometric microlensing
- Dark-lens and luminous-lens SED recovery
- Free-floating versus wide-orbit planet model comparison
- Close/wide and signed-$u_0$ degeneracy recovery
- Missing-data and outlier robustness
- Ensemble parameter-recovery coverage testing
