# read all the 50 chapter files as markdown and compile them into one README.md

text_markdown =""

for index in range(18):
    filename = f'{index:02d}.md'
    print(filename)
    with open(filename, 'r') as input:
        text_markdown += input.read()
    text_markdown += '\n'

with open('README.md', 'w') as output:
    output.write(text_markdown)
