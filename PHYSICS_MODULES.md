# Core Numerical Physics Modules

## nbody/ (7)
- symplectic_integrator.py – Verlet, Forest-Ruth, Yoshida-4
- nbody_integrator.py – Direct N-body + energy/momentum conservation
- barnes_hut.py – Barnes-Hut tree gravity O(N log N)
- particle_mesh.py – Particle-Mesh Poisson via FFT
- adaptive_timestep.py – Individual/block/collision-aware timesteps
- relativistic_orbit.py – 1PN post-Newtonian orbits
- gr_geodesic.py – Schwarzschild geodesic integrator

## cosmology/ (6)
- friedmann.py – H(a), scale-factor evolution, cosmic age, distances
- lcdm.py – ΛCDM parameter engine
- expansion_coords.py – Comoving/proper transforms
- primordial_perturbation.py – BBKS P(k) + Gaussian random field
- cmb.py – Angular power spectrum + temperature map
- cosmic_web.py – Tidal-tensor void/sheet/filament/knot classification

## hydro/ (6)
- sph.py – SPH density, pressure forces, artificial viscosity
- eos.py – Ideal gas, polytrope, isothermal, degenerate EOS
- cooling_heating.py – Radiative cooling + equilibrium T
- star_formation.py – Density-threshold SFR + star particles
- stellar_evolution.py – MS lifetime, endpoints, L/R tracks
- black_hole.py – Rs, ISCO, Hawking T, Bondi, Eddington

## dark/ (4)
- halo_finder.py – Friends-of-Friends + spherical overdensity
- halo_formation.py – Spherical collapse + NFW profile
- dark_energy.py – w(z) CPL + ρ_DE(a)
- modified_gravity.py – Yukawa fifth-force + screening

## planetary/ (6)
- collision.py – Merge/bounce/fragment outcomes
- tidal_heating.py – Viscoelastic tidal power
- tidal_locking.py – Lock timescale + sync check
- atmospheric_escape.py – Jeans + energy-limited escape
- climate_energy.py – 0-D energy-balance climate
- conservation.py – Mass/momentum/energy validation

All pure Python, self-testing, no duplicates of prior packages.
