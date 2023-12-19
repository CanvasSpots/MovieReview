'''
    This file system is responsible for the saving and loading of the movie reivew files.
'''

import csv

def open_categories(type):
    with open('sorting.csv') as sort_file:
        category_dict = csv.DictReader(sort_file, delimiter = ";")
        for category in category_dict:
            if category['Type'] == type:
                categories = (category['Categories'].split(','))
    return categories

def open_movies():
    with open ('movies.csv') as movie_file:
        movie_dict = csv.DictReader(movie_file, delimiter = ";")
        movies = []
        for movie in movie_dict:
            movie['Genre'] = movie['Genre'].split(',')
            movies.append(movie)
    return movies

def add_movie():
    # This is used to add new movies to the movie save file.
    more_to_add = True
    new_genres = []
    new_years = []
    movies = []
    while more_to_add:
        tit = input("\n\nTitle: What is the Title of the movie?\n")
        dat = input("\n\nRelease Date: When was the movie released?\n")
        gen = input("\n\nGenre: What genre is the movie?\n")
        dir = input("\n\nDirector: Who was the director?\n")
        des = input("\n\nIMDB Description: What is the description on IMDB?\n")
        rat = input("\n\nRating: How would you rate the movie?\n")

        # This part separates out relevant type data for the sorting file.
        if "," in gen:
            gen_split = gen.split(',')
            gen_strip = []
            for genre in gen_split:
                gen_strip.append(genre.strip())
        else:
            gen_strip = gen.strip()
        gen_strip = sorted(gen_strip)

        genre_fixed = ""
        for genre in gen_strip:
            if len(genre_fixed) > 0:
                genre_fixed += ","
            genre_fixed += str(genre)
            if genre not in new_genres:
                new_genres.append(genre)
        if dat[:4] not in new_years:
            new_years.append(dat[:4])
        
        movies.append({'Title': tit, 'Release Date': dat, 'Genre': genre_fixed, 'Director': dir, 'IMDB Description': des, 'Rating': rat})

        more = input("Do you have more to add? Type y for yes and n for no. ")
        if more == "n":
            more_to_add = False

    field_movies = ['Title', 'Release Date', 'Genre', 'Director', 'IMDB Description', 'Rating']
    
    # Appends the new movies to the end of the movies data file.
    with open('movies.csv', 'a') as movie_file:
        movie_writer = csv.DictWriter(movie_file, delimiter=";", fieldnames=field_movies)
        for movie in movies:
            movie_writer.writerow(movie)

    # Reads the existing sorting file and begins adding in more genres and release dates if they didn't exist.
    with open('sorting.csv', 'r') as sort_file:
        sort_dict = csv.DictReader(sort_file, delimiter=";")
        types = {}
        for sort_type in sort_dict:
            types[sort_type['Type']] = sort_type['Categories'].split(',')

        for new_genre in new_genres:
            if new_genre not in types['Genre']:
                print(str(new_genre), "genre has been added to Genres.")
                types['Genre'].append(new_genre)
                types['Genre'] = sorted(types['Genre'])

        for new_year in new_years:
            if new_year not in types['Release Date']:
                print(str(new_year), "year has been added to Release Dates.")
                types['Release Date'].append(new_year)
                types['Release Date'] = sorted(types['Release Date'])

        # The type dictionaries need to be reassembled correctly. This code handles that. I probably could 
        # make this section a little bit better by not splitting up the dictionary... but this seemed easier.
        type_dict = []
        field_types = ['Type', 'Categories']
        for key in types.keys():
            key_dict = {}
            for key_name in field_types:
                if key_name == 'Categories':
                    type_keys = ""
                    for category in types[key]:
                        if len(type_keys) > 0:
                            type_keys += ","
                        type_keys += str(category)
                else:
                    type_keys = key
                key_dict[key_name] =  type_keys

            type_dict.append(key_dict)
    
    # Writes the new sorting types dictionary.
    with open('sorting.csv', 'w') as sort_file:
        sort_writer = csv.DictWriter(sort_file, delimiter=";", fieldnames=field_types)
        
        sort_writer.writeheader()
        for row in type_dict:
            sort_writer.writerow(row)
