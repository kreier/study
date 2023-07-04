# Read the content of all 66 book files and compile one large markdown file in 
# the /docs folder for https://kreier.github.io/study/bible

import datetime
import pandas as pd
import os
from md2pdf.core import md2pdf

# Check execution location, exit if not in /markdown
if os.getcwd()[-8:] != "markdown":
    print("This script must be executed inside the markdown folder.")
    exit()

logging.basicConfig(level=logging.DEBUG, filename='../docs/compile.log', format='%(asctime)s %(levelname)s:%(message)s')

# Import the book and chapter description data as pandas dataframe
books = pd.read_csv("https://raw.githubusercontent.com/kreier/study/main/markdown/chapters.csv")

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
    print(f"Processing the {index}. book: {row.book}")

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

# write compiled_markdown_aio.md
try:
    with open(f'../docs/compiled_markdown_aio.md', 'w') as output:
        output.write(f"<!-- generated {datetime.datetime.now()} -->\n")
        output.write(summary_html)
except OSError as e:
    total_output_errors += 1


logging.debug(f"Processed {total_chapters} chapters. That's {total_chapters / 1189 * 100:.1f} Percent. They contain {total_words} words. {total_import_errors} import errors. {total_output_errors} output errors.")
