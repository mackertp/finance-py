# Finance py

This repository is used for documentation of Python applications in financial research. I am using a conda environment that is provided via a yaml file. To follow along, install [miniconda](https://docs.conda.io/en/latest/miniconda.html) on your machine, create an environment from the file, then activate it: 

```console
uname@os:~$ conda env create --name pyfi --file=pyfi.yml
uname@os:~$ conda activate pyfi
```

With the virtual conda environment activated, create a jupyter kernel so that you are able to run all of the notebooks:

```console
uname@os:~$ python -m ipykernel install --user --name=pyfi
uname@os:~$ jupyter-lab
```

I've compiled research from several other sources that you can see in notebooks available throughout this repository. Explore some of the research that I've worked through and feel free to borrow concepts. This repository was built out while studying Yves Hilpisch's *Python for Finance*. If you click into the 'book' folder, see links to the book and his platform.


To export dependencies from the virtual enviornment into a reusable file, simply use the following conda command:

```console
(pyfi) uname@os: conda env export > pyfi.yml
```
