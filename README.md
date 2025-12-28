# Telegraph Parser

Async articles parser Telegra.ph

## Install

```bash
git clone https://github.com/Ladvix/telegraph-parser.git
cd telegraph-parser
pip install -r requirements.txt
```

## Usage

```bash
python main.py -k github
```

## Article url format

For example, https://telegra.ph/Telegraph-Parsing-12-28
- **Telegraph-Parsing** - article title
- **12** - month (december)
- **28** - day

If several articles with the same titles were published on the same date, then an ordinal number is added to the end of the url.

**Example:**
- https://telegra.ph/Telegraph-Parsing-12-28-2
- https://telegra.ph/Telegraph-Parsing-12-28-3