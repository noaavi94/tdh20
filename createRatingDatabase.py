import time
from imdb import IMDb
from utils import timeSince, is_male_story
import xlsxwriter
import xlrd
from threading import Lock, Thread
from imdb import IMDbDataAccessError

# get an excl file with ids list
# create an excl file of only movie types in the format:
# 1 id 2 male rating	3 female rating	4 male votes	5 female votes

ia = IMDb(accessSystem='http', reraiseExceptions=True,  timeout=20)

row = 0
lock = Lock()
errors = []

start = time.time()
i = 1


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

        try:
            movie = ia.get_movie(movie_id, 'vote details')
        except IMDbDataAccessError:
            print("err", movie_id, myrow)
            #add the row to failed req list
            lock.acquire()
            errors.append(myrow)
            lock.release()
            continue

        d = movie.get('demographics')
        if d is None:
            print("d is none", movie, movie_id)
            continue
        if 'males' not in d.keys() or 'females' not in d.keys():
            print("no males")
            continue
        curr_male_rating = d['males']['rating']
        curr_female_rating = d['females']['rating']
        amount_male = d['males']['votes']
        amount_female = d['females']['votes']

        lock.acquire()
        sheet.write(myrow, 0, movie_id)
        sheet.write(myrow, 1, curr_male_rating)
        sheet.write(myrow, 2, curr_female_rating)
        sheet.write(myrow, 3, amount_male)
        sheet.write(myrow, 4, amount_female)

        if errors: #in case row failed try again
            myrow = errors.pop()
        else:
            myrow = row
            row += 1
        lock.release()


def init_work(path, num_of_movies):
    threads = []

    #create the new file
    workbook = xlsxwriter.Workbook('RatingDatabase.xlsx')
    sheet = workbook.add_worksheet()

    #open the ids list
    wb = xlrd.open_workbook(path)
    data = wb.sheet_by_index(0)

    print(timeSince(start))

    threadnum = 30
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
init_work("/home/noa/PycharmProjects/tdh20/MainDatabase.xlsx",8325)



