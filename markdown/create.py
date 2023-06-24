# Just to create empty xx.md shell files 
# according to the number of chapters in each book

import pandas as pd
import os.path

# Import the book and chapter description data as pandas dataframe
books = pd.read_csv("https://raw.githubusercontent.com/kreier/study/main/markdown/chapters.csv")

# Process bible books one by one
total_output_errors = 0

for index, row in books.iterrows():
    for chapter in range(1, row.chapters + 1):
        output_data = f"## {row.book} {chapter}\n\n```\nTBD\n```\n\n"
        outputfile = f'{row.folder}/{chapter:02d}.md'
        # write xx.md directly into the folder with the highlights
        # for safety there should be a check if the file exists and would not be overwritten!
        if os.path.isfile(outputfile):
            print("x", end="")
        else:
            print(f"{outputfile} ", end="")
            try:
                with open(outputfile, 'w', encoding="utf8") as output:    
                    output.write(output_data)
            except OSError as e:
                total_output_errors += 1

print(f"\nExport errors: {total_output_errors}")
