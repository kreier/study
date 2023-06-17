# read all the 50 chapter files as markdown and compile them into one README.md

import logging
import os
import datetime

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

log = logging.getLogger("compilation")

log.info(datetime.datetime.now())
log.info("Starting processing ...")

text_markdown =""

print("Compiling: ", end='')

for index in range(38):
    filename = f'{index:02d}.md'
    print(filename, end=' ')
    with open(filename, 'r') as input:
        text_markdown += input.read()
    text_markdown += '\n'

with open('README.md', 'w') as output:
    output.write(text_markdown)
