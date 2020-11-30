from os import walk


CHROMA_KEY = 0x00b140

current_color = 10
color_map = {CHROMA_KEY:0} # Special values: 0-Transparent 1-BackgroundColor

f = []
for (dirpath, dirnames, filenames) in walk("./input"):
    f.extend(filenames)

for file in f:
    print(f"Converting {file}")
    with open(f"./input/{file}", "r") as in_file, open(f"./output/{file}", "w") as out_file:
        lines = [i.strip() for i in in_file.readlines() if i[:2] != "/*"]
        lines[1] = " ".join(lines[1].split(" ")[i] for i in range(3)) + '",'
        img_width = int(lines[1].split(" ")[0][1:])
        out_file.write(lines[0] + '\n')
        out_file.write(lines[1] + '\n')

        
        for line in lines[2:]:
            if(len(line[1:]) < img_width and len(line[1:]) > 3): # if len(line) < image width
                line = "".join(i for i in line if i != 'c')
                color = line.split(" ")[-1][1:-2]
                if "None" in line:
                    out_file.write(line.split(" ")[0] + "  0")
                elif color in color_map.keys():
                    out_file.write(line.split(" ")[0] + " " + str(color_map[color]) + '",\n')
                else:
                    color_map[color] = current_color
                    out_file.write(line.split(" ")[0] + " " + str(current_color) + '",\n')
                    current_color += 1
            else:
                out_file.write(line + '\n')
        out_file.write("\n")

if(current_color > 256):
    print("WARNING WARNING WARNING WARNING WARNING")
    print("Color count exceeded 256!!")

print("--- Color map ---")
n = 0
for key, val in color_map.items():
    if(val != 0):
        n += 1
        print(f"0x{key},", end="")
        if(n % 6 == 0):
            print()
print(f"\nsize: {n}")

