# -*- coding: ISO-8859-1 -*-
#
#
# Copyright (C) 2006, 2007 André Wobst <wobsta@users.sourceforge.net>
#
# This file is part of PyX (http://pyx.sourceforge.net/).
#
# PyX is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PyX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyX; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA


# Just a quick'n'dirty ascii art (I'll do a nice PyX plot later on):
#
#
#      node1 *
#            | \
#            |   \  neighbor2
#            |     \
#            |       \
#  neighbor3 |element * node3
#            |       /
#            |     /
#            |   /  neighbor1
#            | /
#      node2 *


import struct, binascii, zlib
import bbox, canvas, color, pdfwriter, unit


class node_pt:

    def __init__(self, coords_pt, value):
        self.coords_pt = coords_pt
        self.value = value


class node(node_pt):

    def __init__(self, coords, value):
        node_pt.__init__(self, [unit.topt(coord) for coord in coords], value)


class element:

    def __init__(self, nodes, neighbors=None):
        self.nodes = nodes
        self.neighbors = neighbors


def coords24bit_pt(coords_pt, min_pt, max_pt):
    return struct.pack(">I", int((coords_pt-min_pt)*16777215.0/(max_pt-min_pt)))[1:]


class PDFGenericResource(pdfwriter.PDFobject):

    def __init__(self, type, name, content):
        pdfwriter.PDFobject.__init__(self, type, name)
        self.content = content

    def write(self, file, writer, registry):
        file.write(self.content)


class mesh(canvas.canvasitem):

    def __init__(self, elements, check=1):
        self.elements = elements
        if check:
            colorspacestring = ""
            for element in elements:
                if len(element.nodes) != 3:
                    raise ValueError("triangular mesh expected")
                try:
                    for node in element.nodes:
                        if not colorspacestring:
                            colorspacestring = node.value.colorspacestring()
                        elif node.value.colorspacestring() != colorspacestring:
                            raise ValueError("color space mismatch")
                except AttributeError:
                    raise ValueError("gray, rgb or cmyk color values expected")
                for node in element.nodes:
                    if len(node.coords_pt) != 2:
                        raise ValueError("two dimensional coordinates expected")

    def bbox(self):
        return bbox.bbox_pt(min([node.coords_pt[0] for element in self.elements for node in element.nodes]),
                            min([node.coords_pt[1] for element in self.elements for node in element.nodes]),
                            max([node.coords_pt[0] for element in self.elements for node in element.nodes]),
                            max([node.coords_pt[1] for element in self.elements for node in element.nodes]))

    def data(self, bbox):
        return "".join(["\000%s%s%s" % (coords24bit_pt(node.coords_pt[0], bbox.llx_pt, bbox.urx_pt),
                                        coords24bit_pt(node.coords_pt[1], bbox.lly_pt, bbox.ury_pt),
                                        node.value.tostring8bit())
                        for element in self.elements for node in element.nodes])

    def processPS(self, file, writer, context, registry, bbox):
        thisbbox = self.bbox()
        bbox += thisbbox
        file.write("""<< /ShadingType 4
/ColorSpace %s
/BitsPerCoordinate 24
/BitsPerComponent 8
/BitsPerFlag 8
/Decode [%f %f %f %f %s]
/DataSource currentfile /ASCIIHexDecode filter /FlateDecode filter
>> shfill\n""" % (self.elements[0].nodes[0].value.colorspacestring(),
                  thisbbox.llx_pt, thisbbox.urx_pt, thisbbox.lly_pt, thisbbox.ury_pt,
                  " ".join(["0 1" for value in self.elements[0].nodes[0].value.tostring8bit()])))
        file.write(binascii.b2a_hex(zlib.compress(self.data(thisbbox))))
        file.write("\n")

    def processPDF(self, file, writer, context, registry, bbox):
        thisbbox = self.bbox()
        bbox += thisbbox
        d = self.data(thisbbox)
        if writer.compress:
            filter = "/Filter /FlateDecode\n"
            d = zlib.compress(d)
        else:
            filter = ""
        name = "shading-%s" % id(self)
        shading = PDFGenericResource("shading", name, """<< /ShadingType 4
/ColorSpace %s
/BitsPerCoordinate 24
/BitsPerComponent 8
/BitsPerFlag 8
/Decode [%f %f %f %f %s]
/Length %i
%s>>
stream
%s
endstream\n""" % (self.elements[0].nodes[0].value.colorspacestring(),
                  thisbbox.llx_pt, thisbbox.urx_pt, thisbbox.lly_pt, thisbbox.ury_pt,
                  " ".join(["0 1" for value in self.elements[0].nodes[0].value.tostring8bit()]),
                  len(d), filter, d))
        registry.add(shading)
        registry.addresource("Shading", name, shading)
        file.write("/%s sh\n" % name)
