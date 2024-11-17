# Finance py

Python applications in financial research. 

A yaml file is used to manage the environment. To follow the material, install [miniconda](https://docs.conda.io/en/latest/miniconda.html) on your machine, create an environment from the file, then activate it: 

```console
uname@os:~$ conda env create --name pyfi --file=pyfi.yml
uname@os:~$ conda activate pyfi
```

With the virtual conda environment activated, create a jupyter kernel so that you are able to run all of the notebooks:

```console
uname@os:~$ python -m ipykernel install --user --name=pyfi
uname@os:~$ jupyter-lab
```

To export dependencies from the virtual enviornment into a reusable file, use the following conda command:

```console
(pyfi) uname@os: conda env export > pyfi.yml
```
