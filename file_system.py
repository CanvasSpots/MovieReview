'''
    This file system is responsible for the saving and loading of the movie reivew files.
'''
field_movies = ['Title', 'Release Date', 'Genre', 'Director', 'IMDB Description', 'Rating']

import csv

def input_check(question, title=False):
    user_input = input(question).lower()
    while len(user_input) == 0:
        user_input = input(question).lower()
    if title == True:
        user_input = user_input.title()
    return user_input

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
    def add_more_movies():
        more_question = input_check("\nDo you have more to add? ")
        if "no".startswith(more_question.lower()):
            return False
        return True
    
    # This is used to add new movies to the movie save file.
    more_to_add = True
    new_genres = []
    new_years = []
    new_directors = []
    movies, movie_list_title = open_movie_dict()
        
    while more_to_add:
        tit = input_check("\nTitle: What is the Title of the movie?\n", True)
        dat = input_check("\nRelease Date: When was the movie released? Please use yyyy-mm-dd format.\n")

        # If the movie already exists, you can use this to edit the data.
        title_date = tit + " " + dat
        if title_date in movie_list_title:
            existing = input_check("We found that title in our system! Would you like to update the movies's information? ")
            if "yes".startswith(existing.lower()):
                movies, new_genres = movie_update(movies, title_date, new_genres)
                
        else:
            movie_list_title.append(title_date)
            gen = input_check("\nGenre: What genre is the movie?\n",True)
            dir = input_check("\nDirector: Who was the director?\n", True)
            des = input_check("\nIMDB Description: What is the description on IMDB?\n")
            rat = input_check("\nRating: How would you rate the movie?\n",True)

            # This part separates out relevant genres, years, and director type data for the sorting file.
            genre_fixed, new_genres = genre_check(gen, new_genres)
            if dat[:4] not in new_years:
                new_years.append(dat[:4])
            if dir not in new_directors:
                new_directors.append(dir)
            
            movies.append({'Title': tit, 'Release Date': dat, 'Genre': genre_fixed, 'Director': dir, 'IMDB Description': des, 'Rating': rat})

        more_to_add = add_more_movies()
    
    # Appends the new movies to the end of the movies data file.
    movie_file_sort(movies, movie_list_title)

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
        
        for new_director in new_directors:
            if new_director not in types['Director']:
                print(str(new_director), "director has been added to Directors.")
                types['Director'].append(new_director)
                types['Director'] = sorted(types['Director'])

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

def open_movie_dict():
    with open('movies.csv') as movie_file:
        movie_dict = csv.DictReader(movie_file, delimiter=";")
        movies = []
        movie_list_title = []
        for movie in movie_dict:
            movies.append(movie)
            movie_list_title.append(movie['Title'] + " " + movie['Release Date'])
    return movies, movie_list_title

# Since movies can be added but not necessarily sorted, I've added a new function to sort them as well. If the movie file was previously open (such as when adding), the movie and tiles can be imported to save time.
def movie_file_sort(movies=None, movie_titles = None):
    if movies == None or movie_titles == None:
        movies, movie_titles = open_movie_dict()
    
    sorted_titles = sorted(movie_titles)     
    with open('movies.csv', 'w') as movie_write:
        writer_dict = csv.DictWriter(movie_write, delimiter=";", fieldnames = field_movies)

        writer_dict.writeheader()
        for title in sorted_titles:
            for movie in movies:
                movie_title_date = movie['Title'] + " " + movie['Release Date']
                if title == movie_title_date:
                    writer_dict.writerow(movie)
                    break
    
    print('\nThe movie file movies.csv has been sorted.')

def movie_update(movies, title_date, new_genres):
    for movie in movies:
        movie_title_date = movie['Title'] + " " + movie['Release Date']
        if movie_title_date == title_date:
            possible_update_fields = ['Genre', 'Director', 'Description', 'Rating']
            update_in_progress = True

            while update_in_progress:
                update_section = input_check("\nYou can make updates to the Genre, the Director, the Description, and the Rating.\nWhat would you like to update? ",True)
                
                if update_section in possible_update_fields:
                    print(f"\nThe current {update_section} values are:")
                    print("   ", movie[update_section])
                    update = input_check("\nWhat would you like to change it to?", True)

                    if update_section == "Genre":
                       genres = movie['Genre'] + "," + update
                       update, new_genres = genre_check(genres, new_genres)
                    movie[update_section] = update
                    print(f"The {update_section} for {movie['Title']} has been updated to:")
                    print("    ", update)

                    more_to_update = input_check("\nDo you have more to update? ")
                    if "no".startswith(more_to_update.lower()):
                        update_in_progress = False
    return movies, new_genres

def genre_check(genres, new_genres):
    if "," in genres:
        genre_split = genres.split(',')
        genre_strip = []
        for genre in genre_split:
            genre_strip.append(genre.strip())
    else:
        genre_strip = genres.strip()
    genre_strip = sorted(genre_strip)

    genre_fixed = ""
    for genre in genre_strip:
        if len(genre_fixed) > 0:
            genre_fixed += ","
        genre_fixed += str(genre)
        if genre not in new_genres:
            new_genres.append(genre)

    return genre_fixed, new_genres