set upper_cla [atomselect top "resname CLA and z>0"]
set lower_cla [atomselect top "resname CLA and z<0"]

puts "Upper Chlorides: [$upper_cla num]"
puts "Lower Chlorides: [$lower_cla num]"

set upper_sod [atomselect top "resname SOD and z>0"]
set lower_sod [atomselect top "resname SOD and z<0"]

puts "Upper Sodiums: [$upper_sod num]"
puts "Lower Sodiums: [$lower_sod num]"

