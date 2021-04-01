## Hex
**T**his is kind of a serious problem, 
[clck](https://ioinformatics.org/files/ioi1997problem2.pdf).
On first thought it looks annoying and unnecessarily complicated,
but on 2nd thought .. I've learn new stuff. It's about
a game of *Hex*, originally named *Polygon* from it's creator
*Piet Hein*, if you want you can ck
[wikipedia](https://en.wikipedia.org/wiki/Hex_(board_game)),
for moar info.

There is no simple strategy for this game, for example
look at that: [boom!](http://www.mseymour.ca/hex_book/hexstrat.html).
We need a brute force here and a little bit of game theory.
There is a *minimax* algorithm originally developed from
von Neumann [clck](https://www.chessprogramming.org/Minimax),
here we need to deelop an *evaluate* function and so on.

The program that I came with turns out to be quite slow:),
but didn't want to mess up very much, jst remoo most obvious
bugs, it accepts a position from NPUT and dumps the WHITE moo.
For example for this nput:
```Python
1 2 0 2  0 - BLACK
2 1 2 2  1 - WHITE
2 2 2 2  2 - EMPTY
2 2 0 2
```
it spits the following:
```C++
[[2 0 0 0 0 2]  Here a frame has been added, and WHITE has to
 [1 1 2 0 2 1]  play at the position marked with *.
 [1 2 1 * 2 1] 
 [1 2 2 2 2 1]
 [1 2 2 0 2 1]
 [2 0 0 0 0 2]]
(2, 3) 0
```
The above position is equivalent to the following:
```bash
       _
     _/ \_
   _/b\_/ \_
 _/ \_/*\_/ \_
/w\_/w\_/ \_/ \
\_/ \_/ \_/b\_/
  \_/ \_/ \_/
    \_/ \_/
      \_/
```
