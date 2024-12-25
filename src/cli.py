#!/usr/bin/env python3
import os
from typing import Optional
import click
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from firecrawl import FirecrawlApp

# Initialize Rich console
console = Console()

# Load environment variables
load_dotenv()

# Get API key from environment
API_KEY = os.getenv('FIRECRAWL_API_KEY')

def get_client() -> FirecrawlApp:
    """Get an initialized Firecrawl client"""
    return FirecrawlApp(api_key=API_KEY)

@click.group()
def cli():
    """Firecrawl CLI - A command line interface for Firecrawl API"""
    if not API_KEY:
        console.print(Panel.fit(
            "[red]Error: FIRECRAWL_API_KEY not found in environment variables[/red]"
        ))
        raise click.Abort()

@cli.command()
def version():
    """Display the current version of the CLI"""
    console.print(Panel.fit(
        "[green]Firecrawl CLI v0.1.0[/green]"
    ))

@cli.command()
@click.argument('url')
@click.option('--depth', '-d', type=int, default=3, help='Maximum number of pages to crawl')
@click.option('--wait', '-w', type=float, default=0, help='Wait time between requests in seconds')
@click.option('--format', '-f', type=click.Choice(['markdown', 'html', 'both']), default='both', help='Output format')
def crawl(url: str, depth: int, wait: float, format: str):
    """Start a new web crawl"""
    client = get_client()

    with console.status("[bold green]Starting crawl...") as status:
        formats = ["markdown", "html"] if format == "both" else [format]

        try:
            response = client.crawl_url(
                url,
                params={
                    'limit': depth,
                    'scrapeOptions': {
                        'formats': formats
                    }
                }
            )

            console.print(Panel.fit(
                f"[green]Crawl started successfully![/green]\n"
                f"Response: {response}"
            ))

            # Automatically show initial status
            try:
                status_response = client.check_crawl_status(response)
                table = Table(title=f"Initial Crawl Status")
                table.add_column("Property", style="cyan")
                table.add_column("Value", style="green")

                for key, value in status_response.items():
                    table.add_row(key, str(value))

                console.print(table)
            except Exception as e:
                console.print(Panel.fit(
                    f"[yellow]Note: Could not fetch initial status[/yellow]\n{str(e)}"
                ))

        except Exception as e:
            console.print(Panel.fit(
                f"[red]Failed to start crawl:[/red]\n{str(e)}"
            ))

@cli.command()
@click.argument('crawl_id')
def status(crawl_id: str):
    """Check the status of a crawl"""
    client = get_client()

    with console.status("[bold green]Checking status...") as status:
        try:
            response = client.check_crawl_status(crawl_id)

            table = Table(title=f"Crawl Status: {crawl_id}")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="green")

            for key, value in response.items():
                table.add_row(key, str(value))

            console.print(table)

        except Exception as e:
            console.print(Panel.fit(
                f"[red]Failed to get status:[/red]\n{str(e)}"
            ))

if __name__ == '__main__':
    cli()