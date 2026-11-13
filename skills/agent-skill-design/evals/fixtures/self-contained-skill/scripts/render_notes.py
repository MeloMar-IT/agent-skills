import string
import sys


def main():
    lines = open(sys.argv[1]).read().splitlines()
    groups = {"feat": [], "fix": []}
    for line in lines:
        for key in groups:
            if line.startswith(key + ":"):
                groups[key].append("- " + line.split(":", 1)[1].strip())
    tmpl = string.Template(open("templates/notes.tmpl").read())
    print(tmpl.substitute(features="\n".join(groups["feat"]), fixes="\n".join(groups["fix"])))


if __name__ == "__main__":
    main()
