[bfdict] - bruteforce dictonary generation tool/module

[about]

This is originally based of a bash script i wrote a while ago (~2007ish) and (for me) has
been incredibly useful. I've seen it pop up in all sorts of random places on the interwebs,
so i guess some other ppl found it useful too..

The original script can be found here;
		
	https://packetstormsecurity.com/files/58652/bfdict.sh.txt.html
		
Anyway, Ive witten this version to give a more extensible feature set than the original code, have
resume functionality and generally be more 'useful' by been importable into other scripts.


																				
[usage]


So you can run it as a standalone script;

        ./bfdict.py

        or

        python bfdict.py


If you've installed the module into your python search path, as a runnable module;

        python -m bfdict


and finally as an importable module into your own script;

        from bfdict import bfdict




[module documentation:]

        Paramiters:

                ** setting these is mandatory! **

                these must be set so we have our upper an lower limits for generation;

                .mnlen       int     minimum/starting word length
                .mxlen       int     maximum word length

                validated by:
                        mnlen >= 1
                        mxlen >= mnlen


                ** at least one of these must be set, so we have chars to work with; **

                        .uselower    flag    True/False  enables std lowercase chars
                        .useupper    flag    True/False  enables std uppercase chars
                        .usenumber   flag    True/False  enables number chars
                        .usesymbol   flag    True/False  enables keyboard symbol chars

		**
		
		alternitavley the use of these overides all the previous char set flags, and setting them to false.
		it requires you set the string of chars you want or it will error.
		
                **
                        .usecustom   flag    True/False if set assign a string of the chars to customdict
                        .customdict  str

                ** optional options **

                        .prepend     str     sets a static prepend string to the begining of generated word
                        .append      str     sets a static append string to the end of generated word


   Callable meathods:


                .interactivesetup()
					
					Interactive setup annoyingly asks you questions so you dont have to set options
					in the script.

                .next_word()
				
					Returns the next word in sequence using the options you set,
					Increments counters so on the next call it will return the word next in sequence.
					
					After the last word is produced returns null.

                .savestate(filename)

					Uses cPickle to save the in memory bfdict object to file,
					this should generally be used in consort with .loadstate()

					If no filename is passed it attempts to use '.bfdict' in the modules
					working directory.

					In order to use this automatically, in the main loop of your program,
					place a KeyboardInterrupt exception handler, which calls


					[object].savestate(filename)

						or even;

					if [object].resumesave:
						[object].savestate(filename)


                .loadstate(filename)

						Load previous bfdict instance object from file to resume from a previous run.
						
						If a filename is not passed it will attermpt to load '.bfdict' in the
						modules working directory.

						To use this call;
							
							[object].loadstate(filename)
						
						This also sets the resumesave flag to True, assuming if your resuming 
						once you might like to do it again. This can be run automagically if 
						the file exists by wrapping it in a simple file existance check;
						
							import os
							import bfdict from bfdict

							bf = bfdict()
							resume_file = '.bf_resume'

							if os.path.isfile(resume_file):
								bf.loadstate(resume_file)
						




						
							

[example code]

                ###
                # generate all unsalted des hashes for all char combo's len 1-3
		# with just lowercase chars
                #

                from passlib.hash import des_crypt
                from bfdict import bfdict

                bf = bfdict()

                bf.mnlen = 1
                bf.mxlen = 3
                bf.uselower = True

                passwd = bf.nextword()
                while passwd:
                    print(passwd, des_crypt.hash(passwd))
                    passwd = bf.nextword()


						
						
						

                ###
                # prompt operator for bfdict generation peramiters prior to
		# generating unsalted des hashes
                #

                from passlib.hash import des_crypt
                from bfdict import bfdict

                bf = bfdict()

                bf.interactivesetup()

                passwd = bf.nextword()
                while passwd:
                    print(passwd, des_crypt.hash(passwd))
                    passwd = bf.nextword()


						
						
						

                ###
                # if a resume file exists load it and continue,
		# otherwise prompt for a char set before generating sha256 hashes
                #

                import os, sys, hashlib
                from bfdict import bfdict

                def hash_sha256(word):
                    return hashlib.sha256(word.encode()).hexdigest()


                bf = bfdict()
                bf.resumesave = True

                restore_file = '.hash_sha256'

                if os.path.isfile(restore_file):
                    bf.loadstate(restore_file)

                if not bf.mnlen > 0:
                    bf.interactivesetup()


                hc = 0

                try:
                    word = bf.nextword()
                    while word:
                        print(word, hash_sha256(word))
                        hc += 1
                        word = bf.nextword()

                except KeyboardInterrupt:
				
			print('\n\n')
                        print('Caught KeyboardInterrupt; Quitting.')

                        if bf.resumesave:
                            print('\n')
                            print('Saving state')
                            bf.savestate(restore_file)
                            print('\n')

                        print('Generated {} word/hash combos'.format(str(hc)))
