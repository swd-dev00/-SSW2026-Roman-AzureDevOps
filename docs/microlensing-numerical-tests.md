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

# Proposed Roman Microlensing Survey Simulation Tests and Required Fixes

| **Test** | **Roman Simulation Setup** | **Expected Result** | **Failure Signature** | **Required Fix** |
|---|---|---|---|---|
| High-cadence sampling | Generate F146 epochs at a nominal 12.1-minute cadence over each high-cadence season | Injected short planetary anomalies retain the correct duration, peak time, and morphology after sampling | Anomalies disappear, shift in time, or are represented by too few samples despite sufficient intrinsic duration | Use the real observation-time array rather than assuming evenly spaced daily sampling; preserve sub-day time precision |
| Season-window function | Apply six high-cadence seasons of approximately 70.5 days, separated into three early and three late mission seasons | Events inside observing windows are recovered; unobserved portions are correctly marked missing rather than zero flux | Artificial flux discontinuities, false baselines, or fits across unobserved multi-month and multi-year gaps | Represent gaps with absent epochs or masks; never insert zero-valued measurements into seasonal gaps |
| Low-cadence bridge | Insert middle-mission observations at approximately five-day cadence during four low-cadence seasons | Long-duration events preserve sufficient temporal coverage to constrain $t_{\rm E}$, baseline motion, and astrometric evolution | Long events are truncated or their timescales become strongly biased because only high-cadence seasons are modeled | Add low-cadence epochs to the joint likelihood and retain distinct cadence metadata |
| Photometric noise injection | Inject source-dependent Poisson noise, sky background, detector noise, and systematic noise floors into F146 fluxes | Normalized residuals follow approximately $\mathcal{N}(0,1)$ when evaluated with the injected uncertainties | Reduced $\chi^2$ is systematically much larger or smaller than unity; parameter intervals show poor coverage | Propagate all variance terms consistently and fit an optional error-renormalization or jitter term |
| Faint-source precision | Simulate stars around the survey reference level, including an F146 source near 21.2 AB mag | Recovered signal-to-noise agrees with the adopted Roman exposure model and detection efficiency declines smoothly with magnitude | An abrupt sensitivity cutoff or unrealistically constant precision across source magnitude | Make uncertainties flux- and background-dependent rather than assigning one constant error to every epoch |
| Crowding and blending | Add unresolved neighboring-star flux: $F(t)=F_{\rm s}A(t)+F_{\rm b}$ | The fit recovers source flux $F_{\rm s}$ and blend flux $F_{\rm b}$ without strongly biasing $u_0$, $t_{\rm E}$, or $q$ | Negative source flux, unphysical blend fractions, or biased planet parameters when crowding increases | Fit source and blend flux separately per instrument/filter and impose physically justified priors or parameterizations |
| Color-dependent blending | Generate joint F146, F087, and F213 measurements with distinct source and blend spectral energy distributions | The inferred source color is consistent across the magnification event and helps distinguish the lensed source from contaminants | The pipeline assumes identical blend fractions in all filters or produces event-correlated color changes for an achromatic lensing model | Use independent filter flux terms while tying the common lensing magnification across bands |
| Finite-source caustic crossing | Inject binary-lens events with known $\rho$, $q$, $s$, $\alpha$, and limb-darkening coefficients | Recovered caustic-crossing duration and source radius parameter agree with injected values within posterior uncertainty | Sharp caustic features are numerically unstable or approximated by point-source magnification | Switch automatically to finite-source contour integration or VBMicrolensing near caustics |
| Magnification-method switching | Evaluate one event with point-source, quadrupole, hexadecapole, and full finite-source methods across a caustic approach | Approximate methods converge to the full solution away from caustics, with smooth transitions between methods | Discontinuous light curves or order-dependent changes when the calculation method switches | Use an accuracy-based switching criterion and test overlap regions between methods |
| Annual microlens parallax | Inject Earth–Roman observer acceleration through $(\pi_{\mathrm{E},N},\pi_{\mathrm{E},E})$ | The parallax-enabled model improves the likelihood and recovers the injected vector without a coordinate-sign reversal | Recovered components are swapped, sign-flipped, or dependent on the chosen time origin | Standardize the coordinate convention, reference epoch, and ephemeris interface; add known-vector regression tests |
| Roman–ground satellite parallax | Generate simultaneous Roman and ground-based light curves from separated observer positions | The joint model recovers the imposed satellite-parallax offset and properly handles separate flux systems | Both observatories are assigned the same trajectory or forced to share photometric zero points | Compute observer-specific trajectories while sharing physical lens parameters |
| Astrometric microlensing | Inject centroid shifts $\boldsymbol{\delta\theta}(t)$ together with photometric magnification | The joint posterior recovers $\theta_{\rm E}$ and improves lens-mass constraints relative to photometry alone | Centroid shifts are centered incorrectly, confused with proper motion, or expressed in inconsistent angular units | Fit source position, proper motion, parallax, and lensing displacement in one astrometric reference frame |
| Seasonal astrometric baseline | Use the early–late season separation across Roman's five-year mission | Proper motion and long-duration centroid evolution remain identifiable across the multi-year baseline | Each season receives an independent arbitrary centroid that removes the physical inter-season motion | Include calibrated per-season offsets but retain one global source proper-motion and parallax model |
| Dark-lens recovery | Inject neutron-star or black-hole lenses with negligible lens flux and long $t_{\rm E}$ | The joint photometric–astrometric inference recovers a posterior consistent with the injected lens mass and low lens luminosity | The pipeline forces a luminous-lens SED contribution or misclassifies dark lenses as highly blended stellar lenses | Permit zero lens flux and combine mass–distance inference with lens-flux upper limits rather than mandatory detections |
| Luminous-lens SED recovery | Inject a main-sequence lens with multiband lens flux and a known stellar SED | The inferred lens mass and distance are consistent between microlensing and stellar-population constraints | The SED is assigned entirely to the source or blend, producing inconsistent physical lens properties | Model source, lens, and unrelated blend flux as separate latent components |
| Free-floating planet event | Inject an isolated, short-timescale point-lens event with no detectable host perturbation | The event is recovered without forcing a binary-lens host and the posterior retains the hostless interpretation | The optimizer invents extreme $s$ or $q$ values to force every event into a bound-planet model | Compare point-lens and wide-separation binary-lens hypotheses using model evidence or predictive criteria |
| Bound-versus-free-floating degeneracy | Inject both a truly isolated lens and a very wide-separation planetary system | Model comparison quantifies when the host-star signal is genuinely excluded versus merely undetected | The classification is based only on the best-fit separation without an upper-limit calculation | Perform host-signal injection–recovery and report detection-efficiency limits over $(s,q)$ |
| Close–wide degeneracy | Generate paired solutions near $s$ and $1/s$ with similar central caustics | Both posterior modes are identified and their relative probabilities are reported | A single optimizer returns only one topology and understates parameter uncertainty | Use multimodal sampling, multiple initializations, or explicit close/wide model branches |
| Impact-parameter sign degeneracy | Fit events allowing both positive and negative $u_0$, especially when parallax is enabled | Mirror solutions are either recovered or decisively rejected by the data | Sampling is restricted to one sign and produces overconfident parallax constraints | Allow signed $u_0$ and initialize samplers in both degeneracy branches |
| Missing-data robustness | Randomly remove exposures and insert realistic interruptions within otherwise high-cadence sequences | Posterior estimates remain unbiased, with uncertainty increasing according to lost information | Interpolation creates artificial planetary features or treats masked points as observations | Evaluate the likelihood only at valid epochs; interpolate models, not missing measurements |
| Outlier and cosmic-ray robustness | Inject isolated positive and negative flux excursions | The physical microlensing parameters remain stable and outliers receive low statistical weight | A few bad points create false caustic crossings or short-duration planet detections | Add robust likelihoods, mixture-model outlier terms, or validated quality-mask handling |
| Parameter-recovery coverage | Run an ensemble of injected events spanning $t_{\rm E}$, $u_0$, $\rho$, $q$, $s$, source magnitude, and blending | Nominal 68% and 95% posterior intervals contain the injected truth at approximately their stated frequencies | Persistent undercoverage, biased medians, or failure concentrated in specific parameter regimes | Calibrate priors, likelihoods, sampler convergence, and reported credible intervals using simulation-based calibration |

# Roman GBTDS Simulation Constants

| **Parameter** | **Nominal Value** | **Role in Simulation** |
|---|---:|---|
| Mission duration | 5 years | Sets the full temporal baseline |
| High-cadence seasons | 6 | Defines the primary dense microlensing observing windows |
| Low-cadence seasons | 4 | Preserves long-timescale and astrometric information between dense seasons |
| High-cadence season length | 70.5 days | Controls the observing-window duration |
| F146 cadence | 12.1 minutes | Governs short-anomaly sampling |
| F146 epochs per high-cadence season | 8,390 | Sets the nominal per-season sampling density |
| Low-cadence interval | 5 days | Bridges the middle-mission gap |
| F146 exposure time | 66 seconds | Supports exposure-level signal-to-noise calculations |
| F087 cadence | 6 hours | Provides auxiliary color information |
| F213 cadence | 6 hours | Provides auxiliary color information |

# EXOFASTv2 Feature Summary

| **Feature** | **Capability** |
|---|---|
| Model suite | Battle-tested global modeling suite |
| Adoption | Used in approximately half of published TESS discovery papers |
| Pipeline | End-to-end light-curve to publication-quality modeling workflow |
| Stellar modeling | Spectral energy distributions, evolutionary models, and empirical relations |
| Planetary modeling | Transit photometry, radial velocities, astrometry, and joint system parameters |
| Repository | `https://github.com/jdeast/EXOFASTv2` |

# EXOZIPPy Overview

| **Component** | **Description** |
|---|---|
| Framework | Combines capabilities associated with EXOFASTv2, exoplanet, and MulensModel |
| Implementation | Ground-up Python reimplementation of global Bayesian modeling using PyMC |
| Interface | User-facing wrapper around PyMC intended for exoplanet and broader inference workflows |
| Core components | Transit photometry, radial velocity, SED modeling, stellar models, planetary models, empirical relations, evolutionary models, and gravitational microlensing |
| Development status | Active alpha development; functional but subject to bugs, rough edges, and breaking API changes |
| Repository | `https://github.com/jdeast/exozippy` |
| Community | `https://www.reddit.com/r/exozippy/` |
