

class TextSection:
    
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.lines = []
        self.sections = []
        self.sectionPos = []
        self.lineNum = 0
        self.repeat = 0

    def addLine(self, line):
        self.lines.append(line)
        self.lineNum+= 1

    def addSection(self, section):
        self.sections.append(section)
        self.sectionPos.append(self.lineNum)

    def expand(self):
        for i

class VerilogTemplate:
    
    def __init__(self, template, output);
        self.template = template
        self.output = output
        self.sections = []

    def readTemplate(self):
        lines = []
        with open(self.template, 'r') as f:
            lines = f.readlines()
        currentSection = TextSection('base', None)
        for line in lines:
            if line[:2] == '#<':
                section = TextSection(line[2:], currentSection)
                currentSection.addSection(section)
                currentSection = section
            if line[:2] == '#>' and line[2:] == section.name:
                currentSection = currentSection.parent
            else:
                currentSection.addLine(line)

                
