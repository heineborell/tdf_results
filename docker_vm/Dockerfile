FROM ubuntu:22.04

# Install Ubuntu-specific packages including Zsh and other tools
RUN apt-get update && \
    apt-get install -y curl wget build-essential git python3 python3-pip zsh unzip && \ 
    apt-get install -y virtualenv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Install dependencies
RUN apt-get update -y && apt-get install -y wget xvfb unzip jq

# Install Google Chrome dependencies
RUN apt-get install -y libxss1 libappindicator1 libgconf-2-4 \
    fonts-liberation libasound2 libnspr4 libnss3 libx11-xcb1 libxtst6 lsb-release xdg-utils \
    libgbm1 libnss3 libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 libxcb-dri3-0


# Fetch the latest version numbers and URLs for Chrome and ChromeDriver
RUN curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json > /tmp/versions.json

RUN CHROME_URL=$(jq -r '.channels.Stable.downloads.chrome[] | select(.platform=="linux64") | .url' /tmp/versions.json) && \
    wget -q --continue -O /tmp/chrome-linux64.zip $CHROME_URL && \
    unzip /tmp/chrome-linux64.zip -d /opt/chrome

RUN chmod +x /opt/chrome/chrome-linux64/chrome


RUN CHROMEDRIVER_URL=$(jq -r '.channels.Stable.downloads.chromedriver[] | select(.platform=="linux64") | .url' /tmp/versions.json) && \
    wget -q --continue -O /tmp/chromedriver-linux64.zip $CHROMEDRIVER_URL && \
    unzip /tmp/chromedriver-linux64.zip -d /opt/chromedriver && \
    chmod +x /opt/chromedriver/chromedriver-linux64/chromedriver

# Set up Chromedriver Environment variables
ENV CHROMEDRIVER_DIR=/opt/chromedriver
ENV PATH=$CHROMEDRIVER_DIR:$PATH

# Clean upa
RUN rm /tmp/chrome-linux64.zip /tmp/chromedriver-linux64.zip /tmp/versions.json

# python dependencies
RUN pip install selenium

RUN apt-get install software-properties-common -y &&\
add-apt-repository ppa:neovim-ppa/unstable -y && \
apt update && \
apt install make gcc ripgrep xclip neovim -y


# Set up project directory
WORKDIR /project

# Create a virtual environment and clone the repository
RUN virtualenv -p python3 env && \
    git clone https://github.com/heineborell/tdf_results

# Set the virtual environment as default
ENV PATH="/project/env/bin:$PATH"

# Create a directory; -p ensures parent directories are created if they don't exist
RUN mkdir -p /root/.config/

# Set the working directory to /root
WORKDIR /root

RUN apt-get update && apt-get install -y \
    && add-apt-repository ppa:neovim-ppa/stable \
    && apt-get update && apt-get install -y neovim \
    && apt-get clean

# Clone the dot-files repository directly into /root/.config
RUN git clone https://github.com/heineborell/dot-files /root/.config/

# Set Zsh as the default shell
RUN chsh -s /bin/zsh

# Install the default powerline10k theme with no plugins
# RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.2.1/zsh-in-docker.sh)"

