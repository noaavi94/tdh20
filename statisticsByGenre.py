import xlsxwriter
import xlrd

def write_data(data, num_of_movies, sheet):
    myrow = 0

    while myrow < num_of_movies:

        genre = data.cell_value(myrow, 11)

        if genre == "Genre" :
            movie_id = data.cell_value(myrow, 0)
            sheet.write(myrow, 0, movie_id)
            title = data.cell_value(myrow, 1)
            sheet.write(myrow, 1, title)
            plot = data.cell_value(myrow, 4)
            sheet.write(myrow, 4, plot)
            men_rating = data.cell_value(myrow, 5)
            sheet.write(myrow, 5, men_rating)
            women_rating = data.cell_value(myrow, 6)
            sheet.write(myrow, 6, women_rating)
            men_votes = data.cell_value(myrow, 7)
            sheet.write(myrow, 7, men_votes)
            women_votes = data.cell_value(myrow, 8)
            sheet.write(myrow, 8, women_votes)
            total_votes = data.cell_value(myrow, 9)
            sheet.write(myrow, 9, total_votes)
            rating = data.cell_value(myrow, 10)
            sheet.write(myrow, 10, rating)
            director = data.cell_value(myrow, 13)
            sheet.write(myrow, 13, director)

        myrow += 1


def init_work(path, num_of_movies):

    #create the new file
    workbook = xlsxwriter.Workbook('Genre.xlsx')
    sheet = workbook.add_worksheet()

    #open the ids list
    wb = xlrd.open_workbook(path)
    data = wb.sheet_by_index(0)

    write_data(data, num_of_movies, sheet)

    workbook.close()


#init path and number of movies
init_work("/home/noa/PycharmProjects/tdh20/MovieDatabase.xlsx",8068)



