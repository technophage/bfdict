#!/usr/bin/python
# -*- coding: utf-8 -*-

banner = '''

<mutagen.py>           Simple wordlist mutation tool
                                 sin@technophage.net


This is mostly designed for cracking corporate
style, 'you must change you password in x days',
and use X y and z characters.

From experiance ppl seem to pick sports teams,
places, names and dates, then mutate them for
the rules been inflicted on them.

Then at the end of the month after finally
getting to grips and confirtable with the password,
they have to change it, making 90% of ppl add or
increment a number to the back

Sound simple enough, but the possible mutations
for a word like 'Arsenal' are obcence, and definatly
something that should be done by a machine.

Use with care, this could easily increase your files
by thousands of times.

'''



import sys
import os
from optparse import OptionParser




def mutate(word, crp, num, wcs):

    mutations = []

    word = str(word)

    nbounds = range(0, 20)
    years = range(1980, 2020)
    wcsl = {'e':'3', 'o':'0', 'i':'1', 't':'7', 's':'5', 'a':'4'}       # warez type char subs
    symb = ['@','!','$','.']

    word = word.strip()                                                 # strip charage return
    mutations.append(word)                                              # add it straight back to the out put list, sans crlf

    if crp:                                                             # corp style transformations
        mutations.append(word.lower())                                  # lower
        mutations.append(word.upper())                                  # UPPER
        mutations.append(word.capitalize())                             # Capitalize


        # these are now the base words, and all subsiquent change need to be applied to all of them
        bwl = mutations


    for bw in bwl:

        if num or crp:                                                      # numeric/corp style transformations
            for n in nbounds:                                               # basic number 1,2,3
                tw = word + '{}'.format(n)
                mutations.append(tw)

            for n in nbounds:                                               # formatted numbers 01,02,03
                tw = word + '{:02}'.format(n)
                mutations.append(tw)

            for y in years:                                                 # years 1980..2020

                tw = word + '{}'.format(y)

                if crp:
                    mutations.append(tw)


        '''
        if wcs:                                                             # warez style char substitutions
            tw = word
            for n in range(0, (len[tw] - 1)):
                try:
                    if wcsl[tw[n]]:
                        #tw[n] = wcsl[tw[n]]
                        #mutations.append(tw)
                        for w in mutations:
                            print(w)

                except:
                    pass
        '''

    # finished the base word loop

    # sort to ensure unique list

    mutations = set(mutations)


    # return mutations

    # debug dump
    for w in mutations:
            print(w)

def main():


    #
    # process command switches

    parser = OptionParser()
    parser.add_option("-i", action="store", type="string", dest="input_file", help="input file")
    parser.add_option("-o", action="store", type="string", dest="output_file", help="output file")
    parser.add_option("-w", action="store_true", dest="wareify", help="Warezify", default=False)
    parser.add_option("-n", action="store_true", dest="numify", help="Add iterative numbers", default=False)
    parser.add_option("-c", action="store_true", dest="corpify", help="Corporate password policyificate", default=False)

    (options, args) = parser.parse_args()

    try:
        if os.path.isfile(options.input_file):

            try:
                ouf = open(output_file, 'w')

            except:
                print('Unable to open {} for output'.format(output_file))
                print('Quitting')
                exit(0)

            try:
                with open(input_file, 'r') as inf:
                    for line in inf:
                        mutate(line, options.wareify, options.numify, options.corpify)
            # force quit
            except KeyboardInterupt:
                print('CTRL-C Caught')
                print('Quitting..')

                try:
                    inf.close()
                    out.close()
                except:
                    pass

                exit(0)


            # file error
            except IOError:
                print('Error with {}'.format(input_file))
                print('Quitting.')

                try:
                    inf.close()
                    ouf.close()
                except:
                    pass

                exit(0)

            # other issue !!1!..?
            except:
                pass



if __name__ == '__main__':
    main()

# @=X
