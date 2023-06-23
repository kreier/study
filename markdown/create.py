# Just to create empty xx.md shell files from a copy of the 01.md file
# according to the number of chapters in each book

import pandas as pd

# Import the book and chapter description data as pandas dataframe
books = pd.read_csv("https://raw.githubusercontent.com/kreier/study/main/markdown/chapters.csv")

# Process bible books one by one
total_import_errors = 0
total_output_errors = 0

for index, row in books.iterrows():
    if index > 16:
        # import the 01.md
        inputfile = f'{row.folder}/01.md'
        print(f"\nImported: {inputfile} \nExport: ")
        try:
            with open(inputfile, 'r', encoding="utf8") as input:
                file_data = input.read()
        except OSError as e:
            total_import_errors += 1
        for chapter in range(2, row.chapters + 1):
            outputfile = f'{row.folder}/{chapter:02d}.md'
            print(f"{outputfile} ", end="")

            # write README.md directly into the folder with the highlights
            try:
                with open(outputfile, 'w', encoding="utf8") as output:    
                    output.write(file_data)
            except OSError as e:
                total_output_errors += 1

print(f"\nImport errors: {total_import_errors}")
print(f"Export errors: {total_output_errors}")
