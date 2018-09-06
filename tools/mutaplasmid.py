#!/usr/bin/python
# -*- coding: utf-8 -*-

banner = '''

<mutaplasmid.py>                                     Simple wordlist mutation tool
                                                               sin@technophage.net


**                                                                              **
**    With all the options turned on This will cause an epic amount of bloat    **
**      A single moderatly sized word could easily produce ~50k variations.     **
**                                                                              **

'''

xinfo = '''

This is mostly designed for cracking corporate style 'you must change your
password in x days' and use X,y and z characters. From experiance ppl seem
to pick sports teams, places and names; prepended by dates and/or the obligatory
symbol.

Some ppl then get tricky and character substitute, like all 'e' with '3' :)

Then at the end of the month after finally getting to grips with the unmemorable
password, they have to change it. Making 99% of ppl add or increment a number to
the back.


Sounds simple enough, but the possible mutations for a simple word like 'Jonathan'
are obscence, and definatly something that should be scripted.

With all options on single targeted names, teams or places tailored for the
potential target are recomended.

Other than that simple lists like names, sports teams and places with a more
conservative option set will work without too much crunching.


This script if free for none commercial use only.


'''



import sys
import os
import re
from optparse import OptionParser



########################################################################
##
## script defaults; modify as required

## year from/to
yf=1950
yt=2050

## formatted number from/to
nf=0
nt=20

## character substitution table
wcsl = {'e':'3', 'o':'0', 'i':'1', 't':'7', 's':'5', 'a':'4', 'S':'$'}

## insertable symbol list
symb = ['@','!','$','.']

##
##
#########################################################################


def mutate(word, cap, num, yrs, sym, wcs, dbg=False, rs=False):


    mutations = []

    word = str(word).strip('\n')

    nbnds = range(0, 20)
    years = range(1950, 2020)


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
    parser.add_option("--script-info", action="store_true", dest="xinfo", help="Script info", default=False)
    parser.add_option("-i", action="store", type="string", dest="input_file", help="Input file")
    parser.add_option("-o", action="store", type="string", dest="output_file", help="Output file")
    parser.add_option("-c", action="store_true", dest="cap", help="Case modification", default=False)
    parser.add_option("-s", action="store_true", dest="sym", help="Add/Insert Symbols", default=False)
    parser.add_option("-n", action="store_true", dest="num", help="Add iterative formatted numbers", default=False)
    parser.add_option("-y", action="store_true", dest="yrs", help="Add years", default=False)
    parser.add_option("-w", action="store_true", dest="wcs", help="Character substitutions", default=False)
    parser.add_option("-a", action="store_true", dest="all", help="Select all mutation options ** use with care **", default=False)
    parser.add_option("--yf", action="store", type="int", dest="year_from", help="Assumes years, start year. Default={}".format(yf),default=yf)
    parser.add_option("--yt", action="store", type="int", dest="year_to", help="Assumes years, end year. Default={}".format(yt),default=yt)
    parser.add_option("--nf", action="store", type="int", dest="num_from", help="Assumes numbers, start number. Default={}".format(nf),default=nf)
    parser.add_option("--nt", action="store", type="int", dest="num_to", help="Assumes numbers, end number. Default={}".format(nt),default=nt)

    (options, args) = parser.parse_args()

    if options.xinfo:
        
        print(banner)
        print(xinfo)
        parser.print_help()

        print('\n')

    elif options.input_file:

        try:

            ##
            ## mutation options

            if options.all:
                options.cap = True
                options.sym = True
                options.yrs = True
                options.wcs = True

            if options.cap or options.sym or options.yrs or options.wcs:
                pass
            else:
                print('No options supplied, Quitting.')
                exit()


            ##
            ## i/o files
                
            if os.path.isfile(options.input_file):
                try:
                    inf = open(options.input_file, 'r')

                except IOError:
                    print('Error opening {}, Quitting.'.format(options.input_file))
                    exit()

                    
            else:
                print('Cannot find input file \'{}\', Quitting.'.format(options.input_file))
                exit()

            if options.output_file:
                try:
                    ouf = open(options.output_file, 'w')

                except IOError:
                    print('Error opening output file {}, Quitting.')
                    exit()

            else:
                print('No output file specified, Quitting.')
                exit()

                    
                ## if we got here we must have enough to work with
                ##
                
                pass
            
    
        except:
                print('Unexpected error occoured. Quitting.')
                exit()


    else:
            print(banner)
            parser.print_help()
            
            print('\n')
            

if __name__ == '__main__':
    main()

# @=X
