# finance_py

This repository is used for research on the applications of python for financial research. I am using a conda environment that is provided via a yaml file. To follow along, install [miniconda](https://docs.conda.io/en/latest/miniconda.html) on your machine, create an environment from my file, then activate it: 

```console
uname@os:~$ conda env create -f finance_py.yml
uname@os:~$ conda activate finance_py
```

With the virtual conda environment activated, create a jupyter kernel so that you are able to run all of the notebooks:

```console
uname@os:~$ python -m ipykernel install --user --name=finance_py
uname@os:~$ jupyter-lab
```

Explore some of the research that I've worked through and feel free to borrow concepts. The impetus for this repository is to study Yves Hilpisch's *Python for Finance*. If you click into the 'book' folder, you can see links to the book and his platform. I've compiled research from several other sources that you can see in notebooks available throughout this repository.
