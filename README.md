# Colorshot Automation
This program takes raw data files from the Neutone Colorshot, compiles them, and outputs them with several colorimetric values used for comparison. The following staff took the assigned roles in design and execution.

Name | Role
--|--
Liwayway Piano | Customer, Designer
Thomas Tomsia | Customer, Designer
Chris Quartararo | Author, Designer

## Project Progress
Below are the steps anticipated to deliver a minimum product.

- :white_check_mark: Find data files.
- :white_check_mark: Read data files into one large table.
- :white_check_mark: Compare files to a master list to find just the new data.
- :white_check_mark: Group sets together.
    - :large_orange_diamond: Deal with sets that are not matched 
- :white_check_mark: Find and mark standards.
- :white_check_mark: Calculate colorimetry.
- :white_check_mark: Build report file.
    - :white_check_mark: Test comparison of new data to report file works.
- :white_large_square: Backup report file.
- :white_large_square: Final Integration testing.
- :white_large_square: Package module into a standalone executable.

Key:
- :white_check_mark: - Completed
- :large_orange_diamond: - In Progress
- :white_large_square: - Todo
- :red_circle: - Issues that prevent progress
- :x: - Removed or changed requirement

## Design
This workflow was designed to fit that of the CPD team of Liwayway and Thomas. Thus if this is  being used for additional teams, certain conventions may need to be adopted in terms of data storage and labelling to ensure proper data discover and functionality.

### Data
Data are stored in the network drive mapped to `G:\`. The data files to include are indicated in a text file, each data file as it's own separate line following the example below.
```
# Text file contents
G:\Colorshot Directory\Data file 1.xlsx
G:\Colorshot Directory\Data file 2.xlsx
...
```

The data compilation attempts to compare datapoints that are already included in the final product so as to not have to recompute the entire library of colorimetry each time the program is run.

### Data Point Comparisons
To properly calculate the colorimetry, a set of standard and test (comparison) formulas must be identified. Workflow demands that a standard is run on the Colorshot in the same session as running the tests, thus we _should_ always have a temporally clustered set of a standard and tests. Names of these sets are marked in the `<Shade Name>` column. Standards are tagged with exactly `"STD"` somewhere in the Shade Name. A regex finds these tags to determine which rows are standards. This technique will fail (_i.e._ incorrectly mark shades as standards) if a shade is named with the characters `"STD"` in sequence, however the designers feel this is a unique enough sequence it will not be an issue.

Comparisons sets are grouped and labelled using the `Date only (no time)`, `Shade Name`, and `Fiber Type`.

Complications arise when a single shade is run through the Colorshot multiple times in one day with different test shades, producing multiple standards of the same shade in a single day. This doesn't happen often, but enough to be considered during the design process. To decrease the likelyhood of using of the wrong standard, an expanding temporal filter is employed when a set has more than one standard present. The farther away these measurements are from each other, the higher the confidence in picking the correct standard for colorimetry comparison.

Finally, data points that are not successfully assigned to a set are placed in a separate file with their indentifying information to be dealt with. Once the base data has been corrected, the program will need to be run again to add these datapoints to the final product file.

### Colorimetry Calculations
The final product includes several colorimetry metrics that aid the chemists in formulation. These include the following:

Metric | Description
--|--
$\Delta E_{00}$ | Total color difference using the Delta E2000 formula
$\Delta L^*$ | Change in lightness, or ligher(+)/darker(-) than the standard
$\Delta a^*$ | Change on the red(+)/green(-) axis
$\Delta b^*$ | Change on the yellow(+)/blue(-) axis
$\Delta C^*$ | Change in the magnitude of chroma
$\Delta h^\circ$ | Change (+ anticlockwise/-clockwise) in the hue angle from the standard $h^\circ$

$\Delta E$ values are calculated with the [colour-science](https://www.colour-science.org/) package. 

$\Delta L^*$ and $\Delta b^*$ metrics are simply differences ($x_1-x_2=metric$) between the test formula and the standard of that set. 

The $\Delta a^*$ calculation follows the same difference formula but uses a corrected ${a^*}'$ found by ${a^*}' = (1+ \bar{C}) * a^*$. 

This same ${a^*}'$ is used to calculate corrected $C'$ values for the standard and comparison that are then used to find the difference using the previous formula.

Finally, $\Delta h^\circ$ uses the corrected ${a^*}'$ values to find corrected ${\Delta h^\circ}'$ values which are then used to find the smallest angle difference starting from the standard and moving towards the comparison, measured in degrees. That formula is ${\Delta h^\circ}' = -((({h^\circ}'_{comparison} - {h^\circ}'_{standard}) + 180) \bmod 360 - 180)$, where "$\bmod$" is the modulo (or remainder) operator.

### Other Functionality
Here is some other functionality that doesn't fit neatly into other sections.

A backup of the final product file is made in the case that the next run of the program makes a big ol' mess of the product and it becomes unusable.