# Correlation_between_heat_waves_and_mortality

This script performs analysis on temperature data and mortality data. It calculates the 90th percentile of temperature values, identifies consecutive days above the 90th percentile as heat waves, and performs t-tests on mortality data during heat waves compared to non-heat wave periods.

The repository contains a Jupyter notebook file, named `correlation_between_heat_waves_and_mortality.ipynb`, which showcases the code and analysis for the project

Dependencies
------------

The script requires the following dependencies to be installed:

-   pandas
-   numpy
-   scipy

You can install the dependencies using pip:

Copy code

`pip install pandas numpy scipy`

Usage
-----

To use the script, follow these steps:

1.  Ensure that the necessary data files are present in the same directory as the script:

    -   `Podatki_Podravje_temp_postaja_311.xlsx`: Excel file containing temperature data.
    -   `Podaki o umrlih_po vzroku, datumu smrti, obcini in statusu aktivnosti_2012-2021.xlsx`: Excel file containing mortality data.
2.  Open a terminal or command prompt, navigate to the directory where the script is located.

3.  Run the script using the following command:

    `analyze_death_data.py`

The script will perform the analysis and generate output files for each category (obcina, vzrok, aktivnost) in separate Excel files.

Output
------

The script generates the following output files:

-   `vrocinski_val.xlsx`: Excel file containing the data frame with the "datum" and "vrocinski_val" columns.
-   `<category>.xlsx`: Excel files containing the results of the t-tests for each category (obcina, vzrok, aktivnost).

Customization
-------------

You can modify the code to suit your specific requirements. Here are a few possible modifications:

-   Adjust the date filtering criteria (`df311['datum'] < '2012-01-01'` and `df = df[df['Datum smrti'] < pd.Timestamp('2021-01-01')]`) in the script to select a different range of dates for analysis.
-   Modify the column names in the mortality data file to match the actual column names.
-   Customize the Excel file names and formatting options according to your preferences.
-   Extend the analysis by adding additional categories or modifying the t-test calculations.

Please note that modifying the script requires understanding the underlying logic and data structures.
