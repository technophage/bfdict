#!/usr/bin/python
# -*- coding: utf-8 -*-

banner = '''

<mutaplasmid.py>                                    Simple wordlist mutation tool
                                                              sin@technophage.net


This is mostly designed for cracking corporate style 'you must change your
password in x days' and use X,y and z characters. From experiance ppl seem
to pick sports teams, places and names; prepended by dates and/or the obligatory
symbol.

Some ppl then get tricky and character substitute, like all 'e' with '3' :)

Then at the end of the month after finally getting to grips with the unmemorable
password, they have to change it. Making 99% of ppl add or increment a number to
the back.


Sound simple enough, but the possible mutations for a simple word like 'Balls'
are obscence, and definatly something that should be done by a machine.

This will cause an epic amount of bloat, and as such id stick to simple word lists
like names, sports teams and the like.



'''



import sys
import os
from optparse import OptionParser




def mutate(word, cap, num, yrs, sym, wcs):


    mutations = []

    word = str(word).strip('\n')

    nbnds = range(0, 20)
    years = range(1950, 2020)
    
    wcsl = {'e':'3', 'o':'0', 'i':'1', 't':'7', 's':'5', 'a':'4', 'S':'$', 'E':'£'}
    symb = ['@','!','$','.']





    # capitilisation

    if cap:
        mutations.append(word.lower())
        mutations.append(word.upper())
        mutations.append(word.capitalize())

    else:
        mutations.append(word)

    # ---

    
    # pre-number symbol
    
    if sym:
        prbwl = list(mutations)

        for bw in prbwl:
            for s in symb:
                mutations.append('{}{}'.format(bw, s))
        
    # ---

    
    # numeric

    if num or yrs:

        nbwl = list(mutations)

        for bw in nbwl:

            if num:
                for n in nbnds:
                    mutations.append(bw + '{}'.format(n))

                for n in nbnds:
                    mutations.append(bw + '{:02}'.format(n))



            if yrs:
                for y in years:
                    mutations.append(bw + '{}'.format(y))

    # ---

    
    # post-number symbol

    if sym:
        pobwl = list(mutations)

        for bw in pobwl:
            for s in symb:
                mutations.append('{}{}'.format(bw, s))

    # ---

    


    '''
    # character substitution


    if wcs:                                                             # char substitutions
        tw = word
        for n in range(0, (len[tw] - 1)):
            try:
                if wcsl[tw[n]]:
                    tw[n] = wcsl[tw[n]]
                    mutations.append(tw)
                    for w in mutations:
                        print(w)

            except:
                pass
    '''


    # sort to ensure unique list

    unique_mutations = sorted(set(mutations))


    # return mutations

    ##############################
    ##############################
    # debug dump
    
    for w in unique_mutations:
            print("\t{}".format(w))

    ##############################
    ##############################

def main():


    #
    # process command switches

    parser = OptionParser()
    parser.add_option("-i", action="store", type="string", dest="input_file", help="input file")
    parser.add_option("-o", action="store", type="string", dest="output_file", help="output file")
    parser.add_option("-a", action="store_true", dest="all", help="Select all modifications", default=False)
    parser.add_option("-w", action="store_true", dest="wcs", help="Character substitutions", default=False)
    parser.add_option("-n", action="store_true", dest="num", help="Add iterative numbers", default=False)
    parser.add_option("-y", action="store_true", dest="yrs", help="Add years", default=False)
    parser.add_option("-c", action="store_true", dest="cap", help="Case modification", default=False)

    (options, args) = parser.parse_args()

    if options.input_file:

        try:
            if os.path.isfile(options.input_file):

                # process args, and validate here
                # run
    
                pass
        except:
                pass
                exit()


    else:
            print(banner)
            parser.print_help()
            print('\n')
            

if __name__ == '__main__':
    main()

# @=X
