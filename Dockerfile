FROM continuumio/miniconda3

WORKDIR /home/darvis

COPY . ./
RUN chmod +x start_darvis.sh

RUN conda env create -f environment.yml

RUN echo "source activate darvis" > ~/.bashrc
ENV PATH /opt/conda/envs/darvis/bin:$PATH

EXPOSE 5000

ENTRYPOINT ["./start_darvis.sh"]
