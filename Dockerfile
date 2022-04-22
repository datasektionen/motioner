FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  python3.8 \
  pip \
  curl \
  texlive-latex-extra \
  texlive-lang-european \
  latexmk

RUN mkdir /app 
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x start.sh
CMD ["./start.sh"]
EXPOSE 5000