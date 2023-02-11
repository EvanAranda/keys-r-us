# keys-r-us

-----

**Table of Contents**

- [Development](#setup)
- [License](#license)

## Development

### Install Hatch

This project uses hatch to manage environments.

```console
brew install hatch
```

### Create Default Environment

From the project directory:

```console
hatch env create
```

### Run the App

From the project directory:

```console
python keys_r_us/scripts/run_app.py
```

OR, for devtools support

```console
textual run --dev keys_r_us/scripts/run_dev.py
```

## License

`keys-r-us` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
