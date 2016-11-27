# PSZT Checkers

Python program that allows training AI using (1+1) evolution algorithm and then testing or displaying games played by it.

## SYNOPSIS

```sh
$ ./scenarioEvolution1.py -o ai-data # learn, then save ai data in file

$ ./compareEvolution1.py -i ai-data -n 300 # load ai data from file, then test it in 300 games

$ ./main.py -i ai-data # load ai data, then run single game with full visualisation
```



## FILES
##main.py 
runs single game with visualization
####arguments
`-i file` ai data to load


##scenarioEvolution1.py 
learning phase
####arguments
`-o file` where to save ai data
#####optional
`-i file` starting ai data

`-n number` number of iterations  to run

`-m number` number of games in iteration

`-e` experimental scoring system

`-d` mutations and ai behaviour is determined


##compareEvolution1.py 
testing phase
####arguments
`-i file` ai data to load
#####optional
`-n number` number of test games to play



## REQUIREMENTS
- pypy3
- python3
- even more python
for fancy fancy viewing of games
- GTK3
- gobject-introcpection
- cairo
- cairocffi (or pycairo as drop-in replacement)