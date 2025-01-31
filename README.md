# Murphy-Lab-LI-Graphs
Code to analyze and graph chemotaxis data

## Set Up:
For this code you will need to have pandas, matplotlib, and seaborn installed

Install commands:

    pip install pandas
    pip install matplotlib
    pip install seaborn

If there is a problem with pandas you may need to downgrade your numpy with the command:

    pip install numpy==1.26.4  pyyaml

The error is occuring due to incompatable versions of numpy and pandas

## File formatting:
Make sure you are using CSV files and not Excel files

Make sure there aren't any extra labels
ie. the experiment name in a cell at the top corner

Any extra pieces that appear at the top before the data labels will mess up the formatting of the dataframe
so it is absolutly necessary to remove them

Extra cells such as calculations or copied sections that fall outside of the first set of columns will be ignored completly
As such, it is ok for there to be data in these locations, but it will not be used

Similarly, make sure all of the data falls into one set of columns, not multiple sets next to each other
There should be one column for all of the strains, one for all of the times, etc.
The code will also calculate CI values so they are not necessary for input

## Running the code:
Run the code as you would run any other python file
When prompted, input the path to the file
If the file you are analyzing is in the same folder as the code, you should only need to put the name of the file
Otherwise, you can put the realive path

Make sure the file location DOES NOT have quotes around it
If the input isn't working, first try switching to the full path (instead of the realive)
If that still doesn't fix it, try flipping the direction of the slashes in the file location
I honestly don't know why this fixes it, but sometimes it does

If that still doesn't resolve the issue, write a comment

## Debugging:
I tried to give the necessary comments to understand the code and what the different bits do
to hopefully aid in any modifications necessary but again feel free to reach out with questions