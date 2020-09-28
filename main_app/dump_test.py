import json

def jprint(dict):
  text = json.dumps(dict, sort_keys=True, indent=2)
  print(text, type(text))
  return text

def jload(str):
  obj = json.loads(str)
  print(obj, type(obj))
  return obj

mydict = {
  'user_tags': [
    'boogers', 
    'hamboogers'
    ]
}

text = jprint(mydict)
dictionary = jload(text)
print(' ')
print('THESE THE USER TAGS CONVERTED BACK TO DICT : ', dictionary['user_tags'])


def min_substring(str_lst):
    ################################################
    # HELPER FUNCTION to sort the substrings list and return the smallest substring
    def find_minimum(substring_list, initial_minimum):
        minimum_length = initial_minimum
        # To begin with, the minimum length is the length of our container_string, since
        # a substring cannot be longer than the container string
        smallest_substring = ''
        # Initialize the smallest_substring as an empty string, we will mutate its values below
        for substring in substring_list:
        # Iterate upward through the list of found substrings
            if len(substring) <= minimum_length:
            # For each substring that exists
            # If the length of that substring is less than or equal to the length
            # of the minimum length (which is initially the length of the container_string)
                smallest_substring = substring
                # Set smallest_substring equal to that substring
                minimum_length = len(substring)
                # Set the the minimum length equal to the length of our new minimum substring
        return smallest_substring
        # After checking all substrings and finding the minimum length substring, return the minimum length substring
    ##################################################
    # MAIN FUNCTION BEGINS HERE
    # STEP 1: Set up initial variables
    substrings = []
    # Create an empty list to store found substrings
    container_string = str_lst[0]
    # Our long string, called container_string is equal to the 0th element of str_list
    inside_string = str_lst[1]
    # Our inside string is equal to the 1st element of str_list
    # STEP 2: Find all substrings in container_string
    for i in range(len(container_string)):
    # Iterate by the indices of our container string
        for j in range(i + len(inside_string), len(container_string) + 1):
        # Iterate by the indices in the range of i plus our inside string length to the length of our container string plus 1
        # This is to find all substrings of our container string with a length of AT LEAST the length of our inside string
        # to get the substrings at each index of i, we will set the start of each substring at i and end the substring 
        # at the index of j, which will iterate up through the container string starting at the length of our inside string
        # To visualize this, imagine a window that stretches from the inside string length to the container string length
        # which also iterates upward through the container string after every time it stretches
            substring = container_string[i:j]
            # Store each substring in a variable by grabbing the indices of our container string at i and j
            substring_char_list = list(container_string[i:j])
            # Create a list of all possible characters that exist in our substring, so we'll be able to iterate
            # through each substring's characters
            print(substring_char_list)
            for char in inside_string:
            # Since we are still iterating upward through the container string indices and
            # by the possible windows of indices that contain our smallest substring which contains our inside string,
            # For every character that is within our inside string
                if char in substring_char_list:
                # if the character is within the list of characters at each possible substring
                    substring_char_list.remove(char)
                    # remove that character from the substring character list
                    # This is because we are going to make a check on the length
                    # of our substring, the inside_string, and the list of characters of our substring below
                    # and we want to remove the length of the inside string from the substring character list
            if len(substring_char_list) <= len(substring) - len(inside_string):
            # Now, if the length of the substring character list - which has already had the length of the inside string subtracted from it
            # is LESS THAN OR EQUAL to the length of our substring minus the length of our inside string
            # The substring exists and has no outstanding values (i.e. the loop worked - yay!)
                substrings.append(substring)
                # Add the substring to our substrings list
    return find_minimum(substrings, len(container_string))
    # Finally, return the minimum length substring from our substrings list 