#!/usr/bin/env python3
# DotPhrase is a program that monitors what is typed, and when a user-generated
# "dot phrase" appears, which is a '.' followed by a user-created phrase, the
# program will delete the dot phrase and type a user-created message. For example,
# the user can set ".hi" to return "Hello, world!". When the user types ".hi", the
# program will delete the dot phrase and return "Hello, world!".

from pynput import keyboard # Used for keyboard listening
import sys # Used to exit the program from menu option
import pyinputplus as pyip # Used for input validation
import shelve # Used for saving and retrieving saved dot phrases

c = keyboard.Controller()

input_str = ""

# Whenever a user types, look for dot phrases.
def on_press(key):
    global input_str

    try:
        if key == keyboard.Key.backspace:
            pass
        # Add to the input string only after the user has typed a "." to look for a dot phrase.
        input_str += key.char
        if '.' not in input_str:
            input_str = ""
    except AttributeError:
        if key == keyboard.Key.space:
            # If space entered right after "." as in a sentence, reset the input.
            if input_str == ".":
                input_str = ""
            # Otherwise, capture the dotphrase that was entered.
            elif "." in input_str:
                type_user_phrase(input_str)
                input_str = ""
        else:
            pass

# Start the keyboard listener
def start_listener():
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

# If user releases the Esc key, stop the listener.
def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Check that dot phrase starts with a '.' and is a valid dot phrase.
def is_dot_phrase_valid(dot_phrase):
    if dot_phrase.startswith('.'):
        return True
    else:
        return False

# Check if the dot phrase is saved in the database
def does_dot_phrase_exist(dot_phrase):
    saved_dot_phrases = shelve.open('dotPhraseData')
    if dot_phrase in saved_dot_phrases.keys():
        return True
    else:
        return False
    saved_dot_phrases.close()
    
# Type the user created phrase linked to the given dot phrase.
def type_user_phrase(dot_phrase):
    if does_dot_phrase_exist(dot_phrase):
        # Delete the dot phrase
        for i in range(0, len(dot_phrase)+1):
            c.press(keyboard.Key.backspace)
            c.release(keyboard.Key.backspace)
        # Get the corresponding user phrase and type it
        saved_dot_phrases = shelve.open('dotPhraseData')
        c.type(saved_dot_phrases[dot_phrase])
        saved_dot_phrases.close()
    
# Save a dot phrase
def save_dot_phrase(dot_phrase, user_phrase):
    saved_dot_phrases = shelve.open('dotPhraseData')
    saved_dot_phrases[dot_phrase] = user_phrase
    saved_dot_phrases.close()

# Delete a dot phrase
def delete_dot_phrase(dot_phrase):
    saved_dot_phrases = shelve.open('dotPhraseData')
    saved_dot_phrases.pop(dot_phrase)
    saved_dot_phrases.close()

# Print saved dot phrases and corresponding user phrases in a table format
def print_dot_phrases():
    saved_dot_phrases = shelve.open('dotPhraseData')
    
    print("DOT PHRASE\tREPLACES WITH")
    for i in saved_dot_phrases:
        print("{}\t\t{}".format(i,saved_dot_phrases[i]))

    saved_dot_phrases.close()

# Explain the program functionality to the user.
print("""
DotPhrase is a program that monitors what is typed, and when a user-generated 
"dot phrase" appears, which is a '.' followed by a user-created phrase, the 
program will delete the dot phrase and type a user-created message. For example, 
the user can set ".hi" to return "Hello, world!". When the user types ".hi", 
the program will delete the dot phrase and return "Hello, world!".
""")

while True:
    # Get the user's menu choice.
    print()
    response = pyip.inputMenu(['Start monitoring for dot phrases', 
                               'Create a new dot phrase', 
                               'View created dot phrases',
                               'Delete a dot phrase', 
                               'Exit/quit the program'], 
                               numbered=True)

    # If user chooses to start program, start the keyboard listener.
    if response == 'Start monitoring for dot phrases':
        print("Beginning dot phrase monitoring. You can minimize this window.")
        print("Press the Esc key anytime to stop monitoring.\n")
        start_listener()

    # If user chooses to create new dot phrase, ask for and then validate dot phrase.
    if response == 'Create a new dot phrase':
        print("\nWhat is the new dot phrase?")
        new_dotphrase = input()

        # Check if dot phrase is valid
        while is_dot_phrase_valid(new_dotphrase) == False:
            print("""
That is an invalid dot phrase. Dot phrases must start with a '.' 
For example, ".hello" is a valid dot phrase that starts with a '.'

What is the new dot phrase?""")
            new_dotphrase = input()

        # If the dot phrase is valid, check if it already exists and go back to the main menu.
        if does_dot_phrase_exist(new_dotphrase) == True:
            print("\nThat dot phrase already exists.")
            print("Press enter to continue.")
            input()
        else:
            print("\nWhat would you like this dot phrase replaced with?")
            new_phrase = input()
            save_dot_phrase(new_dotphrase, new_phrase)
            print("\nYour dot phrase: " + new_dotphrase + " will be replaced with: " + new_phrase + "\n")
            print("Press enter to continue")
            input()

    # If user chooses to view created dot phrases, show the dot phrases and replacements in a table.
    if response == 'View created dot phrases':
        print()
        print_dot_phrases()
        print("\nPress enter to continue.")
        input()

    # If the user chooses to delete a dot phrases, show the dot phrases and ask which to delete, then delete it.
    if response == 'Delete a dot phrase':

        # Ask the user to enter the dot phrase they want to delete.
        print("\nEnter the dot phrase you want to delete.\n")
        print_dot_phrases()
        print()
        dot_phrase_to_delete = input()

        # Check if dot phrase exists
        while does_dot_phrase_exist(dot_phrase_to_delete) == False:
            print("\nThat dot phrase does not exist. Please enter the dot phrases you want to delete.\n")
            print_dot_phrases()
            print()
            dot_phrase_to_delete = input()

        # If user did not type back and dot phrase exists, go ahead and now delete it.
        delete_dot_phrase(dot_phrase_to_delete)
        print("\nThe dot phrase: " + dot_phrase_to_delete + " has been deleted.\n")
        print("Press enter to continue.")
        input()

    # If user chooses to quit the program, immediately stop the program
    if response == 'Exit/quit the program':
        sys.exit()
