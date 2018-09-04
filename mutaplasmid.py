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


Sounds simple enough, but the possible mutations for a simple word like 'Jonathan'
are obscence, and definatly something that should be done by a machine.


With all the options turned on This will cause an epic amount of bloat ..

.. A single word could easily produce ~50k variations.

With all options on single targeted names, teams or places tailored for the
potential target are recomended.

Other than that simple lists like names, sports teams and places with more
conservative option sets will work without too much crunching.



'''



import sys
import os
import re
from optparse import OptionParser




def mutate(word, cap, num, yrs, sym, wcs, dbg=False, rs=False):


    mutations = []

    word = str(word).strip('\n')

    nbnds = range(0, 20)
    years = range(1950, 2020)
    
    wcsl = {'e':'3', 'o':'0', 'i':'1', 't':'7', 's':'5', 'a':'4', 'S':'$'}
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
        bwl = set(list(mutations))

        for bw in bwl:
            for s in symb:
                mutations.append('{}{}'.format(bw, s))
        
    # ---

    
    # numeric

    if num or yrs:

        bwl = set(list(mutations))

        for bw in bwl:

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
        bwl = set(list(mutations))

        for bw in bwl:
            for s in symb:
                mutations.append('{}{}'.format(bw, s))

    # ---

    


    
    # character substitution


    if wcs:                                                             # char substitutions
        lc = 1
        while lc <= len(wcsl):
            
            bwl = set(list(mutations))
            
            for bw in bwl:
                for s in wcsl:
                    mutations.append(re.sub(s, wcsl[s], bw))
                    
            lc += 1   
                




    # sort to ensure unique list

    unique_mutations = set(mutations)


    # return mutations




    ##############################
    # debug

    if dbg:
        for w in unique_mutations:
            print("\t{}".format(w))
            
    if rs:
        print len(unique_mutations)

    #
    ##############################

def main():


    #
    # process command switches

    parser = OptionParser()
    parser.add_option("-i", action="store", type="string", dest="input_file", help="Input file")
    parser.add_option("-o", action="store", type="string", dest="output_file", help="Output file")
    parser.add_option("-c", action="store_true", dest="cap", help="Case modification", default=False)
    parser.add_option("-n", action="store_true", dest="num", help="Add iterative numbers", default=False)
    parser.add_option("-y", action="store_true", dest="yrs", help="Add years", default=False)
    parser.add_option("-w", action="store_true", dest="wcs", help="Character substitutions", default=False)
    parser.add_option("-a", action="store_true", dest="all", help="Select all options", default=False)
    # advanced tailoring
    #parser.add_option("--year-from", action="store", type="int", dest="year-from", help="",default=1950)
    #parser.add_option("--year-to", action="store", type="int", dest="year-to", help="",default=2020)
    #parser.add_option("--num-from", action="store", type="int", dest="num-from", help="",default=0)
    #parser.add_option("--num-to", action="store", type="int", dest="num-to", help="",default=20)

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
