This repository scrapes the dynamic gas and/or electricity prices from https://vrijopnaam.app. The code contains command-line functionality and import functionality.

# Requirements
- Clone repo (or use `pip install git+https://github.com/MarcDirven/vrijopnaam-prices`)
- Create venv `python -m venv venv`
- Activate the venv (usage: `activate[.ps1 | .bat]`) 
- Install requirements.txt `pip install -r requirements.txt`
- Set your password under key environment variable `VRIJOPNAAM_PASSWORD` or pass it directly to the script
- Set your username under key environment variable `VRIJOPNAAM_USERNAME` or pass it directly to the script
- Usage: `python get_vrijopnaam_prices.py [--username <username>] [--password <password>] [--pretty-output] [--gas-prices] [--electricity-prices]`
- or: 
```python
import vrijopnaam_prices as prices
import asyncio

async def main():
    p = await prices.get_prices('username', 'password')
    json_format = p.to_json()
    print(json_format)
    

if __name__ == '__main__':
    asyncio.run(main())
```
