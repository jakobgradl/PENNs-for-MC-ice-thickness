# Physics-Encoded Neural Networks for Strictly Mass-Conserving Ice Thickness Interpolation

This repository contains the code that was used to process the data and create the figures in <paper>.
All simulations were performed using the Physics-Informed Neural Networks for Ice and CLimatE (PINNICLE) python package. 
The PENN model code developed for this project is implemented therein and available at https://github.com/ISSMteam/PINNICLE.

## Files included in this repository

run-model.py
save-data.ipynb
thickness-profiles.ipynb
make-figures.ipynb
make-bm3-thk-files.ipynb
make-amb.ipynb

## Instructions

The inversions can be recreated by running the 'run-model.py' script.
The model requires downloading the data sets containing the obsrvation constraints specified below, and subsequently running the 'make-bm3-thk-file.ipynb' and 'make-amb.ipynb' jupyter notebooks to create the ice thickness and apparent mass balance data sets.
All data sets should be placed in the 'data' folder.

The main 'path' variable must be specified in the scripts by replacing '<path-to-folder>' with the path to the 'PENNs-for-MC-ice-thickness' folder.

## Required data sets

The following publicly available data sets are used in this code:

| Data set | File name | Link to repository |
|----------|-----------|--------------------|
| MEaSUREs Phase-Based Antarctica Ice Velocity Map, Version 1[^1,2] | antarctic_ice_vel_phase_map_v01.nc | https://nsidc.org/data/nsidc-0754/versions/1 |
| BedMap3 statistically summarised points | UTIG_2009_ICECAP_AIR_BM3.csv | https://data.bas.ac.uk/full-record.php?id=GB/NERC/BAS/PDC/01502 |
| BedMap3 statistically summarised points | NASA_2011_ICEBRIDGE_AIR_BM2.csv | https://data.bas.ac.uk/full-record.php?id=GB/NERC/BAS/PDC/01618 |
| MEaSUREs ITS_LIVE Antarctic Grounded Ice Sheet Elevation Change, Version 1 | ANT_G1920_GroundedIceHeight_v01.nc | https://nsidc.org/data/nsidc-0782/versions/1 |
| RACMO statistically downscaled surface mass balance | smb_rec.1979-2021.RACMO2.3p2_ANT27_ERA5-3h.AIS.2km.YY.nc | https://zenodo.org/records/10007855 |
| BedMachine Antarctica, Version 3 | BedMachineAntarctica-v3.nc | http://nsidc.org/data/nsidc-0756 |


## References
[^1]: Mouginot, J., Rignot, E., & Scheuchl, B. (2019a). Continent-Wide, Interferometric SAR Phase, Mapping of Antarctic Ice Velocity. Geophysical Research Letters, 46(16), 9710–9718. Retrieved 2026-10-08, from https://onlinelibrary.wiley.com/doi/abs/10.1029/2019GL083826 doi: 10.1029/2019GL083826.
[^2]: Mouginot, J., Rignot, E., & Scheuchl, B. (2019b). MEaSUREs Phase-Based Antarctica Ice Velocity Map, Version 1. NASA National Snow and Ice Data Center Distributed Active Archive Center. Retrieved from http://nsidc.org/data/NSIDC-0754/versions/1 doi: 10.5067/PZ3NJ5RXRH10.

