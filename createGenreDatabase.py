import time
from imdb import IMDb
from utils import timeSince, is_male_story
import xlsxwriter
import xlrd
from threading import Lock, Thread
from imdb import IMDbDataAccessError

# get an excl file in the format:
# 0 id
# create a new excl file with the format:
# 0 id 1 plot

ia = IMDb(accessSystem='http', reraiseExceptions=True,  timeout=20)


row = 0
lock = Lock()
errors = []

start = time.time()
i = 1

def create_plots_data(data, num_of_movies, plot_sheet):
    global row
    global errors
    lock.acquire()
    myrow = row
    row += 1
    lock.release()

    while myrow < num_of_movies:

        # read the current id and write it to the new file
        movie_id = data.cell_value(myrow, 0)

        try:
            movie = ia.get_movie(movie_id)
        except IMDbDataAccessError:
            print("err", movie_id)
            #add the row to failed req list
            lock.acquire()
            errors.append(myrow)
            lock.release()
            continue

        # every movie has 3 keys: synopsis, plot_outline and plot
        # synopsis is the longest and most detailed
        # in case it's missing check for the others
        genre_list = movie.get("genres")
        genre_str = ', '.join(genre_list)

        lock.acquire()
        plot_sheet.write(myrow, 0, movie_id)
        plot_sheet.write(myrow, 1, genre_str)

        if errors: #in case row failed try again
            myrow = errors.pop()
        else:
            myrow = row
            row += 1
        lock.release()

def init_work(path, num_of_movies):
    threads = []

    #create the new plots file
    workbook = xlsxwriter.Workbook('plots.xlsx')
    plot_sheet = workbook.add_worksheet()

    #open the movie_data file
    wb = xlrd.open_workbook(path)
    data = wb.sheet_by_index(0)

    print(timeSince(start))

    threadnum = 50
    for i in range(threadnum):
        x = Thread(target=create_plots_data, args=(data, num_of_movies, plot_sheet,))
        threads.append(x)
        x.start()

    for thread in threads:
        """
        Waits for threads to complete before moving on with the main
        script.
        """
        thread.join()

    print(timeSince(start))
    workbook.close()


#init path and number of movies
init_work("/home/noa/PycharmProjects/tdh20/movies_data0-15000.xlsx", 8068)

