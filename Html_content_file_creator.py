start = int(input("Enter start value : "))
end = int(input("Enter end value : "))

newfile = open('html_content.py', 'w')

newfile.write("html_content_list = []\n\n")

for i in range(start, end+1) :
    newfile.write(f"from html_content_{i} import html{i}\n")

newfile.write("\n")

for i in range(start, end+1) :
    newfile.write(f"html_content_list.append(html{i})\n")
    
newfile.close()