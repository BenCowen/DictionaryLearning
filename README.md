### TO-DO
* save dictionary objects
* UPDATE: parameter search is now running on the devbox (so good dictionaries can be obtained repeatably)
* put lua version on (eh...)

# Sparse Dictionary Learning
This repository provides some basic experiments and tools for training a linear dictionary (e.g. for vectors, including vectorized image patches).
The training process yields a dictionary-- i.e. a matrix, whose rows are _dictionary atoms_-- which can be used along with a sparse code to represent a signal.
This procedure is originally described in "Emergence of simple-cell receptive field properties by learning a sparse code for natural images", by Olshausen and Field [Nature, 381:607–609, 1996](https://www.nature.com/articles/381607a0).
It is famously used in "Learning Fast Approximations of Sparse Coding" (Gregor and Lecun)
 and recently in "LSALSA: efficient sparse coding in single and multiple dictionary settings" ([Cowen, Saridena, Choromanska](https://arxiv.org/abs/1802.06875)).

We train by minimizing<a href="https://www.codecogs.com/eqnedit.php?latex=F" target="_blank"><img src="https://latex.codecogs.com/gif.latex?F" title="F" /></a>
with respect to the matrix/dictionary/decoder <a href="https://www.codecogs.com/eqnedit.php?latex=\mathbf{A}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathbf{A}" title="\mathbf{A}" /></a>
:

<a href="https://www.codecogs.com/eqnedit.php?latex=F(\mathbf{A})&space;=&space;\frac1P&space;\sum_{p=1}^P&space;\frac12||&space;\mathbf{y}(p)-\mathbf{A}\mathbf{x^*}(p)||_2^2&space;&plus;&space;\alpha||\mathbf{x^*}(p)||_1," target="_blank"><img src="https://latex.codecogs.com/gif.latex?F(\mathbf{A})&space;=&space;\frac1P&space;\sum_{p=1}^P&space;\frac12||&space;\mathbf{y}(p)-\mathbf{A}\mathbf{x^*}(p)||_2^2&space;&plus;&space;\alpha||\mathbf{x^*}(p)||_1," title="F(\mathbf{A}) = \frac1P \sum_{p=1}^P \frac12|| \mathbf{y}(p)-\mathbf{A}\mathbf{x^*}(p)||_2^2 + \alpha||\mathbf{x^*}(p)||_1," /></a>

where
<a href="https://www.codecogs.com/eqnedit.php?latex=\alpha&space;\geq&space;0" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\alpha&space;\geq&space;0" title="\alpha \geq 0" /></a>
 is a scalar parameter that balances sparsity with reconstruction error,
<a href="https://www.codecogs.com/eqnedit.php?latex=\mathbf{A}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathbf{A}" title="\mathbf{A}" /></a>
 is the dictionary,
<a href="https://www.codecogs.com/eqnedit.php?latex=\mathbf{y}(p)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathbf{y}(p)" title="\mathbf{y}(p)" /></a>
is the p-th training data sample, and
<a href="https://www.codecogs.com/eqnedit.php?latex=\mathbf{x}(p)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathbf{x}(p)" title="\mathbf{x}(p)" /></a>
is its corresponding _optimal sparse code_.

What do we mean by optimal sparse code? And why would we optimize an L1 term that does not include
<a href="https://www.codecogs.com/eqnedit.php?latex=\mathbf{A}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathbf{A}" title="\mathbf{A}" /></a>
(hence giving a zero subgradient)? The procedure is as follows.
1. Select a batch of image patches (or whatever training data): <a href="https://www.codecogs.com/eqnedit.php?latex=y(p),...,y(p&plus;B)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?y(p),...,y(p&plus;B)" title="y(p),...,y(p+B)" /></a>
2. Compute optimal codes for each <a href="https://www.codecogs.com/eqnedit.php?latex=y(p)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?y(p)" title="y(p)" /></a>.
How? Fix <a href="https://www.codecogs.com/eqnedit.php?latex=\mathbf{A}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathbf{A}" title="\mathbf{A}" /></a>.
With fixed <a href="https://www.codecogs.com/eqnedit.php?latex=\mathbf{A}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathbf{A}" title="\mathbf{A}" /></a>, <a href="https://www.codecogs.com/eqnedit.php?latex=F" target="_blank"><img src="https://latex.codecogs.com/gif.latex?F" title="F" /></a>
is convex with respect to <a href="https://www.codecogs.com/eqnedit.php?latex=x" target="_blank"><img src="https://latex.codecogs.com/gif.latex?x" title="x" /></a>!
So, we compute the argument-minimimum with respect to <a href="https://www.codecogs.com/eqnedit.php?latex=x" target="_blank"><img src="https://latex.codecogs.com/gif.latex?x" title="x" /></a>,
to obtain an optimal code. We call  <a href="https://www.codecogs.com/eqnedit.php?latex=\mathbf{x^*}(p)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathbf{x^*}(p)" title="\mathbf{x^*}(p)" /></a>
the optimal code of <a href="https://www.codecogs.com/eqnedit.php?latex=\mathbf{y}(p)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathbf{y}(p)" title="\mathbf{y}(p)" /></a>,
given the current dictionary. In this repo we compute optimal codes using an algorithm called FISTA.
3. Next, we un-fix <a href="https://www.codecogs.com/eqnedit.php?latex=\mathbf{A}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathbf{A}" title="\mathbf{A}" /></a>, compute the gradient of <a href="https://www.codecogs.com/eqnedit.php?latex=F" target="_blank"><img src="https://latex.codecogs.com/gif.latex?F" title="F" /></a>
with respect to <a href="https://www.codecogs.com/eqnedit.php?latex=A" target="_blank"><img src="https://latex.codecogs.com/gif.latex?A" title="A" /></a>
and perform backpropagation using the batch. Note: <a href="https://www.codecogs.com/eqnedit.php?latex=\mathbf{x^*}(p)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathbf{x^*}(p)" title="\mathbf{x^*}(p)" /></a>
depends on 
<a href="https://www.codecogs.com/eqnedit.php?latex=A" target="_blank"><img src="https://latex.codecogs.com/gif.latex?A" title="A" /></a>,
but it does *NOT* depend on the algorithm used to encode <a href="https://www.codecogs.com/eqnedit.php?latex=\mathbf{y}(p)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathbf{y}(p)" title="\mathbf{y}(p)" /></a>,
since it is a convex problem with a unique solution) 
4. Re-normalize the columns of <a href="https://www.codecogs.com/eqnedit.php?latex=A" target="_blank"><img src="https://latex.codecogs.com/gif.latex?A" title="A" /></a>.
5. Go back to Step 1 and pull out a fresh batch, unless <a href="https://www.codecogs.com/eqnedit.php?latex=A" target="_blank"><img src="https://latex.codecogs.com/gif.latex?A" title="A" /></a> has converged.

In summary, we do not couple the problems of sparse coding (producing codes) and training a decoder (a.k.a. dictionary). Rather, we iterate between them.

After successful optimization, the following should hold:

<a href="https://www.codecogs.com/eqnedit.php?latex=\mathbf{y}(p)&space;\approx&space;\mathbf{A}\mathbf{x}(p)," target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathbf{y}(p)&space;\approx&space;\mathbf{A}\mathbf{x}(p)," title="\mathbf{y}(p) \approx \mathbf{A}\mathbf{x}(p)," /></a>
for <a href="https://www.codecogs.com/eqnedit.php?latex=p=1,...,P" target="_blank"><img src="https://latex.codecogs.com/gif.latex?p=1,...,P" title="p=1,...,P" /></a>.

In other words, the sparse vector <a href="https://www.codecogs.com/eqnedit.php?latex=\mathbf{x}(p)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathbf{x}(p)" title="\mathbf{x}(p)" /></a>
multiplied with the (learned) dictionary <a href="https://www.codecogs.com/eqnedit.php?latex=\mathbf{A}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathbf{A}" title="\mathbf{A}" /></a>
provides an efficient approximation to the signal <a href="https://www.codecogs.com/eqnedit.php?latex=\mathbf{y}(p)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathbf{y}(p)" title="\mathbf{y}(p)" /></a>.

# Usage
This demo requires [PyTorch](https://pytorch.org/). Once downloaded, simply execute `python DEMO.py` to run the dictionary learning demo with MNIST. The results are visualized in the `results` subdirectory.

It should be easy to play around with both model and optimization parameters.
All you need to look at is the `DEMO.py` code (which builds the dataloader, defines parameters, calls training subroutines, etc.). 
For more complicated options, see `DictionaryTraining.py` (where the magic happens). MNIST, CIFAR10, ASIRRA, and Fashion-MNIST are all readily available, but if you have your own dataloader for vectors you should be able to use that too.
