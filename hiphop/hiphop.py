import argparse
import jinja2
import re

META_RE = re.compile(r'^(\d+-\d+-\d+ \d+:\d+:\d+)\s+(\S+)')

REGEXES = [
    re.compile(r'\b(https?://soundcloud.com\S+)'),
    re.compile(r'\b(https?://www.youtube.com\S+)'),
    re.compile(r'\b(https?://open.spotify.com\S+)'),
]


def generate(input_file, output_file):
    links = []
    for line in input_file:
        if 'Link' in line:
            continue
        for r in REGEXES:
            m = r.search(line)
            if m:
                m2 = META_RE.match(line)
                if not m2:
                    continue
                when, who = m2.groups()
                who = who.lstrip('@')
                links.append((when, who, m.groups()[0]))

    links.reverse()

    template_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates/'))
    template = template_env.get_template('index.html')
    output_file.write(template.render(links=links))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('logfile')
    args = parser.parse_args()
    with open(args.logfile) as logfile:
        with open('hiphop.html', 'w') as outfile:
            generate(logfile, outfile)


if __name__ == '__main__':
    main()