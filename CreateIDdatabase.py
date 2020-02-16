import time
from imdb import IMDb
from utils import timeSince, is_male_story
import xlsxwriter
import xlrd
from threading import Lock, Thread
from imdb import IMDbDataAccessError

# get an excl file with ids list
# return an excl file of only movie types in the format:
# 0 id 1 title 2 year 3 genre 4 plot


ia = IMDb(accessSystem='http', reraiseExceptions=True,  timeout=20)

row = 0
lock = Lock()
errors = []

start = time.time()
i = 1


# return "m" or "f" tag for plot
def get_plot(movie):
    # every movie has 3 keys: synopsis, plot_outline and plot
    # synopsis is the longest and most detailed
    # in case it's missing check for the others
    plot = movie.get('synopsis')
    if plot is None:
        plot = movie.get('plot outline')
        if plot is None:
            plot = movie.get('plot')
            if plot is None:
                print(movie.getID())
                print("no plot")
                return None
        else:
            # in case of using 'plot outline' matching it to the form of the other keys
            plot = [plot]
    plot = plot[0]
    if is_male_story(plot):
        return "m"
    else:
       return "f"


def write_data(data, num_of_movies, sheet):
    global row
    global errors
    lock.acquire()
    myrow = row
    row += 1
    lock.release()

    while myrow < num_of_movies:
        if myrow % 500 == 0:
            print('%d (%s) ' % (myrow, timeSince(start)))
        myrow += 1

        # read the current id
        movie_id = data.cell_value(myrow, 0)
        movie_id = movie_id[2:]  # remove 'tt' prefix

        try:
            movie = ia.get_movie(movie_id)
        except IMDbDataAccessError:
            print("err", movie_id, myrow)
            #add the row to failed req list
            lock.acquire()
            errors.append(myrow)
            lock.release()
            continue

        movie_flag = True
        # the row will remain empty and would be deleted later
        if not movie.get('kind') == "movie":
            # print("not movie")
            movie_flag = False

        title = movie.get('title')
        year = movie.get('year')
        genre_list = movie.get("genres")
        genre_str = ', '.join(genre_list)
        plot = get_plot(movie)

        lock.acquire()

        if movie_flag:
            sheet.write(myrow, 0, movie_id)
            sheet.write(myrow, 1, title)
            sheet.write(myrow, 2, year)
            sheet.write(myrow,3,genre_str)
            sheet.write(myrow, 4, plot)

        if errors: #in case row failed try again
            myrow = errors.pop()
        else:
            myrow = row
            row += 1
        lock.release()


def init_work(path, num_of_movies):
    threads = []

    #create the new file
    workbook = xlsxwriter.Workbook('MainDatabase.xlsx')
    sheet = workbook.add_worksheet()

    #open the ids list
    wb = xlrd.open_workbook(path)
    data = wb.sheet_by_index(0)

    print(timeSince(start))

    threadnum = 50
    for i in range(threadnum):
        x = Thread(target=write_data, args=(data, num_of_movies, sheet,))
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
init_work("/home/noa/PycharmProjects/tdh20/rawids.xlsx",10051)



