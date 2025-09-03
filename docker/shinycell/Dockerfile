## Use Rocker R 4.4.1 base (Debian + R 4.4.1 preinstalled)
FROM rocker/r-ver:4.4.1

ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt-get update && apt-get install -y \
    sudo \
    wget \
    curl \
    gdebi-core \
    libcurl4-openssl-dev \
    libglpk-dev \
    libssl-dev \
    libxml2-dev \
    libhdf5-dev \
    build-essential \
    liblzma-dev \
    libgsl-dev \
    build-essential \
    libbz2-dev \
    git \
    python3 \
    python3-pip \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Install Shiny &  Server dependencies
RUN R -e "reqPkg = c('shiny', 'shinyhelper','data.table','Matrix','DT','magrittr','ggplot2','ggrepel','hdf5r','ggdendro','gridExtra','ggpubr'); \
           newPkg = reqPkg[!(reqPkg %in% installed.packages()[,'Package'])]; \
           if(length(newPkg)) install.packages(newPkg)"
           
# Install ShinyCell2 dependencies
RUN R -e "reqPkg = c('data.table', 'Matrix', 'hdf5r', 'reticulate', 'R.utils', 'ggplot2', 'gridExtra', 'glue', 'readr', 'future', 'RColorBrewer'); \
           newPkg = reqPkg[!(reqPkg %in% installed.packages()[,'Package'])]; \
           if(length(newPkg)) install.packages(newPkg)"

# Install Shiny Server
RUN wget https://download3.rstudio.org/ubuntu-20.04/x86_64/shiny-server-1.5.23.1030-amd64.deb && \
    gdebi -n shiny-server-1.5.23.1030-amd64.deb && \
    rm shiny-server-1.5.23.1030-amd64.deb

# Optional: Seurat & Signac
RUN R -e "install.packages('Seurat')"
# RUN R -e "install.packages('Signac', repos='https://cran.rstudio.com/')"

# Optional: anndata
#RUN R -e "reticulate::py_install('anndata')"
RUN pip3 install --no-cache-dir anndata

# Install devtools + ShinyCell2
RUN R -e "install.packages('devtools')"
RUN R -e "devtools::install_github('the-ouyang-lab/ShinyCell2')"

## Install BiocManager + ArchR
RUN R -e "install.packages('BiocManager')"
RUN R -e "devtools::install_github('GreenleafLab/ArchR', ref='master', repos = BiocManager::repositories())"

EXPOSE 3838
CMD ["/usr/bin/shiny-server"]
