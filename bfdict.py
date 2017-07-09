#!/usr/bin/python
# -*- coding: utf-8 -*-


banner = """
 __     ___     __ __        __   
|  |--.'  _|.--|  |__|.----.|  |_ 
|  _  |   _||  _  |  ||  __||   _|
|_____|__|  |_____|__||____||____|
                             [.py]

    bruteforce dictonary generator
               sin@technophage.net

"""

import sys

try:
    from optparse import OptionParser
except:
    print('[*][bfdict] module load error')
    print('[*][bfdict] OptionParser is required for command line processing')

try:
    import cPickle as pickle
    import os
except:
    print('[*][bfdict] module load error')
    print('[*][bfdict] resume requires cPickle to be installed.')
    print('[*][bfdict] pip install cPickle')


class bfdict(object):

    '''

    Module documentation

    #---------------------------------------------------------------------------------------------------------------------------------------------
    # Option variables
    #---------------------------------------------------------------------------------------------------------------------------------------------

    ** setting these is mandatory! **

    these must be set so we have our upper an lower limits for generation;

    mnlen       int     minimum/starting word length
    mxlen       int     maximum word length

    validated by:    
        mnlen >= 1
        mxlen >= mnlen

    ** at least one of these must be set, so we have chars to work with; **

    uselower    flag    True/False  enables std lowercase chars
    useupper    flag    True/False  enables std uppercase chars
    usenumber   flag    True/False  enables number chars
    usesymbol   flag    True/False  enables keyboard symbol chars

    if this next one is set it overides all the previous char set flags, and sets them to False;
    
    usecustom   flag    True/False if set assign a string of the chars to customdict
    customdict  list/str

    ** optional options **

    prepend     str     sets a static prepend string to the begging of generated word
    append      str     sets a static append string to the end of generated word

    outputfile          this is only really useful if your writing a new front end, as its only used by dump_dict function.

    #---------------------------------------------------------------------------------------------------------------------------------------------
    # callable functions
    #---------------------------------------------------------------------------------------------------------------------------------------------

    interactivesetup    interactive setup annoyingly asks you questions so you dont have to set the options above
    
    next_word           returns the next word in sequence using the options you set, increments counters so on the next call it will return the
                        next in sequence. after the last word is produced returns null

    savestate(optional filename])
    
                        uses pickle to save the in memory bfdict object to file, this should generally br used in consort with loadstate().
                        if no filename is passed it attempts to use '.bfdict' in the current working directory.

                        in order to use this, in the main loop of your program, place a KeyboardInterrupt exception handler, which calls

                        --
                        [object].savestate([optional filename])
                        --
                        
                        or even;

                        --
                        if [object].resumesave:
                            [object].savestate([optional filename])
                        --

                        if your setting the resumesave flag.
                        
    loadstate([optional filename])
    
                        load previous bfdict instance object from file to resume from a previous run. if a filename is not passed it will attermpt
                        to load '.bfdict' from the current working directiory.

                        to use this call
                        
                        --
                        [object].loadstate([optional filname])
                        --

                        this also sets the resumesave flag to True, assuming if your resuming once you might like to do it again.

                        this can be run automagically if the file exists by wrapping it in a simple file existance check;

                        --
                        import os
                        import bfdict from bfdict

                        [object] = bfdict()
                        
                        if os.path.isfile([filename]):
                            [object].loadstate([filename])
                        --

    EOD.
    #---------------------------------------------------------------------------------------------------------------------------------------------
    
    '''

    # class vars
    #

    # predefined char sets
    lower = [ 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    upper = [ 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    number = [ '0','1','2','3','4','5','6','7','8','9']
    symbol = [ ',','.',';',':','@','#','~','[','{',']','}','!','"',"'",'$','%','^','&','*','(',')','-','_','=','+','|','?',' ']

    # user defined char sets / strings
    customdict = []
    prepend = ""
    append = ""

    # use flags
    uselower = False
    useupper = False
    usenumber = False
    usesymbol = False
    usecustom = False

    outputfile = ''

    # working vars
    ci = []
    cl = []
    mnlen = 0
    mxlen = 0
    clen = 0
    
    issetup = False

    resumeload = False
    resumesave = False


    # class functions
    #


    def savestate(self, filename='.bfdict'):
        try:
            fh = open(filename, 'wb')
            pickle.dump(self, fh)
            fh.close()
            return True
        
        except IOError:
            print('[*][bfdict.savestate] file IOError, can\'t open {} for writing'.format(str(filename)))
            return False
        
        except:
            print('[*][bfdict.savestate] error dumping restore data')
            return False
        

    def loadstate(self, filename='.bfdict'):
        if os.path.isfile(filename):
            try:
                # read the object out fo the file
                fh = open(filename, 'rb')
                bftmp = pickle.load(fh)
                fh.close()
                
                # lists
                self.ci = bftmp.ci
                self.cl = bftmp.cl

                # int content
                self.mnlen = bftmp.mnlen
                self.mxlen = bftmp.mxlen
                self.clen = bftmp.clen

                # str content
                self.prepend = bftmp.prepend
                self.append = bftmp.append
                self.outputfile = bftmp.outputfile

                # set a ready   
                self.issetup = True

                # since we loaded from a file, im going to assume we want to save on quit too
                self.resumeload = True
                self.resumesave = True

                # return
                return True
        
            except IOError:
                print('[*][bfdict.loadstate] file IOError, can\'t open {} for reading'.format(str(filename)))
                exit(0)
            except:
                print('[*][bfdict.loadstate] error loading restore data')
                exit(0)
        else:
            print('[*][bfdict.loadstate] expected resume file {} not found'.format(str(filename)))
            exit(0)


    def setdict(self):


        if self.resumeload:
            # try to load resume data
            self.loadstate()
            return 

        self.ci = [0]
        self.cl = [0]
        charSets = 0

        inchrs = []
        outchrs = []
        cnum = 0


        # verify self.mnlen and self.mxlen make sense
        if self.mnlen <= 0:
            print('[*][bfdict.setdict] Minimum word length MUST be larger than 0')
            print('[*][bfdict.setdict] self.mnlen == {}'.format(str(self.mnlen)))
            exit(0)
        if self.mnlen > self.mxlen:
            print('[*][bfdict.setdict] Minimum word length is larger than maximum word length')
            print('[*][bfdict.setdict] self.mnlen == {}, self.mxlen == {}'.format(str(self.mnlen), str(self.mxlen)))
            exit(0)

        # set current length
        self.clen = self.mnlen
    
        # init ci array
        for x in range(0, self.mxlen):
            self.ci.append(0)    
        for x in range(0, self.mnlen):
            self.ci[x] = 1

        # add characters
        if self.uselower:
            charSets += 1
            for x in self.lower:
                self.cl.append(x)
                self.cl[0] += 1
        
        if self.useupper:
            charSets += 1
            for x in self.upper:
                self.cl.append(x)
                self.cl[0] += 1
            
        if self.usenumber:
            charSets += 1
            for x in self.number:
                self.cl.append(x)
                self.cl[0] += 1
            
        if self.usesymbol:
            charSets += 1
            for x in self.symbol:
                self.cl.append(x)
                self.cl[0] += 1
            
        if self.usecustom and (self.customdict != None):
            charSets += 1
            for x in self.customdict:
                self.cl.append(str(x))
                self.cl[0] += 1

        if charSets <= 0:
            print '[*][bfdict.setdict] No characters selected'
            exit(0)
            
        # if we got this far mark as ready to go
        self.issetup = True

    #
    #

    def interactivesetup(self):

        # null any set values
        self.uselower = False
        self.useupper = False
        self.usenumber = False
        self.usesymbol = False
        self.usecustom = False
        self.mnlen = 0
        self.mxlen = 0
        self.customdict = []
    
        # word lengths
  
        # min length
        while self.mnlen <= 0:
            try:
                self.mnlen = int(raw_input('[+] enter minimum word length : '))
            except:
                self.mnlen = 0
            
            if self.mnlen <= 0:
                print '\n[*] please enter a value >= 1\n'
        
        # max length
        while self.mxlen < self.mnlen:
            try:
                self.mxlen = int(raw_input('[+] enter maximum word length : '))
            except:
                self.mxlen = 0

            if self.mxlen < self.mnlen:
                print '\n[*] please enter a value >= ' + str(self.mnlen) + '\n'


        # character sets
        
        # custom
        try:
            resp = str(raw_input('[+] use custom character set (y/n) : '))
            if resp[0].lower() == 'y':
                self.usecustom = True
        except:
            pass

        if self.usecustom:
            inputStr = ''
            while not inputStr:
                try:
                    inputStr = str(raw_input('[-] enter characters : '))
                except:
                    pass
                
            for x in range(0, len(inputStr)):
                if inputStr[x] not in self.customdict:
                    self.customdict.append(inputStr[x])
        else:
        # preset char sets
            # lowercase chars
            try:
                resp = str(raw_input('[+] use lowercase characters (y/n) : '))
                if resp[0].lower() == 'y':
                    self.uselower = True
                else:
                    self.uselower = False
            except:
                pass
        
            # uppercase chars
            try:
                resp = str(raw_input('[+] use uppercase characters (y/n) : '))
                if resp[0].lower() == 'y':
                    self.useupper = True
                else:
                    self.useupper = False
            except:
                pass
        
            # number chars
            try:
                resp = str(raw_input('[+] use number characters (y/n) : '))
                if resp[0].lower() == 'y':
                    self.usenumber = True
                else:
                    self.usenumber = False
            except:
                pass
        
            # symbol chars
            try:
                resp = str(raw_input('[+] use standard symbol characters (y/n) : '))
                if resp[0].lower() == 'y':
                    self.usesymbol = True
                else:
                    self.usesymbol = False
            except:
                pass

        # prepend
        try:
            resp = str(raw_input('[+] prepend string to word (y/n) : '))
            if resp[0].lower() == 'y':
                self.prepend = str(raw_input('[+] enter string : '))
        except:
           pass
            
        # append
        try:
            resp = str(raw_input('[+] append string to word (y/n) : '))
            if resp[0].lower() == 'y':
                self.append = str(raw_input('[+] enter string : '))
        except:
           pass

        # fileoutput
        try:
            resp = str(raw_input('[+] output to file (y/n) : '))
            if resp[0].lower() == 'y':
                self.outputfile = str(raw_input('[+] enter filename : '))
        except:
           pass

    #
    #
    
    def dumpdict(self):

        try:
            fo=False
            wc = 0

            # if a filename is set, assume were outputting to file
            if len(self.outputfile) > 0:
                
                # append on resume
                if self.resumeload:
                    mode = 'a'
                else:
                    mode = 'w'
                    
                try:
                    f = open(self.outputfile, mode)
                    fo=True
                    
                except IOError:
                    print('[*][bfdict.dumpdict] error writing to file {}'.format(self.outputfile))
                    exit(0)

            # write to file, else print to screen
            wrd = self.nextword()
            while wrd:
                if fo:
                    f.write(wrd + '\n')
                else:
                    print wrd
                wc += 1
                wrd = self.nextword()

            # close file handler
            if fo:
                f.close()
                fo = False
                
        except KeyboardInterrupt:

            # CTRL-C handler
            
            print('\n\n')
            print('[-][bfdict] Caught keyboard interrupt.')
            print('[-][bfdict] Quitting after {} words.'.format(str(wc)))
                  
            if self.resumesave:
                self.savestate()
                  
            return
                  
        except Exception as e:

            print('[*][bfdict.dumpdict] Unexpected error!')
            exit(0)
            

    #
    #

    def nextword(self):

        # if setup flag not set, run setup function
        if not self.issetup:
            self.setdict()

        # generate word
        if self.clen <= self.mxlen:
            word = ''
            for x in range(0, self.clen):
                word = self.cl[self.ci[x]] + word
                if self.prepend:
                    word = self.prepend + word
                if self.append:
                    word = word + self.append
            self.ci[0] += 1
            if self.ci[0] > self.cl[0]:
                for x in range(0, self.mxlen):
                    if self.ci[x] > self.cl[0]:
                        self.ci[x] = 1
                        self.ci[x+1] += 1
                        if (x+1) == self.clen:
                            self.clen += 1
            return word
        else:
            return

    #
    #


def main():

    custdict = ""

    bf = bfdict()
    
    parser = OptionParser()
    parser.add_option("-i", action="store_true", dest="inter", help="Interactive setup mode [Use alone]", default=False)
    parser.add_option("-m", action="store", type="int", dest="mnlen", help="Minimum word length", default=1)
    parser.add_option("-x", action="store", type="int", dest="mxlen", help="Maximum word length", default=3)
    parser.add_option("-l", action="store_true", dest="uselower", help="Use lowercase characters", default=False)
    parser.add_option("-u", action="store_true", dest="useupper", help="Use uppercase characters", default=False)
    parser.add_option("-n", action="store_true", dest="usenumber", help="Use number characters", default=False)
    parser.add_option("-s", action="store_true", dest="usesymbol", help="Use standard symbols", default=False)
    parser.add_option("-p", action="store", type="string", dest="prepend", help="String to prepend to generated word", default="")
    parser.add_option("-a", action="store", type="string", dest="append", help="String to append to generated word", default="")
    parser.add_option("-c", action="store", type="string", dest="custdict", help="Set custom character set", default='')
    parser.add_option("-f", action="store", type="string", dest="outputfile", help="Output filename [Default is to screen]", metavar="FILE", default='')
    parser.add_option("-R", action="store_true", dest="resumeload", help="Load from resume file", default=False)
    parser.add_option("-S", action="store_true", dest="resumesave", help="Save resume data on quit", default=False)
    
    (options, args) = parser.parse_args()

    custdict = options.custdict

    if options.resumeload:
        if bf.loadstate():
            bf.dumpdict()
    else:

        if options.resumesave:
            bf.resumesave = True
     
        # process options
        if options.inter:
            bf.interactivesetup()
        elif options.custdict:
            bf.uselower = False
            bf.useupper = False
            bf.usenumber = False
            bf.usesymbol = False
            bf.usecustom = True
            if options.prepend:
                bf.prepend = options.prepend
            if options.append:
                bf.append = options.append
            for x in range(0, len(custdict)):
                bf.customdict.append(custdict[n])
        else:
            bf.mnlen = options.mnlen
            bf.mxlen = options.mxlen
            bf.uselower = options.uselower
            bf.useupper = options.useupper
            bf.usenumber = options.usenumber
            bf.usesymbol = options.usesymbol
            if options.prepend:
                bf.prepend = options.prepend
            if options.append:
                bf.append = options.append
            if options.outputfile:
                bf.outputfile = options.outputfile
                
    if (len(sys.argv)>1):
        bf.dumpdict()
    else:
        print banner
        parser.print_help()

if __name__ == '__main__':
    main()

# @=X
