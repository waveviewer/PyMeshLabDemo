import os

folder = r"D:\VisualStudioProjects\meshprocessing\result\school"

with open("commands.ps1", "w") as f:
    for elem in os.listdir(folder):
        if elem[-3:] == "obj":
            command = "python mesh_property.py -i {} ; \n".format(os.path.join(folder, elem))
            f.write(command)
    pass
