# Physics-Encoded Neural Networks for Strictly Mass-Conserving Ice Thickness Interpolation

This repository contains the code that was used to process the data and create the figures in &lt;ref-to-paper&gt;.

All simulations were performed using the Physics-Informed Neural Networks for Ice and CLimatE (PINNICLE) python package[^1]. 
The PENN model code developed for this project is implemented therein and available at https://github.com/ISSMteam/PINNICLE.


## Files included in this repository

| File name | Function |
|-----------|----------|
| run-model.py | Main script to run inversions |
| save-data.ipynb | Post-processing, extract data for figures |
| thickness-profiles.ipynb | Interpolate gridded data along profile lines |
| make-figures.ipynb | Create the figures used in the paper |
| make-bm3-thk-files.ipynb | Create the .mat file containing the thickness observations |
| make-amb.ipynb | Create the .mat file containing the apparent mass balance data |


## Instructions

The inversions can be recreated by running the 'run-model.py' script.
The model requires downloading the data sets containing the obsrvation constraints specified below, and subsequently running the 'make-bm3-thk-file.ipynb' and 'make-amb.ipynb' jupyter notebooks to create the ice thickness and apparent mass balance data sets.
All data sets should be placed in the 'data' folder.

The main 'path' variable must be specified in the scripts by replacing '&lt;path-to-folder&gt;' with the path to the 'PENNs-for-MC-ice-thickness' folder.


## Required data sets

The following publicly available data sets are used in this code:

| Data set | File name | Link to repository |
|----------|-----------|--------------------|
| MEaSUREs Phase-Based Antarctica Ice Velocity Map, Version 1[^2][^3] | antarctic_ice_vel_phase_map_v01.nc | https://nsidc.org/data/nsidc-0754/versions/1 |
| BedMap3 statistically summarised points[^4][^6][^7] | UTIG_2009_ICECAP_AIR_BM3.csv | https://data.bas.ac.uk/full-record.php?id=GB/NERC/BAS/PDC/01502 |
| BedMap3 statistically summarised points[^5][^6][^7] | NASA_2011_ICEBRIDGE_AIR_BM2.csv | https://data.bas.ac.uk/full-record.php?id=GB/NERC/BAS/PDC/01618 |
| MEaSUREs ITS_LIVE Antarctic Grounded Ice Sheet Elevation Change, Version 1[^8][^9] | ANT_G1920_GroundedIceHeight_v01.nc | https://nsidc.org/data/nsidc-0782/versions/1 |
| RACMO statistically downscaled surface mass balance[^10][^11] | smb_rec.1979-2021.RACMO2.3p2_ANT27_ERA5-3h.AIS.2km.YY.nc | https://zenodo.org/records/10007855 |
| BedMachine Antarctica, Version 3[^12][^13] | BedMachineAntarctica-v3.nc | http://nsidc.org/data/nsidc-0756 |


[^1]: Cheng, G., Krishna, M., & Morlighem, M. (2025, August). A Python library for solving ice sheet modeling problems using physics-informed neural networks, PINNICLE v1.0. Geoscientific Model Development, 18(16), 5311–5327. Retrieved 2026-11-03, from https://gmd.copernicus.org/articles/18/5311/2025/ doi: 10.5194/gmd-18-5311-2025.
[^2]: Mouginot, J., Rignot, E., & Scheuchl, B. (2019a). Continent-Wide, Interferometric SAR Phase, Mapping of Antarctic Ice Velocity. Geophysical Research Letters, 46(16), 9710–9718. Retrieved 2026-10-08, from https://onlinelibrary.wiley.com/doi/abs/10.1029/2019GL083826 doi: 10.1029/2019GL083826.
[^3]: Mouginot, J., Rignot, E., & Scheuchl, B. (2019b). MEaSUREs Phase-Based Antarctica Ice Velocity Map, Version 1. NASA National Snow and Ice Data Center Distributed Active Archive Center. Retrieved from http://nsidc.org/data/NSIDC-0754/versions/1 doi: 10.5067/PZ3NJ5RXRH10.
[^4]: Young, D. A., Wright, A. P., Roberts, J. L., Warner, R. C., Young, N. W., Greenbaum, J. S., … Siegert, M. J. (2011, June). A dynamic early East Antarctic Ice Sheet suggested by ice-covered fjord landscapes. Nature, 474(7349), 72–75. Retrieved 2026-10-08, from https://www.nature.com/articles/nature10114 doi: 10.1038/nature10114.
[^5]: MacGregor, J. A., Boisvert, L. N., Medley, B., Petty, A. A., Harbeck, J. P., Bell, R. E., … Yungel, J. K. (2021). The Scientific Legacy of NASA’s Operation IceBridge. Reviews of Geophysics, 59(2), e2020RG000712. Retrieved 2026-10-08, from https://onlinelibrary.wiley.com/doi/abs/10.1029/2020RG000712 doi: 10.1029/2020RG000712.
[^6]: Frémand, A. C., Fretwell, P., Bodart, J. A., Pritchard, H. D., Aitken, A., Bamber, J. L., … Zirizzotti, A. (2023, July). Antarctic Bedmap data: Findable, Accessible, Interoperable, and Reusable (FAIR) sharing of 60 years of ice bed, surface, and thickness data. Earth System Science Data, 15(7), 2695–2710. Retrieved 2026-10-08, from https://essd.copernicus.org/articles/15/2695/2023/doi: 10.5194/essd-15-2695-2023.
[^7]: Pritchard, H. D., Fretwell, P. T., Fremand, A. C., Bodart, J. A., Kirkham, J. D., Aitken, A., … Zirizzotti, A. (2025, March). Bedmap3 updated ice bed, surface and thickness gridded datasets for Antarctica. Scientific Data, 12(1), 414. Retrieved 2025-04-17, from https://www.nature.com/articles/s41597-025-04672-y doi: 10.1038/s41597-025-04672-y.
[^8]: Nilsson, J., Gardner, A. S., & Paolo, F. S. (2022, August). Elevation change of the Antarctic Ice Sheet: 1985 to 2020. Earth System Science Data, 14(8), 3573–3598. Retrieved 2026-05-22, from https://essd.copernicus.org/articles/14/3573/2022/ doi:10.5194/essd-14-3573-2022.
[^9]: Nilsson, J., Gardner, A., & Paolo, F. (2023). MEaSUREs ITS_live Antarctic Grounded Ice Sheet Elevation Change, Version 1. NASA National Snow and Ice Data Center Distributed Active Archive Center. Retrieved 2025-12-03, from http://nsidc.org/data/NSIDC-0782/versions/1 doi: 10.5067/L3LSVDZS15ZV.
[^10]: van Wessem, J. M., van de Berg, W. J., Noël, B. P. Y., van Meijgaard, E., Amory, C., Birnbaum, G., … van den Broeke, M. R. (2018, April). Modelling the climate and surface mass balance of polar ice sheets using RACMO2 – Part 2: Antarctica (1979–2016). The Cryosphere, 12(4), 1479–1498. Retrieved 2026-09-16, from https://tc.copernicus.org/articles/12/1479/2018/ doi: 10.5194/tc-12-1479-2018.
[^11]: Noël, B., van Wessem, J. M., Wouters, B., Trusel, L., Lhermitte, S., & van den Broeke, M. R. (2023, December). Higher Antarctic ice sheet accumulation and surface melt rates revealed at 2 km resolution. Nature Communications, 14(1), 7949. Retrieved 2026-10-02, from https://www.nature.com/articles/s41467-023-43584-6 doi: 10.1038/s41467-023-43584-6.
[^12]: Morlighem, M., Rignot, E., Binder, T., Blankenship, D., Drews, R., Eagles, G., … Young, D. A. (2020, February). Deep glacial troughs and stabilizing ridges unveiled beneath the margins of the Antarctic ice sheet. Nature Geoscience, 13(2), 132–137. Retrieved 2025-03-04, from https://www.nature.com/articles/s41561-019-0510-8 doi: 10.1038/s41561-019-0510-8.
[^13]: Ockenden, H., Bingham, R. G., Goldberg, D., Curtis, A., & Morlighem, M. (2026, January). Complex mesoscale landscapes beneath Antarctica mapped from space. Science, 391(6782), 314–319. Retrieved 2026-01-19, from https://www.science.org/doi/10.1126/science.ady2532 doi: 10.1126/science.ady2532.

