start = int(input("Enter start value : "))
end = int(input("Enter end value : "))

for i in range(start, end+1) :
    newfile = open(f'html_content_{i}.py', 'w')
    newfile.write(f"html{i} = ''' ''' ")
    newfile.close()