import sys

elementalized_phrases = []
min_estimated_score = 100000000000000
# In the elementalize() recursion tree, we will prune branches whose estimated length
# is this value greater than the shortest estimated branch we have seen so far.
# This is a heuristic to prevent exponential blowup of the parse tree.
PRUNING_DISTANCE = 10

def elementalize(symbols, prefix_list, remaining_phrase):
  global min_estimated_score
  if len(remaining_phrase) == 0:
    elementalized_phrases.append(prefix_list)
    return
  if len(remaining_phrase) == 1:
    elementalized_phrases.append(prefix_list + [remaining_phrase])
    return
  estimated_score = len(prefix_list) + len(remaining_phrase) - 1
  if estimated_score < min_estimated_score:
    min_estimated_score = estimated_score
  elif estimated_score > min_estimated_score + PRUNING_DISTANCE:
    return
  if remaining_phrase[:2] in symbols:
    elementalize(symbols, prefix_list + [remaining_phrase[:2]], remaining_phrase[2:])
  elementalize(symbols, prefix_list + [remaining_phrase[:1]], remaining_phrase[1:])

def capitalized(phrase):
  return [s.title() for s in phrase] 

def main():
  if len(sys.argv) < 3:
    print "Usage:", sys.argv[0], "<input file> <phrase>"
    sys.exit(1)

  infile = sys.argv[1]
  elements = [line.strip() for line in open(infile, 'r')]
  symbols = [w.split()[1].lower() for w in elements]

  phrase = ''.join([w.lower() for w in sys.argv[2:]])

  elementalize(symbols, [], phrase)
  elementalized_phrases.sort(key=lambda l: len(l))
  # Scoring: The score of a generated symbol list is the sum of
  # the length of the list, and number of non-chemical elements.
  # The optimal generated list has shortest length and fewest non-chemical elements,
  # and therefore has the lowest possible score.
  min_score = 2*len(phrase)
  min_phrases = []
  for phrase in elementalized_phrases:
    phrase_length = len(phrase)
    num_non_elements = len(filter(lambda s: s not in symbols, phrase))
    # print capitalized(phrase), \
    #     "length:", phrase_length, \
    #     "non-elements:", num_non_elements
    score = phrase_length + num_non_elements
    if score == min_score:
      min_phrases.append(phrase)
    elif score < min_score:
      min_phrases = [phrase]
      min_score = score
  print "Optimal phrase(s):"
  for phrase in min_phrases:
    phrase_length = len(phrase)
    num_non_elements = len(filter(lambda s: s not in symbols, phrase))
    print capitalized(phrase), \
          "length:", phrase_length, \
          "non-elements:", num_non_elements
    score = phrase_length + num_non_elements

if __name__ == '__main__':
  main()
