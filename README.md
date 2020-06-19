#  Vector Embeddings of Brain Dynamics

tl;dr: This repo provided implementation of a siamise network for brain connectivity embeddings.

## Overview

Whereas we can build time-varying functional connectivity (TVFC) graphs easily and efficiently using instantaneous wavelet coherence. And whereas we can compare TVFC graphs using a host of graph-graph metrics---from simple edge-wise overlap, to more robust methods from topological data analysis. The capacity to understand how TVFC states compare among volunteers is limited by the transductive nature of state-of-the-art manifold embedding algorithms such as tSNE and UMAP. Transductive methods tend to overweight the temporal adjacencies of graph-graph distances measured within single volunteers, and thereby ignore the large-scale graph-graph similarities measured across volunteers.

## Solution

To address this issue, this project aims to build vector embeddings of several matrices of TVFC graph-graph distances. One class of inductive and vectorized embedding that may work well is the Siamese neural network. We provide here a simple `tensorflow.keras` implementation.

## Examples



