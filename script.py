from file_system import *
from doublylinkedlist import *
from node import *

movie_tags = ['Title','Release Date', 'Genre', 'Director', 'IMDB Description', 'Rating']

class Review:
    # The review class houses each review's information in a simple-to-access way. 
    def __init__(self, in_title, in_date, in_genres, in_director, in_description, in_rating):
        self.title = in_title
        self.release_date = in_date
        self.genres = in_genres
        self.director = in_director
        self.description = in_description
        self.rating = int(in_rating)

        self.total_lists = 0
        self.similar_movies = []

    def __repr__(self):
        # Return text of a ticket stub of information for each movie review.
        ticket_size = 65

        fixed_genres = ""
        for genre in self.genres:
            if len(fixed_genres) > 0:
                fixed_genres += ", "
            fixed_genres += str(genre)
        
        rating = "CanvasSpots' Rating: "
        for i in range(5):
            if i < self.rating:
                rating += "★"
            else:
                rating += "☆"

        def finish_length(length, text, insert=" "):
            # For creating the total length of the movie ticket stub and adding a piece of paper at the end. If the insert is changed, the second sidebar will not print.
            while len(text) < length:
                text += insert
            if insert == " ":
                text += insert + "|"
            return text
        
        def length_repair(text1, text2, line_len=ticket_size):
            # I don't want to talk about it, but I will anyways. This function regulates the total length of a terminal line that will print for each movie ticket stub. I built it so that there can be two string inputs that are then concatinated. If the strings are left empty, the function automatically prints a blank line with ends.
            text1_len = len(text1)
            description = "\n| " + text1
            text_len = len(text2)
            if text_len > (line_len - text1_len):
                description += finish_length(line_len - text1_len, text2[:(line_len - text1_len)])
                for i in range((text_len - (line_len - text1_len)) // line_len + 1):
                    end = line_len * (i + 1) - text1_len
                    line = "\n| " + text2[(end):(end + line_len)]
                    if (end + line_len) > text_len:
                        line_len += 3
                    description += finish_length(line_len, line)               
            else: 
                line = text2
                description += finish_length(line_len - text1_len, line)
            return description
        
        text = "┌ᵥ" + finish_length(ticket_size + 1, "", "ᶺᵥ") + "┐"
        text += length_repair("","")
        text += length_repair("Title: ", self.title)
        text += length_repair("Release Date: ", self.release_date)
        text += length_repair("Director: ", self.director)
        text += length_repair("", rating)
        text += length_repair("","")
        text += length_repair("Description from IMDB: ", self.description)
        text += length_repair("","")
        text += length_repair(str(self.total_lists) + " // Genres: ", fixed_genres)
        text += "\n└ᵥ" + finish_length(ticket_size + 1, "", "ᶺᵥ") + "┘"
        return text
    
    def increase_list(self):
        self.total_lists += 1

print("    ┌⏑-⏑-⏑-⏑-⏑-⏑-⏑-⏑-⏑-⏑-⏑-⏑-⏑-⏑-⏑┐   ")
print("    | ┌ - - - - - - - - - - - - ┐ |   ")
print("    | | * *        *        * * | |   ")
print("    | | *    W E L C O M E    * | |   ")
print("    | |           T O           | |   ")
print("    | |        M O V I E        | |   ")
print("    | | *     R E V I E W     * | |   ")
print("    | | * *        *        * * | |   ")
print("    | └ - - - - - - - - - - - - ┘ |   ")
print("    └-----------------------------┘   ")
print("  /     ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒     \ ")
print("/     ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒     ")
print("    ⌒ ⌒ B Y ⌒ C A N V A S S P O T S   ")
print("  ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ⌒ ")

def exit():
    print("\nThank you for using Movie Reviews, the movie review searching database.")
    print("Please return soon!")

def insert_sorting_categories(type):
    # Creates a category linked list to be searched through based on the category types.
    categories = open_categories(type)
    category_list = DoublyLinkedList()
    for category in categories:
        category_list.add_to_tail(category)
    return category_list, categories

def insert_movie_reviews(type, categories):
    # Creates a linked list for each category and adds all corresponding movie review linked sublist.
    movie_reviews = open_movies()
    movie_review_list = {}
    movie_list = {}
    for category in categories:
        movie_child_list = DoublyLinkedList()
        for review in movie_reviews:
            if category in review[type]:
                # This part checks if there's an existing review already created. Reviews are classes that have been saved to a dictionary. The key to the dictionary is the movie's release date and the movie's title, both of which can be easily looked through. If not, a new review is made. The review is the added as a node to the linked list item.
                review_key = review[movie_tags[1]] + " " + review[movie_tags[0]]
                if review_key not in movie_list.keys():
                    movie_review = Review(review[movie_tags[0]], review[movie_tags[1]], review[movie_tags[2]], review[movie_tags[3]], review[movie_tags[4]], review[movie_tags[5]])
                    movie_list[review_key] = movie_review
                movie_list[review_key].increase_list()
                movie_child_list.add_to_tail(movie_list[review_key])
        movie_review_list[category] = movie_child_list

    return movie_review_list

def select_category_type(type='Genre'):
    category_type = type
    category_list, categories = insert_sorting_categories(category_type)
    movie_review_list = insert_movie_reviews(type, categories)
    return category_list, categories, movie_review_list

def input_check(question):
    user_input = input(question).lower()
    while len(user_input) == 0:
        user_input = input(question).lower()
    return user_input

category_type = 'Genre'
tips = True
cat_list, cats, movie_list = select_category_type(category_type)

sel_cat = ""
while len(sel_cat) == 0:
    # This creates the question, but only lets the user know about the other options if tips is set to True.
    search_question = "\nWhat {type} of movie are you thinking of watching??\n".format(type=category_type.lower())
    if tips:
        tips = False
        search_question += """
Type the beginning of the {type} and press enter to see if it's here. You can also enter:
    '/add' to add a movie to the review list.
    '/change' to change the category types.
    '/print' to print the category types.
    '/exit' to exit out of this program. 
""".format(type=category_type.lower())
    search_question += "\nChoose wisely: "
    user_input = input_check(search_question)

    # This first section checks if the user input is a user command before searching thru the category list.
    if user_input[0] == "/": 
        # Allows the user to add a new movie title to the review section. This bit of code was created because I was adding my own reviews and it takes a lot more time to enter them into the movies.csv and check against the sorting.csv.
        if "/add".startswith(user_input.lower()):
            print('\nAdd new movie review selected.')
            add_movie()

        # Allows the user to change the category sort type. Currently only genre and the release date work. I might add more later, like directors.
        elif "/change".startswith(user_input.lower()):
            user_input = input_check("\nChange category types selected.\nHow would you like to sort thru our movies?\nYou can say 'genre' to sort by genre, or 'release date' to sort by year the movie's were released. Say anything else to return to the previous menu.\n\n")
            possible_answers = ['genre', 'release date']
            if user_input in possible_answers:
                cat_list, cats, movie_list = select_category_type(user_input.title())
            elif user_input == "/exit":
                select_movie_category = user_input

        # Allows users to print a list of the categories available. Not really useful since the whole point is to be able to search the list (which this can do).
        elif "/print".startswith(user_input.lower()):
            print('\nPrint category types selected.')
            print(cats)

        # I added in an exit so I could program different parts out of order (which meant I needed a quick way to leave). Can still be used by the user.
        elif "/exit".startswith(user_input.lower()):
            print("\nExit program selected.")
            exit()
            sel_cat = user_input
    
    # If none of the above commands were input, the used will then begin searching the list for the category that begins with their text.
    else:
        matching = []
        cat_list_head = cat_list.get_head_node()
        while cat_list_head is not None:
            if str(cat_list_head.get_value()).startswith(user_input.title()):
                matching.append(cat_list_head.get_value())
            cat_list_head = cat_list_head.get_next_node()

        if len(matching) == 0:
            print("\nThere are no movie reviews with {type}'s starting with {input} in them.".format(input=user_input, type=category_type.lower()))
        elif len(matching) > 1:
            print("\nThe following {type}'s match your input: ".format(type=category_type.lower()))
            category_matches = ""
            for category in matching:
                if category is not matching[0]:
                    category_matches += ", "
                category_matches += category
            print("    • " + category_matches)
        else:
            sel_cat = matching[0]
            user_input = input_check("The only matching {type} is {cat}. Would you like to view movie reviews for that type? ".format(type=category_type.lower(), cat=sel_cat.lower()))
            if "yes".startswith(user_input):
                movie_list_head = movie_list[sel_cat].get_head_node()
                print("\nSelected {type} category:".format(type=category_type.lower()), sel_cat)
                while movie_list_head is not None:   
                    print(movie_list_head.get_value())
                    movie_list_head = movie_list_head.get_next_node()
            
            # This part allows for people to repeat the code without running the code again.
            user_input = input_check("Would you like to search the database again? ")
            if "yes".startswith(user_input):
                sel_cat = ""
            else:
                exit()
