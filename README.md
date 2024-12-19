# CryptoTracker


## Setup python env
With conda:
```bash
conda create --name crypto_tracker python=3.11
conda activate crypto_tracker
pip install -r requirements.txt
```
With virtualenv:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Start main script
To start the main script, activate the python env, add this repo to the PYTHONPATH and start the script. For example:
```bash
conda activate crypto_tracker
export PYTHONPATH=/path/to/repos/CryptoTracker
cd /path/to/repos/CryptoTracker/crypto_tracker
python main.py --config_path=configs/main_config.yaml
```
Alternatively, you can start the script in the background with `nohup`:
```bash
nohup python main.py --config_path=configs/main_config.yaml > output.log 2>&1 &
```
