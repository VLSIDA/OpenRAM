
class text_section:

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.lines = []
        self.sections = []
        self.sectionPos = []
        self.lineNum = 0
        self.repeat = 1

    def addLine(self, line):
        self.lines.append(line)
        self.lineNum+= 1

    def addSection(self, section):
        self.sections.append(section)
        self.sectionPos.append(self.lineNum)

    def expand(self):
        expanded = []
        pos = 0
        if self.repeat == 0:
            return []
        if len(self.sections) == 0:
            return self.lines * self.repeat

        for s, sPos in zip(self.sections, self.sectionPos):
            if pos < sPos:
                expanded += self.lines[pos:sPos]
                pos = sPos
            expanded += s.expand()

        if pos < self.lineNum:
            expanded += self.lines[pos:]

        if self.repeat > 1:
            expanded = expanded * self.repeat

        return expanded


class verilog_template:

    def __init__(self, template):
        self.template = template
        self.sections = {}
        self.textDict = {}
        self.baseSection = None
        self.expanded = None

    def readTemplate(self):
        lines = []
        with open(self.template, 'r') as f:
            lines = f.readlines()
        self.baseSection = text_section('base', None)
        currentSection = self.baseSection
        for line in lines:
            if line[:2] == '#<':
                section = text_section(line[2:].strip('\n'), currentSection)
                currentSection.addSection(section)
                currentSection = section
            elif line[:2] == '#>' and line[2:].strip('\n') == currentSection.name:
                self.sections[currentSection.name] = currentSection
                currentSection = currentSection.parent
            else:
                currentSection.addLine(line)

    def expand(self):
        self.expanded = self.baseSection.expand()

    def postProcess(self):
        text = ""
        for line in self.expanded:
            if '#$' in line:
                while True:
                    indStart = line.find('#$')
                    if indStart == -1:
                        break
                    indEnd = line.find('$#')
                    line = line[:indStart] + str(self.textDict[line[indStart + 2:indEnd]]) + line[indEnd + 2:]
                text += line
            elif '#!' in line:
                indLabelStart = line.find('#!') + 2
                indLabelEnd = line.find('!', indLabelStart)
                label = line[indLabelStart:indLabelEnd]
                self.textDict[label] = eval(line[indLabelEnd + 1:-1], self.textDict)
            else:
                text += line
        return text

    def generate(self, filename):
        self.expand()
        text = self.postProcess()
        with open(filename, 'w') as f:
            f.write(text)

    def setSectionRepeat(self, name, repeat):
        self.sections[name].repeat = repeat

    def setTextDict(self, label, value):
        self.textDict[label] = value
