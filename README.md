## What is this repository for?

This repository contains calculations for the paper _Smoothly slice knots with Alexander polynomial one and high unknotting number_.

### Detailed description of the calculations

The python-script `manolescu-marengon-knots-morse.py` generates [PD Code](http://katlas.org/wiki/Planar_Diagrams) for the family of knots _mm<sub>l</sub> defined in the paper. The script accepts a single positive integers _l_ as parameter.
Internally, it uses [Morse Code](https://cbz20.raspberryip.com/code/khtpp/docs/Input.html) and the script `morse2pd.py` to convert Morse Code to PD Code (the latter script file was originally written for [a different project](https://github.com/LLewark/theta)).
The resulting PD Codes are saved in the files `mm1.in`, ..., `mm6.in`.

These files are used as input for Szabó's [Knot Floer homology calculator](https://web.math.princeton.edu/~szabo/HFKcalc.html), which outputs the files `mm1.in.mod2`, `mm1.in.mod2.Morse`, ...,  `mm6.in.mod2`, `mm6.in.mod2.Morse`.

Finally, the python-script `create_table.py` with parameter one of the file names `mm1.in.mod2`, ..., `mm6.in.mod2` returns a LaTeX table. These tables can be found at the end of the paper.
