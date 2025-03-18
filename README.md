# AviMove

Python package for the analysis of avian movement and behaviour. Currently involves two sub-modules, `cal_wind2` and `forage_detect`, implementing the methodologies of [Goto et al., 2018](https://www.science.org/doi/10.1126/sciadv.1700097) and [Garrod et al., 2021](https://www.science.org/doi/10.1126/sciadv.1700097).

## Reading capacity

AxyTrek, Little Leonardo DVL-4003DGT, and BiP online storage formats are currently supported.

## Acceleration characteristics

- Flap/glide detection
  - dorsoventral acceleration signals of flapping/gliding motions.
- Flight detection
  - Estimation of flight periods from spectral analysis of dorsoventral acceleration, **requires** typical flapping frequency.
- Speed and distance calculations
  - **requires** GPS recording.

## `cal_wind2`

Wind estimation method from GPS tracks of seabirds.