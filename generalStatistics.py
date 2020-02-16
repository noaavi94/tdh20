import xlrd
import matplotlib.pyplot as plt

# remember to update "num_of_movies" and the file path

female_sum_for_female_plot = 0
male_sum_for_female_plot = 0
male_sum_for_male_plot = 0
female_sum_for_male_plot = 0
female_plot_counter = 0
male_plot_counter = 0
female_amount = 0
male_amount = 0

plots_by_year = {}
for i in range(1902, 2020):
    plots_by_year[i] = {"m":0, "f":0}


rev_by_year = {}
for i in range(1902, 2020):
    rev_by_year[i] = {"m":0, "f":0}

genres_dict = {}


wb = xlrd.open_workbook("/home/noa/PycharmProjects/tdh20/MovieDatabase.xlsx")
sheet = wb.sheet_by_index(0)

num_of_movies = 8068

for i in range(1,num_of_movies):
    #read from the file the movie's id
    movie_id = sheet.cell_value(i, 0)

    #read from the file the male and female rating
    curr_male_rating = sheet.cell_value(i, 5)
    curr_female_rating = sheet.cell_value(i, 6)


    #get the plot from the plots column
    plot = sheet.cell_value(i, 4)

    male_amount += (sheet.cell_value(i, 7))
    female_amount += sheet.cell_value(i, 8)

    year = sheet.cell_value(i, 2)

    #get the fst genre
    genre = sheet.cell_value(i, 3).split(",")[0]

    genres_dict[genre] = {}


    if plot == "m":
        male_plot_counter += 1
        female_sum_for_male_plot += curr_female_rating
        male_sum_for_male_plot += curr_male_rating

        old_m = plots_by_year[year]["m"]
        old_f = plots_by_year[year]["f"]
        plots_by_year[year] = {"m" : old_m+1, "f": old_f }

        old_m = rev_by_year[year]["m"]
        old_f = rev_by_year[year]["f"]
        rev_by_year[year] = {"m" : old_m+1, "f": old_f }

    else:
        female_plot_counter += 1
        female_sum_for_female_plot += curr_female_rating
        male_sum_for_female_plot += curr_male_rating

        old_m = plots_by_year[year]["m"]
        old_f = plots_by_year[year]["f"]
        plots_by_year[year] = {"m": old_m, "f": old_f+ 1}

        old_m = rev_by_year[year]["m"]
        old_f = rev_by_year[year]["f"]
        rev_by_year[year] = {"m" : old_m, "f": old_f + 1}


print("result: ")

print("The number of movies with female stories: ", female_plot_counter)
print("The number of movies with male stories: ", male_plot_counter)


print("The avg rating from male is: ",
      round((male_sum_for_female_plot + male_sum_for_male_plot)/num_of_movies,1))
print("The avg rating from women is: ",
      round((female_sum_for_female_plot + female_sum_for_male_plot)/num_of_movies,1))

print("The amount of reviews man wrote is: ", male_amount)
print("The amount of reviews women wrote is: ", female_amount)

print("The avg female rating when the plot was based on males is: ",
        round(female_sum_for_male_plot / male_plot_counter,1))
print("The avg male rating when the plot was based on males is: ",
        round(male_sum_for_male_plot / male_plot_counter, 1))
print("The avg female rating when the plot was based on females is: ",
        round(female_sum_for_female_plot / female_plot_counter,1))
print("The avg male rating when the plot was based on females is: ",
        round(male_sum_for_female_plot / female_plot_counter,1))

years = plots_by_year.keys()
f = [plots_by_year[i]["f"] for i in years]
m = [plots_by_year[i]["m"] for i in years]

plt.xlabel('Years')
plt.ylabel('Number of Movies')
plt.plot(years, f, label='women')
plt.plot(years, m, label='men')
#plt.show()


years = rev_by_year.keys()
f = [rev_by_year[i]["f"] for i in years]
m = [rev_by_year[i]["m"] for i in years]

plt.xlabel('Years')
plt.ylabel('Number of Reviews')
plt.plot(years, f, label='women')
plt.plot(years, m, label='men')
#plt.show()