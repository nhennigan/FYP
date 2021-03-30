
def plot_seating_chart(venue,seat_no):
    mat = []
#    if request.method == 'POST' and 'venue' in request.form and 'seat_no' in request.form:
#        seating_chart.plot_seating(request.form['venue'],request.form['seat_no'])
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
    for i in range(length):
        rowList = []
        for j in range(breadth):
            # you need to increment through dataList here, like this:
            rowList.append('clear_chair.PNG')
        mat.append(rowList)
 
    counter=0
    x_count=-1
    for x in mat:
        x_count +=1
        y_count=-1
        for y in x:
            y_count+=1
            counter +=1
            if counter == int(seat_no):
                mat[x_count][y_count]='highlighted_chair.png'
    
    mat_t = list(zip(*mat))

#    f_name,l_name,course = conn.get_student_data(session["username"])
#    exam_list = conn.get_exam_data(session["username"])
#    user_in = User(session["username"],f_name,l_name,course)
    return mat_t   
    #return render_template('home.html',user=user_in,exams=exam_list,m=mat_t)
#    return redirect(url_for('home_page',seating = mat_t))
#    return render_template('seat.html', m= mat_t,v= request.form['venue'])
#   return redirect(url_for(home_page))

