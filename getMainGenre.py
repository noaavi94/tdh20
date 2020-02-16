import xlsxwriter
import xlrd


i = 1

def get_main_genre(num_of_movies):
    #open the movie_data file
    wb = xlrd.open_workbook("/home/noa/PycharmProjects/tdh20/MovieDatabase.xlsx")
    data = wb.sheet_by_index(0)

    workbook = xlsxwriter.Workbook('mainGenre.xlsx')
    new_sheet = workbook.add_worksheet()

    myrow = 0

    while myrow < num_of_movies:
        movie_id = data.cell_value(myrow, 0)
        gen = data.cell_value(myrow, 3)
        mg = gen.split(",")

        new_sheet.write(myrow, 0, movie_id)
        new_sheet.write(myrow, 3, mg[0])
        myrow  += 1


    workbook.close()

get_main_genre(8068)