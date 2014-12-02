import string

def read_file(filename):
    r"""Assume the file is the format
    word \t tag
    word \t tag
    [[blank line separates sentences]]

    This function reads the file and returns a list of sentences.  each
    sentence is a pair (tokens, tags), each of which is a list of strings of
    the same length.
    """
    sentences = open(filename).read().strip().split("\n\n")
    ret = []
    for sent in sentences:
        lines = sent.split("\n")
        pairs = [L.split("\t") for L in lines]
        tokens = [tok for tok,tag in pairs]
        tags = [tag for tok,tag in pairs]
        ret.append( (tokens,tags) )
    return ret

def clean_str(s):
    """Clean a word string so it doesn't contain special crfsuite characters"""
    return s.replace(":","_COLON_").replace("\\", "_BACKSLASH_")

def extract_features_for_sentence1(tokens):
    N = len(tokens)
    feats_per_position = [set() for i in range(N)]
    for t in range(N):
        w = clean_str(tokens[t])
        feats_per_position[t].add("word=%s" % w)
        feats_per_position[t].add("affix_1=%s" % w[0])
        feats_per_position[t].add("affix_1_special_char=%s" % "T" if (w[0] == "@" or w[0] == "#") else "F")
        feats_per_position[t].add("affix_2=%s" % w[0:2])
        feats_per_position[t].add("affix_3=%s" % w[0:3])
        feats_per_position[t].add("suffix_1=%s" % w[-1:])
        feats_per_position[t].add("suffix_2=%s" % w[-2:])
        feats_per_position[t].add("suffix_3=%s" % w[-3:])
        # Positional offset -1
        if (t > 0):
            w = clean_str(tokens[t-1])
            feats_per_position[t].add("affix_1_special_char_position_-1=%s" % "T" if (w[0] == "@" or w[0] == "#") else "F")
        # Positional offset +1
        if (t < N-1):
            wPost = clean_str(tokens[t+1])
            feats_per_position[t].add("affix_1_special_char_position_+1=%s" % "T" if (w[0] == "@" or w[0] == "#") else "F")
    return feats_per_position

extract_features_for_sentence = extract_features_for_sentence1

def extract_features_for_file(input_file, output_file):
    """This runs the feature extractor on input_file, and saves the output to
    output_file."""
    sents = read_file(input_file)
    with open(output_file,'w') as output_fileobj:
        for tokens,goldtags in sents:
            feats = extract_features_for_sentence(tokens)
            for t in range(len(tokens)):
                feats_tabsep = "\t".join(feats[t])
                print>>output_fileobj, "%s\t%s" % (goldtags[t], feats_tabsep)
            print>>output_fileobj, ""

extract_features_for_file("train.txt", "train.feats")
#extract_features_for_file("train_dev_concat.txt", "train.feats")
extract_features_for_file("dev.txt", "dev.feats")
