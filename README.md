# Stack Overflow Deep Cuts
Finds overlooked Stack Overflow questions worth answering.

## Installation

- Clone repository

        git clone https://github.com/klenwell/stack-overflow-deep-cuts.git
        cd stack-overflow-deep-cuts

- Prepare `secrets.yml`.

        cp secrets.yml{-dist,}

- Copy [Stack Overflow API key](https://api.stackexchange.com/) to `secrets.yml`:

        api-key: TBA

- Choose Python or Ruby version and see below.

## Python Version

It is recommended you use [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) to localize your environment.

### Install Dependencies

Adjust Python version (here `3.6.1`) as appropriate:

    cd python
    pyenv virtualenv 3.6.1 stack-overflow-deep-cuts
    pyenv local stack-overflow-deep-cuts
    pip install -r requirements.txt

### Run Script

    python main.py
