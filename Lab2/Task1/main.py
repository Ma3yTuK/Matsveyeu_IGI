import input_methods as im
import parse_methods as pm

def main():
    text = str()
    k = 10
    n = 4
    
    request = (
        '\n'
        '1) Change text\n'
        '2) Change k\n'
        '3) Change n\n'
        '4) Number of sentences\n'
        '5) Number of non-declarative sentences\n'
        '6) Average length of a sentence\n'
        '7) Average length of a word\n'
        '8) Top-k repeated n-grams\n'
        '9) Exit\n'
        'Choose action: '
    )

    while True:

        match im.integer_input(request, 1, 9):
            case 1:
                text = im.multiline_input("Text to parse:")
            case 2:
                k = im.integer_input('k: ', 1, 100)
            case 3:
                n = im.integer_input('n: ', 1, 100)
            case 4:
                print('Number of sentences: {0}'.format(pm.sentence_count(text)))
            case 5:
                print('Number of non-declarative sentences: {0}'.format(pm.non_declarative_sentence_count(text)))
            case 6:
                print('Average length of a sentence: {0}'.format(pm.avg_sentence_length(text)))
            case 7:
                print('Average length of a word: {0}'.format(pm.avg_word_length(text)))
            case 8:
                top_n_grams = pm.top_n_grams(text, n)[:k]
                if len(top_n_grams) < k:
                    print('Can not find enough n-grams')
                else:
                    print('Top-k repeated n-grams (n-gram : number of occurrences):')
                    for n_gram in top_n_grams:
                        print('{0} : {1}'.format(*n_gram))
            case 9:
                break

if __name__ == '__main__':
    main()
