"""Single-port synchronous SRAM assembled from foundry SRAM hard cells.

Requests are captured on the rising edge and access starts on the falling
edge, matching OpenRAM's behavioral model. BLDRV owns precharge, column
selection, and write drive; none of those generic arrays are instantiated.
"""

from openram import OPTS
from openram.base import design, lef, verilog
from openram.sram_factory import factory
from openram.tech import spice


class ihp_sram(design, verilog, lef):
    def __init__(self, name, sram_config):
        if (sram_config.num_words != 64 or sram_config.num_banks != 1
                or sram_config.words_per_row != 4
                or not 1 <= sram_config.word_size <= 8
                or sram_config.num_spare_rows or sram_config.num_spare_cols
                or sram_config.write_size != sram_config.word_size
                or (OPTS.num_rw_ports, OPTS.num_w_ports, OPTS.num_r_ports) != (1, 0, 0)):
            raise ValueError("IHP SRAM requires 64 words, 1..8 bits, mux4, one RW port, "
                             "one bank, full-word writes, and no spares")
        if OPTS.analytical_delay or OPTS.use_pex or OPTS.trim_netlist:
            raise ValueError("IHP SRAM currently requires simulation characterization, "
                             "use_pex=False, and trim_netlist=False")
        design.__init__(self, name)
        lef.__init__(self, ["m1", "m2", "m3", "m4", "m5"])
        self.lef_units = 1000  # Match the installed SG13G2 technology LEF.
        verilog.__init__(self)
        self.sram_config = sram_config
        sram_config.set_local_config(self)
        self.num_wmasks = 0
        self.vdd_name, self.gnd_name = spice["power"], spice["ground"]
        # Match the generic top's netlist-only Liberty area convention.
        self.width = self.height = 0

    def create_netlist(self):
        self.request_pins = ([f"din0[{i}]" for i in range(self.word_size)]
                             + [f"addr0[{i}]" for i in range(self.addr_size)]
                             + ["csb0", "web0"])
        self.request_nets = ([f"data_{i}" for i in range(self.word_size)]
                             + [f"address_{i}" for i in range(self.addr_size)]
                             + ["csb_q", "web_q"])
        for pin in self.request_pins + ["clk0"]:
            self.add_pin(pin, "INPUT")
        for bit in range(self.word_size):
            self.add_pin(f"dout0[{bit}]", "OUTPUT")
        self.add_pin(self.vdd_name, "POWER")
        self.add_pin(self.gnd_name, "GROUND")
        self.registers = factory.create(module_type="ihp_input_registers",
                                        bits=len(self.request_pins))
        self.register_inst = self.add_inst("request", self.registers)
        self.connect_inst(self.request_pins + self.request_nets
                          + ["clk0", self.vdd_name, self.gnd_name])
        inv = factory.create(module_type="ihp_control_cell", kind="inv")
        and2 = factory.create(module_type="ihp_control_cell", kind="and2")
        self.interface_insts = []
        for name, source, target in (("access_clock", "clk0", "clk_n"),
                                      ("select", "csb_q", "cs"),
                                      ("write_enable", "web_q", "we")):
            inst = self.add_inst(name, inv)
            self.connect_inst([source, target, self.vdd_name, self.gnd_name])
            self.interface_insts.append(inst)
        self.control = factory.create(module_type="ihp_control_logic")
        self.control_inst = self.add_inst("control", self.control)
        self.connect_inst(["clk_n", "cs", "web_q", "we", "row_cs", "eclk",
                           "pre_n", "sae", "wclk", self.vdd_name, self.gnd_name])
        self.write_insts = []
        for bit in range(self.word_size):
            insts = []
            for name, mod, nodes in (
                ("invert", inv, [f"data_{bit}", f"data_bar_{bit}"]),
                ("one", and2, [f"data_{bit}", "wclk", f"wr_one_{bit}"]),
                ("zero", and2, [f"data_bar_{bit}", "wclk", f"wr_zero_{bit}"]),
            ):
                insts.append(self.add_inst(f"write_{bit}_{name}", mod))
                self.connect_inst(nodes + [self.vdd_name, self.gnd_name])
            self.write_insts.append(insts)
        self.memory = factory.create(module_type="ihp_row_memory", cols=self.num_cols)
        self.memory_inst = self.add_inst("memory", self.memory)
        memory_nets = [f"address_{i + 2}" for i in reversed(range(4))]
        memory_nets += ["row_cs", "eclk", "address_1", "address_0"]
        for bit in range(self.word_size):
            memory_nets += ["pre_n", "sae", f"wr_one_{bit}", f"wr_zero_{bit}",
                            f"dout0[{bit}]", f"qn_unused_{bit}"]
        self.connect_inst(memory_nets + [self.vdd_name, self.gnd_name])

    def get_cell_name(self, instance_name, row, col):
        cell = self.memory.memory.array.cell_inst[row, col]
        sep = OPTS.hier_seperator
        root = instance_name if instance_name.lower().startswith("x") else "x" + instance_name
        return (sep.join([root, "xmemory", "xmemory", "xarray",
                          "x" + cell.name]), cell)

    def get_characterization_probes(self, row, col, port):
        if port != 0:
            raise ValueError("IHP SRAM has only port 0")
        sep = OPTS.hier_seperator
        return {"bl": sep.join(["x" + self.name, "xmemory", "xmemory", f"bl_0_{col}"]),
                "br": sep.join(["x" + self.name, "xmemory", "xmemory", f"br_0_{col}"]),
                "sen": sep.join(["x" + self.name, "sae"])}

    def create_layout(self):
        # Keep the foundry array/BLDRV assembly intact.  The thin request row
        # sits below it; the cycle controller occupies the right-hand bay.
        self.register_inst.place((2, 2))
        self.memory_inst.place((2, 15))
        self.control_inst.place((self.memory.width + 6, 15))
        x = 2
        for inst in self.interface_insts + [i for group in self.write_insts for i in group]:
            inst.place((x, 72))
            x += inst.mod.width - .51
        # Bridge the one-row library's site gaps, as in the request bank.
        # This keeps its supply rails continuous rather than escaping every
        # gate separately through the signal-routing layers.
        for y in (72, 76.2):
            self.add_rect("m1", (2.51, y), width=x - 2.51, height=.6)
        self.width = max(self.registers.width + 4, self.control_inst.rx() + 2, x + 2)
        self.height = 83
        for index, name in enumerate(self.request_pins):
            pin = self.register_inst.get_pin(self.registers.data_names[index])
            self.add_layout_pin(name, "m5", (pin.cx() - .15, 0), .3, 1)
        pin = self.register_inst.get_pin("clk")
        self.add_layout_pin("clk0", "m5", (pin.cx() - .15, 0), .3, 1)
        for bit in range(self.word_size):
            pin = self.memory_inst.get_pin(f"qp_{bit}")
            self.add_layout_pin(f"dout0[{bit}]", "m5", (pin.cx() - .15, self.height - 1), .3, 1)
        for name, x in ((self.vdd_name, self.width - 2), (self.gnd_name, self.width - 4)):
            self.add_layout_pin(name, "m5", (x, 0), .6, 1)
        self._route_macro()
        self.add_boundary()

    def _route_macro(self):
        """Route real hard-cell metal, not rectangular hierarchy blockages.

        Source pins have 0.51 um pitch and cannot accept the generic square
        minimum-area via pads.  Narrow, tall pads preserve that pitch.  Metal
        connectivity is extracted before routing so existing supply straps
        and signal wiring remain available only to their own nets.
        """
        import heapq
        import tempfile
        import klayout.db as kdb
        import numpy as np
        from matplotlib.path import Path
        from openram.base import vector
        from openram.tech import layer

        metals = ["m1", "m2", "m3", "m4", "m5"]
        with tempfile.NamedTemporaryFile(suffix=".gds") as stream:
            self.gds_write(stream.name)
            layout = kdb.Layout()
            layout.read(stream.name)
        top = layout.top_cell()
        top.flatten(True)
        extractor = kdb.LayoutToNetlist(kdb.RecursiveShapeIterator(layout, top, []))
        regions = [extractor.make_polygon_layer(layout.layer(*layer[n]), n) for n in metals]
        vias = [extractor.make_polygon_layer(layout.layer(*layer[f"via{i}"]), f"via{i}")
                for i in range(1, 5)]
        for region in regions:
            extractor.connect(region)
        for i, via in enumerate(vias):
            extractor.connect(regions[i], via)
            extractor.connect(via, regions[i + 1])
        extractor.extract_netlist()
        dbu = layout.dbu

        def point(x, y):
            return kdb.Point(round(x / dbu), round(y / dbu))

        def box(x, y, dx, dy):
            p = point(x, y)
            return kdb.Box(p.x - round(dx / dbu), p.y - round(dy / dbu),
                           p.x + round(dx / dbu), p.y + round(dy / dbu))

        # The physical terminals are obtained from the actual netlist order.
        terminals = {}
        own = {}
        seen = set()
        connections = [(inst, pin, name) for inst in self.insts
                       for pin, name in zip(inst.spice_pins, inst.get_connections())]
        connections += [(self, name, name) for name in self.pin_map]
        for inst, pin_name, name in connections:
            pins = sorted(inst.get_pins(pin_name), key=lambda p: (p.layer, p.lx(), p.by()))
            pin = pins[0]
            index = metals.index(pin.layer)
            net = extractor.probe_net(regions[index], point(pin.cx(), pin.cy()))
            if net is None:
                raise ValueError(f"No physical net at {inst.name}/{pin_name}")
            shapes = [extractor.shapes_of_net(net, r, True) for r in regions]
            own.setdefault(name, [kdb.Region() for _ in metals])
            for i in range(5):
                own[name][i] += shapes[i]
            key = (name, net.cluster_id)
            if key not in seen:
                terminals.setdefault(name, []).append((inst, pin_name, pins, shapes))
                seen.add(key)
        all_shapes = [kdb.Region(top.begin_shapes_rec(layout.layer(*layer[n]))).merged()
                      for n in metals]
        cuts = [kdb.Region(top.begin_shapes_rec(layout.layer(*layer[f"via{i}"]))).merged()
                for i in range(1, 5)]
        routed = [kdb.Region() for _ in metals]
        # A fine routing grid is independent of the 5 nm manufacturing grid.
        pitch = .1
        nx, ny = int(self.width / pitch) + 1, int(self.height / pitch) + 1
        xs, ys = np.arange(nx) * pitch, np.arange(ny) * pitch

        def raster(region):
            result = np.zeros((ny, nx), dtype=bool)
            for polygon in region.each_merged():
                bounds = polygon.bbox()
                x0 = max(0, int(bounds.left * dbu / pitch) - 1)
                x1 = min(nx, int(bounds.right * dbu / pitch) + 2)
                y0 = max(0, int(bounds.bottom * dbu / pitch) - 1)
                y1 = min(ny, int(bounds.top * dbu / pitch) + 2)
                xx, yy = np.meshgrid(xs[x0:x1], ys[y0:y1])
                coords = np.column_stack((xx.ravel(), yy.ravel()))
                hull = [(p.x * dbu, p.y * dbu) for p in polygon.each_point_hull()]
                mask = Path(hull).contains_points(coords, radius=1e-7)
                for hole in range(polygon.holes()):
                    ring = [(p.x * dbu, p.y * dbu) for p in polygon.each_point_hole(hole)]
                    mask &= ~Path(ring).contains_points(coords, radius=-1e-7)
                result[y0:y1, x0:x1] |= mask.reshape(yy.shape)
            return result

        def add_wire(index, coords, name):
            if len(coords) < 2:
                return
            simplified = []
            for coord in coords:
                if simplified and coord == simplified[-1]:
                    continue
                if len(simplified) > 1 and ((simplified[-2][0] == simplified[-1][0] == coord[0])
                                            or (simplified[-2][1] == simplified[-1][1] == coord[1])):
                    simplified.pop()
                simplified.append(coord)
            coords = simplified
            if len(coords) < 2:
                return
            shape = kdb.Region(kdb.Path([point(*p) for p in coords], round(.26 / dbu),
                                       round(.13 / dbu), round(.13 / dbu)))
            if index >= 2 and not (shape.sized(round(.24 / dbu)) & foreign[index]).is_empty():
                raise ValueError(f"Unsafe wire {name} on {metals[index]}: {coords}")
            self.add_path(metals[index], coords, width=.26)
            for x, y in (coords[0], coords[-1]):
                self.add_rect(metals[index], (x - .13, y - .13), .26, .26)
            # Model the corner squares emitted by OpenRAM as well as the
            # end squares needed to turn from an off-grid access point.
            routed[index] += shape
            own[name][index] += shape

        def add_via(x, y, lower, upper, name, horizontal_layers=()):
            p = vector(x, y)
            for i in range(max(lower, 2), upper + 1):
                dx, dy = (.52, .37) if i in horizontal_layers else (.37, .52)
                if not (kdb.Region(box(x, y, dx, dy)) & foreign[i]).is_empty():
                    raise ValueError(f"Unsafe via {name} on {metals[i]} at {x}, {y}")
            for i in range(lower, upper):
                self.add_rect(f"via{i + 1}", p - vector(.095, .095), .19, .19)
                cuts[i] += kdb.Region(box(x, y, .095, .095))
            for i in range(lower, upper + 1):
                dx, dy = (.28, .13) if i in horizontal_layers else (.13, .28)
                self.add_rect(metals[i], p - vector(dx, dy), 2 * dx, 2 * dy)
                shape = kdb.Region(box(x, y, dx, dy))
                routed[i] += shape
                own[name][i] += shape

        # Most constrained fanout first; supplies last, using the remaining
        # open upper-metal channels rather than crossing source M1 rails.
        names = sorted(terminals, key=lambda n: (-len(terminals[n]), n))
        names = [n for n in names if n not in (self.vdd_name, self.gnd_name)] + [self.vdd_name, self.gnd_name]
        planned = {}
        for name in names:
            ports = terminals[name]
            if len(ports) == 1 and name not in (self.vdd_name, self.gnd_name):
                continue
            foreign = [(all_shapes[i] + routed[i] - own[name][i]).merged() for i in range(5)]
            blocked = [raster(foreign[i].sized(round(.38 / dbu))) for i in (2, 3, 4)]
            via_blocked = [raster(foreign[i].sized(round(.38 / dbu), round(.53 / dbu), 2))
                           for i in (2, 3, 4)]
            starts = []
            for inst, pin_name, pins, shapes in ports:
                found = None
                access = []
                # M1 pins can already reach M2 through closely spaced source
                # vias. Escape from that connected M2 rather than inserting
                # an illegal third via1 between the source cuts.
                for lower in (4, 3, 2, 1, 0):
                    # Sample each rectilinear arm, not just the bounding
                    # box of an L/T-shaped output conductor.
                    pieces = [part for shape in shapes[lower].each()
                              for part in shape.decompose_trapezoids()]
                    for polygon in pieces:
                        bounds = polygon.bbox()
                        cx, cy = bounds.center().x * dbu, bounds.center().y * dbu
                        candidates = [(cx, cy)]
                        candidates += [(cx, y) for y in np.arange(bounds.bottom * dbu + .3, bounds.top * dbu - .2, .2)]
                        candidates += [(x, cy) for x in np.arange(bounds.left * dbu + .3, bounds.right * dbu - .2, .2)]
                        access += [(lower, [(x, y) for x, y in candidates if polygon.inside(point(x, y))])]
                for pin in sorted(pins, key=lambda p: -metals.index(p.layer)):
                    candidates = [(pin.cx(), pin.cy())]
                    candidates += [(pin.cx(), y) for y in np.arange(pin.by() + .1, pin.uy() - .09, .025)]
                    candidates += [(pin.cx(), y) for y in np.arange(pin.by() + .3, pin.uy() - .2, .1)]
                    candidates += [(x, pin.cy()) for x in np.arange(pin.lx() + .3, pin.rx() - .2, .1)]
                    access.append((metals.index(pin.layer), candidates))
                    lower = metals.index(pin.layer)
                    for distance in (.6, 1.2, 1.8, 2.4):
                        for x, y, sx, sy in ((pin.cx(), pin.by() - distance, pin.cx(), pin.by()),
                                             (pin.cx(), pin.uy() + distance, pin.cx(), pin.uy()),
                                             (pin.lx() - distance, pin.cy(), pin.lx(), pin.cy()),
                                             (pin.rx() + distance, pin.cy(), pin.rx(), pin.cy())):
                            stem = kdb.Region(kdb.Path([point(x, y), point(sx, sy)], round(.26 / dbu)))
                            if (stem.sized(round(.215 / dbu)) & foreign[lower]).is_empty():
                                access.append((lower, [(x, y, sx, sy)]))
                for upper in (4, 3, 2):
                    for lower, candidates in access:
                        for candidate in candidates:
                            x, y = candidate[:2]
                            x, y = round(x / .005) * .005, round(y / .005) * .005
                            if upper < lower:
                                continue
                            horizontal_layers = []
                            safe = True
                            for i in range(lower, upper + 1):
                                dx, dy = (.31, .46) if i == 0 else (.38, .53)
                                if (foreign[i] & kdb.Region(box(x, y, dx, dy))).is_empty():
                                    continue
                                # Short horizontal output arms need the
                                # same-area pad rotated on that metal.
                                if (foreign[i] & kdb.Region(box(x, y, dy, dx))).is_empty():
                                    horizontal_layers.append(i)
                                else:
                                    safe = False
                                    break
                            if not safe:
                                continue
                            if any(not (cuts[i] & kdb.Region(box(x, y, .32, .32))).is_empty()
                                   for i in range(lower, upper)):
                                continue
                            grid = [(gx, gy)
                                    for gx in (round(x / pitch), int(x / pitch), int(x / pitch) + 1)
                                    for gy in (round(y / pitch), int(y / pitch), int(y / pitch) + 1)]
                            landing = None
                            for gx, gy in grid:
                                if blocked[upper - 2][gy, gx]:
                                    continue
                                escape = kdb.Region(kdb.Path(
                                    [point(x, y), point(gx * pitch, y), point(gx * pitch, gy * pitch)],
                                    round(.26 / dbu), round(.13 / dbu), round(.13 / dbu)))
                                if (escape.sized(round(.25 / dbu)) & foreign[upper]).is_empty():
                                    landing = gx, gy
                                    break
                            if landing is None:
                                continue
                            gx, gy = landing
                            found = (x, y, lower, upper, gx, gy, candidate[2:], horizontal_layers)
                            break
                        if found:
                            break
                    if found:
                        break
                if found is None:
                    raise ValueError(f"No safe via access for {inst.name}/{pin_name} ({name})")
                x, y, lower, upper, gx, gy, source, horizontal_layers = found
                if source:
                    add_wire(lower, [source, (x, y)], name)
                add_via(x, y, lower, upper, name, horizontal_layers)
                add_wire(upper, [(x, y), (gx * pitch, y), (gx * pitch, gy * pitch)], name)
                # Every metal in this existing stack is already connected.
                # Route into any of them; asking A* to add a second via at
                # the rounded grid point would conflict with the source cut.
                starts.append([(z - 2, gy, gx) for z in range(max(2, lower), upper + 1)])
            planned[name] = starts
        for name, starts in planned.items():
            foreign = [(all_shapes[i] + routed[i] - own[name][i]).merged() for i in range(5)]
            blocked = [raster(foreign[i].sized(round(.38 / dbu))) for i in (2, 3, 4)]
            via_blocked = [raster(foreign[i].sized(round(.38 / dbu), round(.53 / dbu), 2))
                           for i in (2, 3, 4)]
            cut_blocked = [raster(cuts[i].sized(round(.32 / dbu))) for i in (2, 3)]
            target = set(starts[0])
            for access in starts[1:]:
                if target.intersection(access):
                    continue
                goal = list(target)
                # Multi-terminal tree: A* to the existing tree's bounding box.
                xmin, xmax = min(p[2] for p in goal), max(p[2] for p in goal)
                ymin, ymax = min(p[1] for p in goal), max(p[1] for p in goal)

                def heuristic(node):
                    _, y, x = node
                    return max(xmin - x, 0, x - xmax) + max(ymin - y, 0, y - ymax)

                cost = {node: 0 for node in access if not blocked[node[0]][node[1], node[2]]}
                queue = [(heuristic(node), 0, node) for node in cost]
                heapq.heapify(queue)
                parent = {}
                end = None
                while queue:
                    _, distance, node = heapq.heappop(queue)
                    if distance != cost[node]:
                        continue
                    if node in target:
                        end = node
                        break
                    z, y, x = node
                    neighbors = [(z, y, x - 1), (z, y, x + 1), (z, y - 1, x), (z, y + 1, x)]
                    neighbors += [(z - 1, y, x), (z + 1, y, x)]
                    for nxt in neighbors:
                        zz, yy, xx = nxt
                        if not (0 <= zz < 3 and 3 <= xx < nx - 3 and 3 <= yy < ny - 3):
                            continue
                        if blocked[zz][yy, xx]:
                            continue
                        change = zz != z
                        if change and (via_blocked[z][y, x] or via_blocked[zz][y, x]):
                            continue
                        if change and cut_blocked[min(z, zz)][y, x]:
                            continue
                        step = 12 if change else 1
                        new_cost = distance + step
                        if new_cost >= cost.get(nxt, float("inf")):
                            continue
                        cost[nxt], parent[nxt] = new_cost, node
                        heapq.heappush(queue, (new_cost + heuristic(nxt), new_cost, nxt))
                if end is None:
                    raise ValueError(f"No macro route for {name}: {access} to {starts[0]}")
                path = [end]
                while path[-1] in parent:
                    path.append(parent[path[-1]])
                target.update(path)
                target.update(access)
                segment = []
                z = path[0][0]
                for zz, y, x in path:
                    coord = (round(x * pitch, 3), round(y * pitch, 3))
                    if zz != z:
                        add_wire(z + 2, segment, name)
                        add_via(*coord, min(z, zz) + 2, max(z, zz) + 2, name)
                        segment, z = [coord], zz
                    else:
                        segment.append(coord)
                add_wire(z + 2, segment, name)
                cut_blocked = [raster(cuts[i].sized(round(.32 / dbu))) for i in (2, 3)]
            # Close sub-rule notches against pre-existing metal of this same
            # net.  This is additive only: no foundry shape is removed.
            for i in range(5):
                original = own[name][i].merged()
                # Leave legal 0.21 um source gaps intact: closing them can
                # turn a narrow source rail into a wide-rule conductor.
                radius = round(.105 / dbu) - 1
                fill = original.sized(radius, 3).sized(-radius, 3) - original
                for polygon in fill.each_merged():
                    for rect in polygon.decompose_trapezoids():
                        bounds = rect.bbox()
                        self.add_rect(metals[i], (bounds.left * dbu, bounds.bottom * dbu),
                                      bounds.width() * dbu, bounds.height() * dbu)
                routed[i] += fill
                own[name][i] += fill
