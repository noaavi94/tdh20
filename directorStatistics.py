import time
import math
from utils import timeSince, is_male_story
import xlrd
import matplotlib.pyplot as plt

# make sure to update "num_of_movies" and the file path

female_sum_for_female_dir = 0
male_sum_for_female_dir = 0
male_sum_for_male_dir = 0
female_sum_for_male_dir = 0
female_dir_counter = 0
male_dir_counter = 0
male_dir_male_plot = 0
female_dir_female_plot = 0

dir_by_year = {}
for i in range(1902, 2020):
    dir_by_year[i] = {"m":0, "f":0}


wb = xlrd.open_workbook("/home/noa/PycharmProjects/tdh20/MovieDatabase.xlsx")
sheet = wb.sheet_by_index(0)

num_of_movies = 8068

for i in range(1,num_of_movies):

    #read from the file the male and female rating
    curr_male_rating = sheet.cell_value(i, 5)
    curr_female_rating = sheet.cell_value(i, 6)

    year = sheet.cell_value(i, 2)

    #get the director's gender
    dir = sheet.cell_value(i, 13)

    #get the plot from the plots column
    plot = sheet.cell_value(i, 4)

    if dir == "m":
        male_dir_counter += 1
        female_sum_for_male_dir += curr_female_rating
        male_sum_for_male_dir += curr_male_rating
        if plot == "m":
            male_dir_male_plot += 1

        old_m = dir_by_year[year]["m"]
        old_f = dir_by_year[year]["f"]
        dir_by_year[year] = {"m": old_m + 1, "f": old_f}


    else:
        female_dir_counter += 1
        female_sum_for_female_dir += curr_female_rating
        male_sum_for_female_dir += curr_male_rating
        if plot == "f":
            female_dir_female_plot += 1

        old_m = dir_by_year[year]["m"]
        old_f = dir_by_year[year]["f"]
        dir_by_year[year] = {"m": old_m, "f": old_f + 1}


print("result: ")

print("The number of movies with female director: ", female_dir_counter)
print("The number of movies with male director: ", male_dir_counter)

print("The number of movies with female director and female plot: ", female_dir_female_plot)
print("The number of movies with male director and male plot: ", male_dir_male_plot)
print("The number of movies with female director and male plot: ", 584 - female_dir_female_plot)
print("The number of movies with male director and female plot: ", 7483 - male_dir_male_plot)


print("The avg female rating when the dir was male: ",
        round(female_sum_for_male_dir / male_dir_counter,1))
print("The avg male rating when the dir was male: ",
        round(male_sum_for_male_dir / male_dir_counter, 1))
print("The avg female rating when the dir was females is: ",
        round(female_sum_for_female_dir / female_dir_counter,1))
print("The avg male rating when the dir was females is: ",
        round(male_sum_for_female_dir / female_dir_counter,1))


for i in range(1902, 2020):
    print(i, "male", dir_by_year[i]["m"],"female: ", dir_by_year[i]["f"] )


