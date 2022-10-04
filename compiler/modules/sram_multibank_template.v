
module {{ module_name }}  (
`ifdef USE_POWER_PINS
    {{ vdd }},
    {{ gnd }},
`endif
{% for port in rw_ports %}
    clk{{ port }},
    addr{{ port }},
    din{{ port }},
    csb{{ port }},
{% if num_wmask > 1 %}
    wmask{{ port }},
{% endif %}
    web{{ port }},
    dout{{ port }},
{% endfor %}
{% for port in r_ports %}
    clk{{ port }},
    addr{{ port }},
    csb{{ port }},
    dout{{ port }},
{% endfor %}
{% for port in w_ports %}
    clk{{ port }},
    addr{{ port }},
    din{{ port }},
    csb{{ port }},
{% if num_wmask > 1 %}
    wmask{{ port }},
{% endif %}
    web{{ port }},
{% endfor %}
  );

  parameter DATA_WIDTH = {{ data_width }};
  parameter ADDR_WIDTH= {{ addr_width }};

  parameter BANK_SEL = {{ bank_sel }};
  parameter NUM_WMASK = {{ num_wmask }};

`ifdef USE_POWER_PINS
  inout {{ vdd }};
  inout {{ gnd }};
`endif
{% for port in rw_ports %}
  input clk{{ port }};
  input [ADDR_WIDTH - 1 : 0] addr{{ port }};
  input [DATA_WIDTH - 1: 0] din{{ port }};
  input csb{{ port }};
  input web{{ port }};
{% if num_wmask > 1 %}
  input [NUM_WMASK - 1 : 0] wmask{{ port }};
{% endif %}
  output reg [DATA_WIDTH - 1 : 0] dout{{ port }};
{% endfor %}
{% for port in r_ports %}
  input clk{{ port }};
  input [ADDR_WIDTH - 1 : 0] addr{{ port }};
  input csb{{ port }};
  output reg [DATA_WIDTH - 1 : 0] dout{{ port }};
{% endfor %}
{% for port in w_ports %}
  input clk{{ port }};
  input [ADDR_WIDTH - 1 : 0] addr{{ port }};
  input [DATA_WIDTH - 1: 0] din{{ port }};
  input csb{{ port }};
  input web{{ port }};
{% if num_wmask > 1 %}
  input [NUM_WMASK - 1 : 0] wmask{{ port }};
{% endif %}
{% endfor %}

{% for port in ports %}
  reg [BANK_SEL - 1 : 0] addr{{ port }}_reg;

{% for bank in banks %}
  wire [DATA_WIDTH - 1 : 0] dout{{ port }}_bank{{ bank }};

  reg web{{ port }}_bank{{ bank }};

  reg csb{{ port }}_bank{{ bank }};

{% endfor %}
{% endfor %}

{% for bank in banks %}
  {{ bank_module_name }} bank{{ bank }} (
`ifdef USE_POWER_PINS
    .{{ vdd }}({{ vdd }}),
    .{{ gnd }}({{ gnd }}),
`endif
{% for port in rw_ports %}
    .clk{{ port }}(clk{{ port }}),
    .addr{{ port }}(addr{{ port }}[ADDR_WIDTH - BANK_SEL - 1 : 0]),
    .din{{ port }}(din{{ port }}),
    .csb{{ port }}(csb{{ port }}_bank{{ bank }}),
    .web{{ port }}(web{{ port }}_bank{{ bank }}),
{% if num_wmask > 1 %}
    .wmask{{ port }}(wmask{{ port }}),
{% endif %}
    .dout{{ port }}(dout{{ port }}_bank{{ bank }}),
{% endfor %}
{% for port in r_ports %}
    .clk{{ port }}(clk{{ port }}),
    .addr{{ port }}(addr{{ port }}[ADDR_WIDTH - BANK_SEL - 1 : 0]),
    .csb{{ port }}(csb{{ port }}_bank{{ bank }}),
    .dout{{ port }}(dout{{ port }}_bank{{ bank }}),
{% endfor %}
{% for port in w_ports %}
    .clk{{ port }}(clk{{ port }}),
    .addr{{ port }}(addr{{ port }}[ADDR_WIDTH - BANK_SEL - 1 : 0]),
    .din{{ port }}(din{{ port }}),
    .csb{{ port }}(csb{{ port }}_bank{{ bank }}),
{% if num_wmask > 1 %}
    .wmask{{ port }}(wmask{{ port }}),
{% endif %}
    .web{{ port }}(web{{ port }}_bank{{ bank }}),
{% endfor %}
  );
{% endfor %}

{% for port in ports %}
  always @(posedge clk{{ port }}) begin
    addr{{ port }}_reg <= addr{{ port }}[ADDR_WIDTH - 1 : ADDR_WIDTH - BANK_SEL];
  end
{% endfor %}

{% for port in ports %}
  always @(*) begin
    case (addr{{ port }}_reg)
{% for bank in banks %}
      {{ bank }}: begin
        dout{{ port }} = dout{{ port }}_bank{{ bank }};
      end
{% endfor %}
    endcase
  end
{% endfor %}

{% for port in rw_ports %}
  always @(*) begin
{% for bank in banks %}
    csb{{ port }}_bank{{ bank }} = 1'b1;
    web{{ port }}_bank{{ bank }} = 1'b1;
{% endfor %}
    case (addr{{ port }}[ADDR_WIDTH - 1 : ADDR_WIDTH - BANK_SEL])
{% for bank in banks %}
      {{ bank }}: begin
        web{{ port }}_bank{{ bank }} = web{{ port }};
        csb{{ port }}_bank{{ bank }} = csb{{ port }};
      end
{% endfor %}
    endcase
  end
{% endfor %}

{% for port in w_ports %}
  always @(*) begin
{% for bank in banks %}
    csb{{ port }}_bank{{ bank }} = 1'b1;
    web{{ port }}_bank{{ bank }} = 1'b1;
{% endfor %}
    case (addr{{ port }}[ADDR_WIDTH - 1 : ADDR_WIDTH - BANK_SEL])
{% for bank in banks %}
      {{ bank }}: begin
        web{{ port }}_bank{{ bank }} = web{{ port }};
        csb{{ port }}_bank{{ bank }} = csb{{ port }};
      end
{% endfor %}
    endcase
  end
{% endfor %}

{% for port in r_ports %}
  always @(*) begin
{% for bank in banks %}
    csb{{ port }}_bank{{ bank }} = 1'b1;
{% endfor %}
    case (addr{{ port }}[ADDR_WIDTH - 1 : ADDR_WIDTH - BANK_SEL])
{% for bank in banks %}
      {{ bank }}: begin
        csb{{ port }}_bank{{ bank }} = csb{{ port }};
      end
{% endfor %}
    endcase
  end
{% endfor %}
endmodule
