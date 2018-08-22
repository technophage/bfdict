#!/usr/bin/python
# -*- coding: utf-8 -*-

banner = '''

<fettled.py>  Simple wordlist fettling tool        
                        sin@technophage.net
                        
'''



import sys
import os
from optparse import OptionParser

    

def human_chars(word):
        for c in word:
                # 'normal' typable ascii chars
                if ((ord(c) >= 33) and (ord(c) <= 127)):
                        return True
                else:
                        return False

def main():

        mnlen_check = False
        mnlen = 0
        
        mxlen_check = False
        mxlen = 0
        
        human_check = False

        #
        # process command switches
        
        parser = OptionParser()
        parser.add_option("-i", action="store", type="string", dest="input_file", help="input file")
        parser.add_option("-o", action="store", type="string", dest="output_file", help="output file")
        parser.add_option("-m", action="store", type="int", dest="mnlen", help="define minimum word length", default=0)        
        parser.add_option("-x", action="store", type="int", dest="mxlen", help="define maximum word length", default=0)
        parser.add_option("-k", action="store_true", dest="human_check", help="filter for only keyboard typable characters", default=False)

        (options, args) = parser.parse_args()

        # if
        if options.input_file:
                if os.path.isfile(options.input_file):
                        input_file = options.input_file
                else:
                        print('{} not found!'.format(options.input_file))
                        print('Quitting!')
                        exit(0)

        else:
                print(banner)
                parser.print_help()
                print('\n')
                exit(0)

        # of
        if options.output_file:
                output_file = options.output_file
        else:
                print('No output file specified, defaulting to output.txt')
                output_file = 'output.txt'

        # mn
        if options.mnlen > 0:
                mnlen_check = True
                mnlen = options.mnlen
        else:
                mnlen_check = False

        # mx
        if options.mxlen > 0:
                if options.mxlen > mnlen:
                        mxlen_check = True
                        mxlen = options.mxlen
                else:
                        print('Maximum word length must be >= minimum length')
                        exit(0)
        else:
                mxlen_check = False
        
        # kbd chr                
        if options.human_check:
                human_check = True

        ##

                
        # 
        # display settings

        print('\n')
        print('--[ Summary ]-----')

        if mnlen_check:
                print('\tminimum length   : {}'.format(str(mnlen)))
        else:
                print('\tminimum length   : none')
                
        if mxlen_check:
                print('\tmaximum length   : {}'.format(str(mxlen)))
        else:
                print('\tmaximum length   : none')
                
        if human_check:
                print('\tcharacters       : keyboard typable')
        else:
                print('\tcharacters       : any')
        
        print('\tinput file       : {}'.format(input_file))
        print('\toutput file      : {}'.format(output_file))

        ##

        
        # GO!!
        #
        
        print('\nWorking..\n')


        try:
                outfile = open(output_file, 'w')
                
        except IOError:
                print('Problem opening {} for output'.format(output_file))
                print('Quitting.')
                exit(0)


        iw = 0
        ow = 0

        try:
                with open(input_file, 'r') as infile:
                        for word in infile:
                                iw += 1
                                
                                # -1 blue, no..yellow..
                                #  0 
                                # +1 african or european

                                bk = 0

                                # check size

                                wlen = len(word.strip())
                                
                                # mn
                                if bk >= 0:
                                        if mnlen_check:
                                                if wlen >= mnlen:
                                                        bk = 1
                                                else:
                                                        bk = -1
                                # mx
                                if bk >= 0:
                                        if mxlen_check:
                                                if wlen <= mxlen:
                                                        bk = 1
                                                else:
                                                        bk = -1
                
                                # check composition
                                if bk >= 0:
                                        if human_check:
                                                if human_chars(word):
                                                        bk = 1
                                                else:
                                                        bk = -1



                                # if we get to here with +1, it passed the tests
                                if bk == 1:
                                        outfile.write(word)
                                        ow += 1
        except IOError:
                print('Problem opening ' + input_file + ' for input')
                print('Quitting..')
                exit(0)
                

        # finished run
        # close out files

        try:
                infile.close()
        except:
                pass

        try:
                outfile.close()
        except:
                pass


        #
        # display summary info

        print('--[ Statistics ]-----')

        print('\tinput file       : {}'.format(input_file))
        print('\twords read       : {}'.format(str(iw)))
        print('\toutput file      : {}'.format(output_file))
        print('\twords output     : {}'.format(str(ow)))
        print('\n\n')        


        # bye bye


if __name__ == '__main__':
        main()


# @=X
