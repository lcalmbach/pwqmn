**PWQMN-Browser: An interactive analysis tool for surface water quality data sets**

[The Provincial (Stream) Water Quality Monitoring Network](https://www.ontario.ca/data/provincial-stream-water-quality-monitoring-network) has published a rich data set of its monitoring data, including 2165 stations and 150 parameters. More information on the dataset can be found [here](https://www.javacoeapp.lrc.gov.on.ca/geonetwork/srv/en/metadata.show?id=13826) 

The current tool allows us to present this dataset in interactive scatter, time series, boxplots, etc. to better discover patterns and trends. 

PWQMN-Browser is written in python and uses the following two main libraries:
* [streamlit](https://streamlit.io/)
* [Altair](https://altair-viz.github.io/)

Note that the sample data is a subset of all available data since Github has restrictions on the file size that may be uploaded. The entire dataset is used in the site listed below.

A prototype can be visited on [http://18.222.39.57:8501](http://18.222.39.57:8501)

PWQMN-Browser is currently under development; any input is highly appreciated. Please don't hesitate using the issue-section to contribute.