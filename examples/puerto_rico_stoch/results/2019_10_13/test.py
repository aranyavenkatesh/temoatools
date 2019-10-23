

db_shift = {"A_0": "A_2", "A_1": "A_3", "B_0": "B_2", "B_1": "B_3", "C_0": "C_2", "C_1": "C_3", "D_0": "D_2",
                "D_1": "D_3"}

filenames = ["costs_yearly"]

for filename in filenames:


    # Read-in existing results
    filein = filename + ".csv"
    f = open(filein, 'r')
    filedata = f.read()
    f.close()

    # Make a replacement on a copy of filedata, to preserve original results
    newdata = filedata
    # Remove first line of newdata, so that when combined we do not have the headings twice
    ind = newdata.find("\n") + 2
    newdata = newdata[ind:]
    # Add a row number for the first line
    newdata = "0" + newdata

    # Replace db names with db_shift
    for key in db_shift.keys():
        newdata = newdata.replace(key,db_shift[key])

    # Combine data
    combdata = filedata + newdata

    # Write out updated results
    fileout = filename + "_exp.csv"
    f = open(fileout,'w')
    f.write(combdata)
    f.close()