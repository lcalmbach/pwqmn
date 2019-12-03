# Fontus, Interactive Water Quality Charts (in  progress)
*version: %version%*
### Intro 
This application allows to visualize water quality data from the Ontario Provincial (Stream) Water Quality Monitoring Network (PWQMN). The monitoring data includes data from various surface water bodies (rivers, creeks, lakes). The current dataset comprises %stations% stations and %parameters% parameters. A sampling event is considered the collection of measurements on the same date at the same sampling location. There are currently %samples% in the dataset. Most samples do only include few analysis as is shown in the parameters summary. The original dataset can be downloaded from [here](https://www.ontario.ca/data/provincial-stream-water-quality-monitoring-network "download data").

### Navigation and Filters
Various filters allow to interact with the plots. data can be filtered by

Stations: select ddd

![screenshot yearly filter](icon48.png)

### Menu 
#### Plotting
Fontus allows to visualize data in 3 different plots:
* Scatter plot
* Histogram
* Boxplot

To generate a scatter plot:

1. select Plotting from the menu
2. Select one of the following group by parameters: River, Station, Year, Month, Season. All samples belonging to the same groupby item will appear as the same marker on the plot. 
3. Select the appropriate x and y parameters.
4. Select one or multiple surface water bodies. Note that if only one station is selected, the plot will have additional interactive features, which will not appear if multiple plots are shown.

#### Parameters
The parameter table includes the following columns: 
* PARM: unique parameter name, e.g. CAUT for 'calcium unfiltered'
* PARM_DESCRIPTION: long name, without unit, e.g. CALCIUM, UNFILTERED TOTAL
* DESCRIPTION: long name and unit
* LABEL: field used for labeling the axis

If no water is selected, all parameters being measured in at least one sample are listed. If a water body is selected, then only parameters available in one of the stations of this water body are listed. Getting a clearer picture on which parmaters are available in your stations of interest may save you time later, when plotting the data.

#### Stations
The stations table includes the following columns: 
* RIVER_NAME:   name of the river or lake
* STATION_NAME: station name. Note that the original PWQMN station names do not include the prefix 'S-' which was added for this applications. Without the prefix, the names were sometimes converted to numbers and the trailing zeros removed.
* LOCATION: description of the sampling location
* STATUS: Status of the station: I for inactive and A for active.

If no surface water body is selected, all stations in the dataset are listed. If a water body is selected, only stations of this water body are listed. Getting a clearer picture on which stations are available may save you time later, when plotting the data.

