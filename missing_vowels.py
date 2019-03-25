import difflib
import sys
import re
import random

# Minimum number of letters per word in generated questions.
# Used to avoid splitting words too finely.
MIN_WORD_LENGTH = 3

# Insert at most |num_spaces| spaces at random positions into |word|.
# Ensure that there are no leading, trailing, or consecutive spaces.
def insert_spaces(word, num_spaces):
  if num_spaces <= 0:
    return word
  word = word.strip()
  pos = random.randint(1, max(1, len(word)-2))
  word_with_added_space = re.sub('  ', ' ', word[:pos] + ' ' + word[pos:])
  return insert_spaces(word_with_added_space, num_spaces - 1)

# Group consecutive letters, such that every word formed is at least
# |min_word_length| letters long.
def collate(word_list, min_word_length):
  output_list = []
  i = 0
  while i < len(word_list):
    this_word = word_list[i]
    list_has_more_words = i < (len(word_list) - 1)
    next_word = word_list[i+1] if list_has_more_words else None

    if len(this_word) < min_word_length:
      collated_word = this_word
      i += 1  # Count this_word.
      while i < len(word_list)-1 and len(collated_word) < min_word_length:
        next_word = word_list[i]
        collated_word += next_word
        i += 1  # Count next_word.
      if len(collated_word) < min_word_length and len(output_list) > 0:
        # No more words left, and the current word is shorter than we want,
        # so join it with the previous word in the list.
        output_list.append(output_list.pop() + collated_word)
      else:
        # Either the collated word is now long enough, or there are no more
        # words to join it with, either next or previous, so just return
        # the collated word.
        output_list.append(collated_word)
    elif list_has_more_words and len(next_word) < min_word_length:
      if i == len(word_list) - 2:
        # The next word is the last word.
        # Join next word with current word, since there are no
        # words after it that it can be prefixed to.
        output_list.append(this_word + next_word)
        i += 2  # Count this_word and next_word.
      else:
        # With 50% probability, join the next word with the current word.
        # This is to avoid the predictability of short words always being joined
        # with their succeeding rather than preceding words.
        should_join_with_current_word = random.choice([True, False])
        if should_join_with_current_word:
          output_list.append(this_word + next_word)
          i += 2  # Count this_word and next_word.
        else:
          # In this case, insert this word as-is, and we'll join the next word
          # with *its* next word, in the next iteration.
          output_list.append(this_word)
          i += 1  # Count this_word.
    else:
      output_list.append(this_word)
      i += 1  # Count this_word.
  return output_list

def main():
  if len(sys.argv) < 2:
    print 'Usage:', sys.argv[0], '<input file>'
    sys.exit(1)
  with open(sys.argv[1], 'r') as f:
    # Ignore empty lines and lines beginning with '#' (comments).
    answers = filter(lambda s: len(s) > 0 and s[0] != '#',
                     [line.strip().upper() for line in f])
    random.shuffle(answers)
    print 'QUESTIONS:'
    for i in range(len(answers)):
      # Strip out vowels, and all non-alphanumeric characters.
      string = re.sub('[^A-Z0-9 ]+', '', re.sub('[AEIOU]', '', answers[i]))
      stripped_words = ''.join([insert_spaces(word, len(word)) \
                                  for word in string.split(' ')]) \
                          .split(' ')
      collated_words = collate(stripped_words, MIN_WORD_LENGTH)
      # Check that we aren't missing or adding any letters.
      lhs = re.sub(' ', '', ''.join(collated_words))
      rhs = re.sub(' ', '', string)
      assert lhs == rhs, \
             'diffing {} and {}, found: {}'\
             .format(lhs, rhs,\
                 ' '.join([li for li in difflib.ndiff(lhs, rhs) \
                             if li[0] != ' ']))
      print '{:2}. {}'.format(i+1, ' '.join(collated_words))
    print '\nANSWERS:'
    for i in range(len(answers)):
      print '{:2}. {}'.format(i+1, answers[i])
    
      
if __name__ == '__main__':
  main()
