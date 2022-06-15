import re


class baseSection:
    children = []

    def expand(self, dict, fd):
        for c in self.children:
            c.expand(dict, fd)


class loopSection(baseSection):

    def __init__(self, var, key):
        self.children = []
        self.var = var
        self.key = key

    def expand(self, dict, fd):
        for ind in dict[self.key]:
            dict[self.var] = ind
            for c in self.children:
                c.expand(dict, fd)
        if self.var in dict:
            del dict[self.var]


class textSection(baseSection):

    def __init__(self, text):
        self.text = text

    def expand(self, dict, fd):
        var_re = re.compile('\{\{ (\S*) \}\}')
        vars = var_re.finditer(self.text)
        newText = self.text
        for var in vars:
            newText = newText.replace('{{ ' + var.group(1) + ' }}', str(dict[var.group(1)]))
        print(newText, end='', file=fd)


class template:

    def __init__(self, template, dict):
        self.template = template
        self.dict = dict

    def readTemplate(self):
        lines = []
        with open(self.template, 'r') as f:
            lines = f.readlines()

        self.baseSectionSection = baseSection()
        sections = []
        context = [self.baseSectionSection]
        for_re = re.compile('\{% for (\S*) in (\S*) %\}')
        end_re = re.compile('\{% endfor %\}')
        for line in lines:
            m = for_re.match(line)
            if m:
                section = loopSection(m.group(1), m.group(2))
                sections.append(section)
                context[-1].children.append(section)
                context.append(section)
                continue
            if end_re.match(line):
                context.pop()
            else:
                context[-1].children.append(textSection(line))

    def write(self, filename):
        fd = open(filename, 'w')
        self.readTemplate()
        self.baseSectionSection.expand(self.dict, fd)
        fd.close()
