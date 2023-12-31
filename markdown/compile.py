# Read the content of all 1189 chapter files from the 66 books and compile the 
# respective 66 summary README.md in the folders. Then copy a conversion to the 
# /docs folder for https://kreier.github.io/study/bible
# v0.1 creates 66 README.md files in /markdown/$book$/ and /docs/bible/$book$/
# v0.2 creates summary files /markdown /docs and /

import logging
import datetime
import pandas as pd
import os

# Check execution location, exit if not in /markdown
if os.getcwd()[-9:] != "\markdown":
    print("This script must be executed inside the markdown folder.")
    exit()

logging.basicConfig(level=logging.DEBUG, filename='compile.log', format='%(asctime)s %(levelname)s:%(message)s')

# Import the book and chapter description data as pandas dataframe
books = pd.read_csv("https://raw.githubusercontent.com/kreier/study/main/markdown/chapters.csv")
# print(books.info())


# Process bible books one by one
summary_string = ""
summary_html = ""
summary_readme = ""
total_words = 0
total_chapters = 0
total_import_errors = 0
total_output_errors = 0

for index, row in books.iterrows():
    processed_chapters = 0
    text_markdown = ""  
    for chapter in range(row.chapters + 1):
        filename = f'{row.folder}/{chapter:02d}.md'
        try:
            with open(filename, 'r', encoding="utf8") as input:
                file_data = input.read()
                words = file_data.split(" ")
                num_words = len(words)
                # logging.debug(f"{filename} has {num_words} words")
                text_markdown += file_data
                if chapter > 0:
                    processed_chapters += 1
                    total_words += num_words
                    total_chapters += 1
                print(filename, end=' ')
            text_markdown += '\n'
        except OSError as e:
            total_import_errors += 1
            # logging.error(f"error reading {filename}")

    # write README.md directly into the folder with the highlights
    try:
        with open(f'{row.folder}/README.md', 'w', encoding="utf8") as output:    
            output.write(text_markdown)
    except OSError as e:
        total_output_errors += 1

    # write README.md to the respective folder https://kreier.github.io/study/bible/$book$
    try:
        with open(f'../docs/bible/{row.html_folder}/README.md', 'w', encoding="utf8") as output:    
            output.write(text_markdown)
    except OSError as e:
        total_output_errors += 1
        # print(f"{row.html_folder}")

    # update the strings for each book of the bible
    summary_string += f"[{row.book}]({row.folder}/) {processed_chapters}/{row.chapters}, "
    summary_html += f"[{row.book}](bible/{row.html_folder}/) {processed_chapters}/{row.chapters}, "
    summary_readme += f"[{row.book}](docs/bible/{row.html_folder}/) {processed_chapters}/{row.chapters}, "
    if index == 38:
        summary_html += "\n\n"
        summary_string += "\n\n"
        summary_readme += "\n\n"

summary_compilation = f"\n\nSummary of compilation: {total_chapters}/1189\n"
summary_string += summary_compilation
summary_html += summary_compilation
summary_readme += summary_compilation

# write README.md to folder https://kreier.github.io/study/markdown/
try:
    with open(f'README.md', 'w') as output:
        output.write("# Overview of processed files \n\n")
        output.write(summary_string)
        output.write(f"\n\nlast updated: {datetime.datetime.now()}\n")
except OSError as e:
    total_output_errors += 1

part1 = part2 = header = miracles = ""
# write README.md to the overview page for https://kreier.github.io/study/
# get part 1
try:
    with open('../docs/part1.md', 'r') as input:
        part1 = input.read()
except OSError as e:
    total_import_errors += 1

# get part 2
try:
    with open('../docs/part2.md', 'r') as input:
        part2 = input.read()
except OSError as e:
    total_import_errors += 1

# write README.md
try:
    with open(f'../docs/README.md', 'w') as output:
        output.write(f"<!-- generated {datetime.datetime.now()} -->\n")
        output.write(part1)
        output.write(summary_html)
        output.write(part2)
except OSError as e:
    total_output_errors += 1


# write README.md in the root folder of the repository https://kreier.github.io/study/
# get header
try:
    with open('../markdown/header.md', 'r') as input:
        header = input.read()
except OSError as e:
    total_import_errors += 1

# get miracles
try:
    with open('../miracles/README.md', 'r') as input:
        miracles = input.read()
except OSError as e:
    total_import_errors += 1

# write README.md
try:
    with open(f'../README.md', 'w') as output:
        output.write(header)
        output.write(summary_readme)
        output.write("\n")
        output.write(miracles)
        output.write(f"\nlast updated: {datetime.datetime.now()}\n")
except OSError as e:
    total_output_errors += 1


# update the root README.md in https://kreier.github.io/study/bible/
# TBD - provide links all the chapters

logging.debug(f"Processed {total_chapters} chapters. That's {total_chapters / 1189 * 100:.1f} Percent. They contain {total_words} words. {total_import_errors} import errors. {total_output_errors} output errors.")
