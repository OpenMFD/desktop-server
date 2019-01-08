OpenMFD Desktop Server
======================

This project is the MFD server that will be responsible for taking in any requests from the UI and running them on the
host machine.

Supported operating systems: Windows and macOS. Linux probably works, but I don't intend on testing it there. The only
reason macOS is supported is because it makes life easier for me as I'm building the UI on macOS.

## Running for development purposes

Note: This assumes you have at least Python 3.7 installed. If your Python3 binary is separate (such as `python3` update 
the first two command accordingly)

### On macOS/Linux:

Setup Python venv:

```bash
$ python -m venv venv
```

Active the environment:

```bash
$ source venv/bin/activate
```

Install dependencies:

```bash
$ pip install -r requirements.txt
```

Run dev server:

```bash
$ FLASK_ENV=development FLASK_APP=mfdserver flask run --host=0.0.0.0 --port=6789
```

Make sure you update the IP in the UI project with your local one so that it can connect if you're running it from a
different device on the network.