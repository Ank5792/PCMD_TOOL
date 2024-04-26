input_file = "TCID.csv"
output_file = "TCID_modified.csv"
new_delimiter = "___"

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        print("Line:- ",line)
        outfile.write(line.replace(",", new_delimiter))
