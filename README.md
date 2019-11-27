# MATIC - Model Analysis Tool for Integrity and Conformance

Proof-of-concept implementation of model-driven-software-development
tool presented in the
paper *MATIC: Model Analysis Tool for Integrity and Conformance*.

Building
--------

To build, clone this repository and run the command;

```bash
docker build -t docker-matic .
```

Running
-------

To run, after building, run the command;

```bash
docker run --rm -it docker-matic
```

#### State Machine Program

```bash
cd src/GraphicalExample
python convert_software_model.py software_model.xml HelloWorld.json
cp HelloWorld.json ../
cd ../
python compile_application.py HelloWorld.json PROG.json
python run_compiled_application.py HelloWorld.json PROG.json

Event Shell>MyTrigger
Event Shell>MyTrigger
CTRL+C
```

#### NaCl Cryptographic Program

```bash
cd src
python compile_application.py example_nacl.json PROG.json
python run_compiled_application.py example_nacl.json PROG.json

Event Shell>CryptoTest
Event Shell>CryptoTest
Event Shell>ToggleErrors
Event Shell>CryptoTest
Event Shell>ToggleErrors
Event Shell>CryptoTest
CTRL+C
```

#### Zlib Data Compression Example

```bash
cd src
python compile_application.py example_zlib.json PROG.json
python run_compiled_application.py example_zlib.json PROG.json

Event Shell>DeflateInflate
CTRL+C
```
