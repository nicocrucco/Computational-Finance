# Computational Finance

This is the project for the Computatuional Finance Exam. The exercise's goal is to value a swaption analytically and using a MonteCarlo simulation (with three different numerairs).

Let $t_n = 2$ Years and $p = 20$ with $t_n-t_{n-1} = 1$ Years.
1. Compute the swap rate $R_p(0, t_n)$ that makes the IRS fair.
2. Compute the swaption price ATM, that is for $k = R_p(0, t_n)$
3. Compute the swaption price for $k = R_p(0, t_n) ± \Delta$ with $\Delta$ = .5%; 1%; 5%
4. Perform the MC both in the bank account and the $P(t, T)$ numeraire with $T = t_n$ and $T = t_n+p$.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

## Usage

The final code to execute is ESAME.py. It has to be executed with all the modules in the same folder. When ESAME.py is executed from terminal, you have to digit -help to see the usage function
```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```
