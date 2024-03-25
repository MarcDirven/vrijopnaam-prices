This repository scrapes the dynamic gas and/or electricity prices from https://vrijopnaam.app. The code contains command-line functionality and import functionality.

# Usage
- At least python 3.10 is needed
- Optional:
  - Set your password under key environment `VRIJOPNAAM_PASSWORD` (or pass it directly to the script)
  - Set your username under key environment `VRIJOPNAAM_USERNAME` (or pass it directly to the script)
  - Create venv `python -m venv venv`
  
  - Activate the venv:
    - Linux users `. venv/bin/activate`
    - Powershell (Windows) `.\venv\Scripts\activate.ps1`
    - Batch (Windows) `.\venv\Scripts\activate.bat`
- `pip install git+https://github.com/MarcDirven/vrijopnaam-prices`
- `--indent, -i` can be used to beautify the json output
- Usage: `get-vrijopnaam-prices [--username, -u <username>] [--password, -p <password>] [--gas-prices, -g] [--electricity-prices, -e] [--indent <number>]`
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
