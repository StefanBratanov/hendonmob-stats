# hendonmob-stats

[![tests](https://github.com/StefanBratanov/hendonmob-stats/actions/workflows/tests.yml/badge.svg)](https://github.com/StefanBratanov/hendonmob-stats/actions/workflows/tests.yml)

Python scripts to extract, save and visualise data from [Hendon Mob](https://www.thehendonmob.com/). Look at the tests for usage. Once the data is saved, [gui.py](./gui.py) can be run to visualise the data.

## Prerequisites
- Python 3.7+

## Setup
```bash
pip install -r requirements.txt
# only if running gui.py
pip install pandasgui
```

## Run tests
```bash
python -m unittest extractors_tests database_tests
```

