# EmailSystem

This application is used to send scheduled email. For now, this application is limited to *outlook*.

## How to run application

1. Create virtual environment `python3 -m venv <env_name>`
2. Activate virtual environment `sourve <env_name>/bin/activate`
3. Install **pip-tools** to handle dependencies `pip3 install pip-tools`
4. Main dependencies are saved wihin **requirements.in**, use `pip-compile ./requirements.in` to extract other dependencies to **requirements.txt**
5. Update virtual environment with `pip-sync`
6. Run application `python3 run.py`

## How to run unit test

1. Activate virtual environment
2. Run test `pytest tests/`