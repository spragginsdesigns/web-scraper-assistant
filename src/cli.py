#!/usr/bin/env python3
import os
import asyncio
from typing import Optional, List, Dict, Any
import click
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from crawl4ai import AsyncWebCrawler, CacheMode
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from functools import wraps

# Initialize Rich console
console = Console()

# Load environment variables
load_dotenv()

def async_command(f):
    """Decorator to run async click commands"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper

@click.group()
def cli():
    """Web Scraper Assistant - A command line interface powered by Crawl4AI"""
    pass

@cli.command()
def version():
    """Display the current version of the CLI"""
    console.print(Panel.fit(
        f"[green]Web Scraper Assistant v0.1.0[/green]\n"
        f"Crawl4AI installed"
    ))

@cli.command()
@click.argument('url')
@click.option('--depth', '-d', type=int, default=3, help='Maximum crawl depth')
@click.option('--wait', '-w', type=float, default=1.0, help='Wait time between requests in seconds')
@click.option('--format', '-f', type=click.Choice(['markdown', 'html', 'text']), default='markdown', help='Output format')
@click.option('--output', '-o', type=str, help='Output file path')
@click.option('--headless/--no-headless', default=True, help='Run browser in headless mode')
@async_command
async def crawl(url: str, depth: int, wait: float, format: str, output: Optional[str], headless: bool):
    """Start a new web crawl"""
    try:
        with console.status("[bold green]Initializing crawler...") as status:
            # Configure browser settings
            browser_conf = BrowserConfig(
                headless=headless,
                viewport_width=1280,
                viewport_height=720,
                verbose=True
            )

            # Create content filter
            prune_filter = PruningContentFilter(
                threshold=0.45,  # Lower threshold to catch more content
                threshold_type="dynamic",
                min_word_threshold=5
            )

            # Create markdown generator with content filter
            md_generator = DefaultMarkdownGenerator(content_filter=prune_filter)

            # Configure crawler settings with improved options
            crawl_conf = CrawlerRunConfig(
                # Content filtering
                word_count_threshold=10,  # Lower threshold to catch more content
                excluded_tags=['form', 'header', 'nav', 'footer'],  # Exclude unnecessary elements
                exclude_external_links=True,  # Focus on internal content

                # Content processing
                process_iframes=True,  # Handle iframe content
                remove_overlay_elements=True,  # Remove popups/modals
                markdown_generator=md_generator,  # Use our configured markdown generator

                # Cache control (using new CacheMode)
                cache_mode=CacheMode.ENABLED,  # Use cache if available

                verbose=True
            )

            async with AsyncWebCrawler(config=browser_conf) as crawler:
                status.update("[bold green]Starting crawl...")
                result = await crawler.arun(
                    url=url,
                    config=crawl_conf
                )

                if not result.success:
                    console.print(Panel.fit(
                        f"[red]Failed to crawl:[/red]\n"
                        f"Status code: {result.status_code}\n"
                        f"Error: {result.error_message if hasattr(result, 'error_message') else 'Unknown error'}"
                    ))
                    return

                if output:
                    # Use the appropriate markdown version based on format
                    if format == 'markdown':
                        content = result.markdown_v2.fit_markdown if hasattr(result, 'markdown_v2') else result.markdown
                    else:
                        content = result.html if format == 'html' else result.text

                    if content:
                        with open(output, 'w', encoding='utf-8') as f:
                            f.write(content)
                        console.print(Panel.fit(
                            f"[green]Crawl completed successfully![/green]\n"
                            f"Results saved to: {output}"
                        ))
                    else:
                        console.print(Panel.fit(
                            f"[yellow]Warning:[/yellow] No content was retrieved in {format} format"
                        ))
                else:
                    # Display results in console
                    table = Table(title=f"Crawl Results")
                    table.add_column("Property", style="cyan")
                    table.add_column("Value", style="green")

                    # Add more detailed crawl statistics
                    if hasattr(result, 'status_code'):
                        table.add_row("Status Code", str(result.status_code))
                    if hasattr(result, 'total_time'):
                        table.add_row("Total Time", f"{result.total_time:.2f}s")

                    # Add media statistics if available
                    if hasattr(result, 'media'):
                        images_count = len(result.media.get("images", []))
                        table.add_row("Images Found", str(images_count))

                    # Add link statistics if available
                    if hasattr(result, 'links'):
                        internal_links = len(result.links.get("internal", []))
                        table.add_row("Internal Links", str(internal_links))

                    console.print(table)

                    # Show content preview using appropriate markdown version
                    if format == 'markdown':
                        content = result.markdown_v2.fit_markdown if hasattr(result, 'markdown_v2') else result.markdown
                    else:
                        content = result.html if format == 'html' else result.text

                    if content:
                        console.print(Panel.fit(
                            "[bold]Content Preview:[/bold]\n" +
                            content[:500] + "..."
                        ))
                    else:
                        console.print(Panel.fit(
                            f"[yellow]Warning:[/yellow] No content was retrieved in {format} format"
                        ))

    except Exception as e:
        console.print(Panel.fit(
            f"[red]Failed to complete crawl:[/red]\n{str(e)}"
        ))

@cli.command()
@async_command
async def doctor():
    """Run diagnostics to verify the setup"""
    try:
        browser_conf = BrowserConfig(headless=True, verbose=True)
        async with AsyncWebCrawler(config=browser_conf) as crawler:
            console.print(Panel.fit(
                "[green]✓ Crawl4AI installation verified[/green]\n"
                "✓ Browser automation ready\n"
                "✓ System requirements met"
            ))
    except Exception as e:
        console.print(Panel.fit(
            f"[red]! Setup verification failed[/red]\n{str(e)}"
        ))

if __name__ == '__main__':
    cli()