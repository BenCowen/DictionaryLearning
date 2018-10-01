#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dictionary Class

@author: Benjamin Cowen, Feb 24 2018
@contact: bc1947@nyu.edu, bencowen.com/lsalsa
"""
import numpy as np
import torch
from torch.autograd import Variable
import torch.nn as nn
import torchvision


def computeMaxEigVal(Dict):
    """
    Find Maximum Eigenvalue using Power Method
    """
    if Dict.use_cuda:
        bk = Variable(torch.ones(1,Dict.n).cuda())
    else:
        bk = Variable(torch.ones(1,Dict.n))
    
    f = 1
    iters= 20
    for n in range(0,iters):
        bk = bk/f
        bk = Dict.encode(Dict.forward(bk))
        f = bk.abs().max()
    Dict.maxEig = float(bk.abs().max())

class dictionary(nn.Module):
    """
    Class which defines an mxn linear dictionary.
    """
    def __init__(self, out_size, in_size, datName, use_cuda):
        super(dictionary, self).__init__()
        if use_cuda:
            self.atoms = nn.Linear(in_size, out_size, bias = False).cuda()
        else:
            self.atoms = nn.Linear(in_size, out_size, bias = False)
        self.m = out_size
        self.n = in_size
        self.datName = datName
        self.use_cuda = use_cuda
        
# Set Dictionary Weights:
    def setWeights(self, weights):
        self.atoms.weight.data = weights

# Scale Dictionary Weights:
    def scaleWeights(self, num):
        self.atoms.weight.data *= num

#######################
## BASIC OPERATIONS
#######################
# Forward Pass (decoding)
    def forward(self,input):
        return self.atoms(input)
# Transpose Pass ([roughly] encoding)
    def encode(self,input):
        return torch.matmul(self.atoms.weight.t(), input.t()).t()
    
# Normalize each column (a.k.a. atom) for the dictionary    
    def normalizeAtoms(self):
        for a in range(0,self.n):
            atom = self.atoms.weight.data[:,a]
            aNorm = atom.norm()
            if aNorm < 1e-7:
                atom *= 0
            else:
                atom /= aNorm
            self.atoms.weight.data[:,a]=atom
            
# Find Maximum Eigenvalue using Power Method
    def getMaxEigVal(self):
        computeMaxEigVal(self)

# Return copies of the weights
    def getDecWeights(self):
        return self.atoms.weight.data.clone()

    def getEncWeights(self):
        return self.atoms.weight.data.t().clone()

#######################
## VISUALIZATION
#######################        
# Print the weight values
    def printWeightVals(self):
      print(self.getDecWeights())

    def printAtomImage(self, filename):
        imsize = int(np.sqrt(float(self.m)))
        # Normalize.
        Z = self.getDecWeights()
#        Z = Z = Z - Z.min()
#        Z = Z/(Z.abs().max())
        W = torch.Tensor(self.n, 1, imsize, imsize)
        for a in range(self.n):
            W[a][0] = Z[:,a].clone().resize_(imsize,imsize)
        # Number of atom images per row.
        nr = int(np.sqrt(float(self.n)))
        torchvision.utils.save_image(W, filename, nrow=nr,
                                     normalize=True, pad_value=255)

    
    
    
    
        
        
