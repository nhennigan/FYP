
def plot_seating_chart(venue,seat_no):
    mat = []
    kingfisher_length =25
    kingfisher_breadth = 25
    bailey_allen_length = 20
    bailey_allen_breadth = 30
    engineering_length = 10
    engineering_breadth = 4
    galway_bay_length = 8
    galway_bay_breadth = 10
    leisureland_length = 5
    leisureland_breadth = 10
 
    #get venue dimensions
    if venue == "Kingfisher":
        length = kingfisher_length
        breadth = kingfisher_breadth
    elif venue == "Bailey Allen Hall":
        length = bailey_allen_length
        breadth = bailey_allen_breadth
    elif venue == "Alice Perry Engineering Building":
        length = engineering_length
        breadth = engineering_breadth
    elif venue == "Galway Bay Hotel":
        length = galway_bay_length
        breadth = galway_bay_breadth
    else:
        length = leisureland_length
        breadth = leisureland_breadth
 
    mat = []
    #create empty matrix and add empty chairs
    for i in range(length):
        rowList = []
        for j in range(breadth):
            # you need to increment through dataList here, like this:
            rowList.append('clear_chair.PNG')
        mat.append(rowList)
 
    counter=0
    x_count=-1
    #iterate over empty chairs matrix and put highlight chair in 
    for x in mat:
        x_count +=1
        y_count=-1
        for y in x:
            y_count+=1
            counter +=1
            if counter == int(seat_no):
                mat[x_count][y_count]='highlighted_chair.png'
    
    mat_t = list(zip(*mat))

    return mat_t   

