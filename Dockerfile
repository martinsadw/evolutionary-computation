FROM r-base:latest

RUN apt update && apt install python3 python3-pip -y
RUN pip3 install numpy matplotlib scipy
RUN Rscript -e "install.packages('irace', repos='https://cran.fiocruz.br/')"

VOLUME /evolutionary-computation

WORKDIR /evolutionary-computation
CMD ./run_irace.sh

# docker build -t martinsadw/evolutionary-computation .
# docker run -d --rm --name pso-container -v /home/getcomp/Documents/Andre/evolutionary-computation/:/evolutionary-computation martinsadw/evolutionary-computation
