# Fontus, Interactive Water Quality Charts (in  progress)



### Table of content
Intro
- Navigation and Filters
Menu
- Plotting
-- Scatter plot
[Station information](#Station-information)  
Parameters
Settings

*version: %version%*
### Intro 
This application allows to visualize water quality data from the Ontario Provincial (Stream) Water Quality Monitoring Network (PWQMN). The monitoring data includes data from various surface water bodies (rivers, creeks, lakes). The current dataset comprises %stations% stations and %parameters% parameters. A sampling event is considered the collection of measurements on the same date at the same sampling location. There are currently %samples% in the dataset. Most samples do only include few analysis as is shown in the parameters summary. The original dataset can be downloaded from [here](https://www.ontario.ca/data/provincial-stream-water-quality-monitoring-network "download data").

### Navigation and Filters
Various filters allow to interact with the plots. The filters are enabled on the sideboard, by checking the filter by year and month checkboxes. The stations filter becomes available, if only one surface water body is selected from the multi select box on the sideboard. You may either select <all stations> or a specific station and the plot will rerender based on the selection. In this case, an additional link to Google map will appear, allowing to navigate to the sampling location. In most cases it is possible virtually visite the site using the street view tool.

![screenshot yearly filter](https://github.com/lcalmbach/pwqmn/raw/master/static/images/scatter_filter_year.png)

### Menu 
#### Plotting
Fontus allows to visualize data in 4 different plots:
* Scatter plot
* Histogram
* Boxplot
* Maps

##### Scatter plot:
1. select Plotting from the menu
2. Select one of the following group by parameters: River, Station, Year, Month, Season. All samples belonging to the same groupby item will appear as the same marker on the plot. 
3. Select the appropriate x and y parameters.
4. Select one or multiple surface water bodies. Note that if only one station is selected, the plot will have additional interactive features, which will not appear if multiple plots are shown.

##### Histogram:
##### Boxplot:
##### Maps:

#### Parameters
The parameter table includes the following columns: 
* PARM: unique parameter name, e.g. CAUT for 'calcium unfiltered'
* PARM_DESCRIPTION: long name, without unit, e.g. CALCIUM, UNFILTERED TOTAL
* DESCRIPTION: long name and unit
* LABEL: field used for labeling the axis

If no water is selected, all parameters being measured in at least one sample are listed. If a water body is selected, then only parameters available in one of the stations of this water body are listed. Getting a clearer picture on which parmaters are available in your stations of interest may save you time later, when plotting the data.

#### Station information
The stations table includes the following columns: 
* RIVER_NAME:   name of the river or lake
* STATION_NAME: station name. Note that the original PWQMN station names do not include the prefix 'S-' which was added for this applications. Without the prefix, the names were sometimes converted to numbers and the trailing zeros removed.
* LOCATION: description of the sampling location
* STATUS: status of the station: I for inactive and A for active.
* FIRSTYR: first year of sampling at this station
* LASTYR: last year of sampling at this station
* Missing: number of year without sampling

If no surface water body is selected, all stations in the dataset are listed. If a water body is selected, only stations of this water body are listed. Getting a clearer picture on which stations are available may save you time later, when plotting the data.


