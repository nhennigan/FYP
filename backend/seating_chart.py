import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

kingfisher_length =3
kingfisher_breadth = 4
bailey_allen_length = 20
bailet_allen_breadth = 30

def plot_seating(venue,seat_no):

#need to put in more venues and check how I have them in the database
    if venue == "Kingfisher":
        length = kingfisher_length
        breadth = kingfisher_breadth
    else:
        length = bailey_allen_length
        breadth = bailet_allen_breadth

    data = np.ones((length,breadth), dtype=int)
    my_cmap = mcolors.ListedColormap(['r', 'b'])
    my_cmap.set_bad(color='w', alpha=0)
    
    counter=0
    x_count=-1
    for x in data:
        x_count +=1
        y_count=-1
        for y in x:
            y_count+=1
            counter +=1
            if counter == seat_no:
                data[x_count][y_count]=2

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
   
    for x in range(breadth + 1):
        ax.axhline(x, lw=2, color='k', zorder=5)
    for y in range(length+1):
        ax.axvline(y, lw=2, color='k', zorder=5)
    ax.imshow(data.T,cmap=my_cmap,extent=[0, length, 0, breadth])

    frame1 = plt.gca()
    frame1.axes.xaxis.set_ticklabels([])
    frame1.axes.yaxis.set_ticklabels([])
    frame1.set_title("Front of exam hall",fontsize=20)
    plt.show()

#if __name__ == "__main__":
#    plot_seating("Bil",7)
