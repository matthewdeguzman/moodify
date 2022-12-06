from pathlib import Path
import csv
import os

# retrieve parent directory
directory = Path(__file__).resolve().parent.parent

data = []
max_size = 100000

# Clean up the dataset to remove irrelevant data
with open(os.path.join(directory, 'track_dataset.csv'), 'r', encoding='utf-8') as f:
    reader = csv.reader(f)

     # iterates through every row in the csv file and grabs the relevant data
    for row in reader:
        new_data = row[:1] + row[9:11] + row[12:13] + row[17:18]
        data.append(new_data)

        # writes the data to the new csv file once data has reached a max size
        if len(data) == max_size:
            with open(os.path.join(directory, 'new-data.csv'), 'a', encoding='utf-8', newline='') as g:
                writer = csv.writer(g)
                writer.writerows(data)

            # clears the elements in data to make room for more
            data.clear()

    # writes the remaining data to the csv file
    if len(data) > 0:
        with open(os.path.join(directory, 'new-data.csv'), 'a', encoding='utf-8', newline='') as g:
                writer = csv.writer(g)
                writer.writerows(data)