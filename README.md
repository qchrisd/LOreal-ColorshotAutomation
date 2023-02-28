# Colorshot Automation
This program takes raw data files from the Neutone Colorshot, compiles them, and outputs them with several colorimetric values used for comparison. The following staff took the assigned roles in design and execution.

Name | Role
--|--
Liwayway Piano | Customer, Designer
Thomas Tomasia | Customer, Designer
Chris Quartararo | Author, Designer

## Design
This workflow was designed to fit that of the CPD team of Liwayway and Thomas. Thus if this is being used for additional teams, certain conventions may need to be adopted in terms of data storage and labelling to ensure proper data discover and functionality.

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
To properly calculate the colorimetry, a set of standard and test formulas must be identified. Workflow demands that a standard is run on the Colorshot in the same session as running the tests, thus we _should_ always have a temporally clustered set of a standard and tests. Names of these sets are marked with the `<Shade Name>`. Standards are tagged with `"STD"` after this name. A regex finds these tags to determine which rows are standards.

Complications arise when a single shade is run through the Colorshot multiple times in one day with different test shades, producing multiple standards of the same shade in a single day. This doesn't happen often, but enough to be considered during the design process. To decrease the likelyhood of using of the wrong standard, an expanding temporal filter is employed when searching for sets. The farther away these measurements are from each other, the higher the confidence in picking the correct standard for colorimetry comparison.

Comparisons sets are grouped and labelled using the `Shade Name`, `Nuance (Technical Number)`, and `Fiber Type`.

Finally, data points that are not successfully assigned to a set are placed in a separate file with their indentifying information to be dealt with. Once the base data has been corrected, the program will need to be run again to add these datapoints to the final product file.

### Colorimetry Calculations
The final product includes several colorimetry metrics that aid the chemists in formulation. These include the following:

Metric | Description
--|--
$\Delta E_{00}$ | Total color difference using the Delta E2000 formula
$\Delta L^*$ | Change in lightness, or ligher(+)/darker(-) than the comparison
$\Delta a^*$ | Change on the red(+)/green(-) axis
$\Delta b^*$ | Change on the yellow(+)/blue(-) axis
$\Delta C^*$ | Change in the magnitude of chroma
$\Delta h^\circ$ | Change in the hue angle

$\Delta E$ values are calculated with the [python-colormath](https://python-colormath.readthedocs.io/en/latest/) package. The other metrics are simply differences ($x_1-x_2=metric$) between the test formula and the standard of that set.

### Other Functionality
Here is some other functionality that doesn't fit neatly into other sections.

A backup of the final product file is made in the case that the next run of the program makes a big ol' mess of the product and it becomes unusable.