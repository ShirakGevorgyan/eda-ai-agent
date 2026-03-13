# Load the design
read_verilog counter.v

# Link the design with library cells
link

# Run synthesis
compile_ultra

# Write the output netlist
write -format verilog -hierarchy -output counter_netlist.v