# Read the content of all 1189 chapter files from the 66 books and compile the 
# respective 66 summary README.md in the folders. Then copy a conversion to the 
# /docs folder for https://kreier.github.io/study/bible

import logging

logging.basicConfig(level=logging.DEBUG, filename='compile.log', format='%(asctime)s %(levelname)s:%(message)s')

# Import the book and chapter description data as pandas dataframe

import pandas as pd

books = pd.read_csv("https://raw.githubusercontent.com/kreier/study/main/markdown/chapters.csv")
# print(books.info())


# Process one book by one

text_markdown =""
total_words = 0
total_chapters = 0
total_import_errors = 0
total_output_errors = 0

for index, row in books.iterrows():
    for chapter in range(row.chapters):
        filename = f'{row.folder}/{chapter:02d}.md'
        try:
            with open(filename, 'r') as input:
                file_data = input.read()
                words = file_data.split(" ")
                num_words = len(words)
                # logging.debug(f"{filename} has {num_words} words")
                total_words += num_words
                total_chapters += 1
                text_markdown += file_data
            text_markdown += '\n'
        except OSError as e:
            total_import_errors += 1
            # logging.error(f"error reading {filename}")
    try:
        with open(f'{row.folder}/README.md', 'w') as output:    
            output.write(text_markdown)
    except OSError as e:
        total_output_errors += 1
    text_markdown = ""  

logging.debug(f"""Processed {total_chapters} chapters. That's {total_chapters / 1189 * 100:.1f} Percent. They contain {total_words} words. {total_import_errors} import errors. {total_output_errors} output errors.""")
