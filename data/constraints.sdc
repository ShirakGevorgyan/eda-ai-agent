# Define the system clock
create_clock -name sys_clk -period 10.0 [get_ports clk]

# Set input and output delays
set_input_delay -max 2.0 -clock sys_clk [get_ports reset]
set_output_delay -max 1.5 -clock sys_clk [get_ports count]

# Set operating conditions
set_operating_conditions Typical