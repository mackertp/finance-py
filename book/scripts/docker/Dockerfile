# 
# Building a Docker Image with latest
# version of Ubuntu and basic Python.
#
# @author Preston Mackert
#

FROM ubuntu:latest
LABEL maintainer='preston'

# add the install script, give permissions, then run
ADD install.sh /
RUN chmod u+x /install.sh
RUN /install.sh

# prepend the new path
ENV PATH /root/miniconda3/bin:$PATH

# execute IPython when the container is run
CMD ["ipython"]