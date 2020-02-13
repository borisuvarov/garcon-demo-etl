# Hello World ETL based on garcon/SWF

## Installation (Mac OS)
1. Copy .env.shadow to .env, add AWS credentials.
2. Run `make install_without_dev_from_lock`.
3. Run `brew install redis`.
4. Run `brew services start redis`.

# Run
1. Create PyCharm run configurations for decider, worker and exec processes, or run them via commands like this one: `pipenv run python cli.py decider hello_world`.
2. Run exec process.
