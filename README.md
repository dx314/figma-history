## Figma Version History Analyzer

This Python script retrieves the version history of a Figma project file and calculates the start and finish times of changes per day. The output is saved in a CSV file called raw_data.csv. Additionally, it generates a line graph showing the duration of changes per day with a baseline at 8 hours. The graph are saved as PNG files in the local directory.

## Features

- Retrieves version history for a Figma project file
- Calculates daily start and finish times of changes
- Saves version history data in CSV format
- Plots a line graph of the duration of changes per day with an 8-hour baseline
- Converts timestamps from UTC to GMT+8

## Prerequisites

To use this script, you need Python 3.6 or higher installed on your system.

You also need the following Python libraries:

- requests
- matplotlib
- pandas
- pytz

You can install these libraries using pip:

```bash
pip install requests matplotlib pandas pytz
```

## Usage

1. Clone this repository or download the script to your local machine.
2. Run the script by providing the Figma API key and a list of file IDs as command-line arguments:

```bash
python figma_version_analyzer.py <YOUR_PERSONAL_ACCESS_TOKEN> <FILE_ID_1> <FILE_ID_2>
```

Replace <YOUR_PERSONAL_ACCESS_TOKEN> with your Figma API key and <FILE_ID_1>, <FILE_ID_2>, ... with the Figma file IDs you want to analyze.
3. The version history data will be saved in a CSV file named raw_data.csv.
4. Generate line graphs, where days is the number of days you want to plot. If you left empty, it will plot all the days.

```bash
python gen_graphs.py --days <NUMBER_OF_DAYS>
```

5. The line graph of the duration of changes per day will be saved as a PNG image named duration_line_graph.png.

## License

This project is licensed under the MIT License. See the LICENSE file for details.