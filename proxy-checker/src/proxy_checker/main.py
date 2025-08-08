import click
from pathlib import Path

from .models import Proxy
from .storage import ProxyStorage
from .checker import run_checks_concurrently

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@click.group()
def cli():
    pass


@cli.command()
@click.argument('proxy_string', type=str)
@click.option('--test-url', default='https://api.ipify.org?format=json', help='URL of the IP test service.')
@click.option('--csv-path', default='proxies.csv', help='Path to the output CSV file.')
@click.option('--timeout', default=10, help='Request timeout in seconds.')
def single(proxy_string, test_url, csv_path, timeout):
    try:
        protocol, address = proxy_string.strip().split("://", 1)
        host, port_str = address.split(":", 1)
        proxy = Proxy(protocol, host, int(port_str))
    except ValueError:
        raise click.BadParameter('Provide proxy in format: protocol://host:port (e.g., http://1.2.3.4:8080)')
    
    result = run_checks_concurrently([proxy], test_url, timeout, max_workers=1) # Run the check

    if result:
        storage = ProxyStorage(Path(csv_path))
        storage.save_proxies(result)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False, resolve_path=True))
@click.option('--test-url', default='https://api.ipify.org?format=json', help='URL of the IP test service.')
@click.option('--csv-path', default='proxies.csv', help='Path to the output CSV file.')
@click.option('--timeout', default=10, help='Request timeout in seconds.')
@click.option('--workers', default=10, help='Number of concurrent workers.')
def file(input_file, test_url, csv_path, timeout, workers):
    in_path = Path(input_file)
    storage = ProxyStorage(Path(csv_path))
    
    proxies_to_test = []
    if in_path.suffix == '.txt':
        click.echo(f"Loading proxies from text file: {in_path}")
        proxies_to_test = storage.load_from_text(in_path)
    elif in_path.suffix == '.csv':
        click.echo(f"Re-testing proxies from CSV file: {in_path}")
        storage.path = in_path # Point storage to the input file for loading
        proxies_to_test = storage.load_from_csv()
    else:
        raise click.BadParameter("Input file must be a .txt or .csv file.")

    if not proxies_to_test:
        click.echo("No valid proxies found to test.")
        return
    
    results = run_checks_concurrently(proxies_to_test, test_url, timeout, workers) # Run checks concurrently
    
    output_storage = ProxyStorage(Path(csv_path))
    output_storage.save_proxies(results)


if __name__ == '__main__':
    cli()