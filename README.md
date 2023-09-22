# About this project 

This is the project for the Computatuional Finance Exam. The exercise's goal is to value a swaption analytically (Jamshidian Approximation) and using a MonteCarlo simulation (with three different numerairs).

Let $t_n = 2$ Years and $p = 20$ with $t_n-t_{n-1} = 1$ Years.
1. Compute the swap rate $R_p(0, t_n)$ that makes the IRS fair.
2. Compute the swaption price ATM, that is for $k = R_p(0, t_n)$
3. Compute the swaption price for $k = R_p(0, t_n) ± \Delta$ with $\Delta$ = .5%; 1%; 5%
4. Perform the MonteCarlo both in the bank account and the $P(t, T)$ numeraire with $T = t_n$ and $T = t_n+p$.

A Swaption is a contract that give the holder the right to enter into a certain interest rate swap at a certain time in the future. In our case the maturity of the Swaption is $t_n = 2$ y and so in case of exercising it, the interest rate swap would start in tn with the first payment in $t_n+1$ and last
payment done in $t_n+p$, that in our case means 22 years from now. Of course the aim is to price the Swaption today, at time $t_0$ and is considered a situation in which we are the receiving part, so we collect the fixed rate k and pay the floating LIBOR or EURIBOR. During the project we will consider the Hull-White model for the interest rates (with γ = .5 and σ = .05).


Result example: in the tabel are reported the Jamshidian results along with the MonteCarlo
results for every k and N=500000 (number of repetitions). 

|k |N| Analytic |$BankAccount ± err$ |$P(t, t_n) ± err$| $P(t, t_n+p) ± err$|
|:---:|:---:|:---:|:---:|:---:|:---:| 
|0.013577 |500000| 0.03634|0.03637 ± 0.0003| 0.0363± 0.0010 |0.03644±0.0009|
|0.018577| 500000| 0.09791 |0.09788± 0.0004| 0.0979±0.0012 |0.0979±0.0011|
|0.008577 |500000 |0.00705| 0.0070± 0.0001 |0.0070±0.0006| 0.0070±0.0006|
|0.023577| 500000 |0.17961 |0.1795± 0.0004| 0.1795±0.0013 |0.1796±0.0012|
|0.003577 |500000 |0.00050| 0.0005± 0.00002 |0.0005±0.00031 |0.0005±0.0003|
|0.063577| 500000 |0.89144 |0.8912 ± 0.0008| 0.8912±0.0017| 0.89141±0.0012|
|-0.03642| 500000 |0| 0.0 ±0.0| 0.0±0.0| 0.0±0.0|

<!-- HOW TO INSTALL -->

<h2 id="how-to-install"> How to install</h2>

Firstly the repository has to be cloned and before doing any operation you should move into the directory just created using the following commands:

```bash
 $ git clone https://github.com/nicocrucco/Computational-Finance.git
 $ cd Computational-Finance
```

The open source packages used in this project and necessary to start the simulation are in `requirements.txt` file and you can install them as following:

```bash
$ pip install -r requirements.txt
```

## Usage

To perform the simulation it has to be executed:

```bash
$ python run exam_code.py
```
 To inspect the ```usage``` function and the parameters that can be set to perform different simulations:
 
```bash
$ python run exam_code.py --help
```
Parameters that can be set: 
```bash
n : number of MC trajectories, defaults to 5000 
tn : swaption maturity date, defaults to 2
p : final IRS payment, defaults to 20
gamma : the gamma paramter of the HW model, defaults to .5
sigma : the vol paramter of the HW model, defaults to .05
```


