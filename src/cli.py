#!/usr/bin/env python3
import os
import asyncio
from typing import Optional, List, Dict, Any, Set
import click
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from crawl4ai import AsyncWebCrawler, CacheMode
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from functools import wraps
import urllib.parse
import pathlib
import re

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

def sanitize_filename(url: str) -> str:
    """Create a safe filename from URL"""
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.strip('/')
    if not path:
        path = 'index'
    elif path.endswith('/'):
        path = path[:-1] + '_index'
    return path.replace('/', '_')

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

@cli.command()
@click.argument('urls', nargs=-1)
@click.option('--from-file', '-f', type=click.Path(exists=True), help='Read URLs from file')
@click.option('--output-dir', '-o', type=click.Path(), required=True, help='Output directory for results')
@click.option('--max-concurrent', '-c', type=int, default=3, help='Maximum concurrent crawls')
@click.option('--batch-size', '-b', type=int, default=10, help='Batch size for processing')
@click.option('--format', type=click.Choice(['markdown', 'html', 'text']), default='markdown', help='Output format')
@click.option('--headless/--no-headless', default=True, help='Run browser in headless mode')
@click.option('--wait', '-w', type=float, default=1.0, help='Wait time between requests in seconds')
@async_command
async def crawl_many(urls: tuple, from_file: str, output_dir: str, max_concurrent: int,
                    batch_size: int, format: str, headless: bool, wait: float):
    """Crawl multiple URLs in parallel with optimized performance"""
    try:
        # Early error handling for input validation
        if not urls and not from_file:
            raise click.UsageError("Please provide URLs or a file containing URLs")

        # Prepare URLs list
        url_list = list(urls)
        if from_file:
            with open(from_file, 'r', encoding='utf-8') as f:
                url_list.extend(line.strip() for line in f if line.strip() and not line.startswith('#'))

        if not url_list:
            raise click.UsageError("No valid URLs provided")

        # Ensure output directory exists
        output_path = pathlib.Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Configure browser settings
        browser_conf = BrowserConfig(
            headless=headless,
            viewport_width=1280,
            viewport_height=720,
            verbose=True
        )

        # Create content filter
        prune_filter = PruningContentFilter(
            threshold=0.45,
            threshold_type="dynamic",
            min_word_threshold=5
        )

        # Create markdown generator
        md_generator = DefaultMarkdownGenerator(content_filter=prune_filter)

        # Configure crawler settings
        crawl_conf = CrawlerRunConfig(
            # Content filtering
            word_count_threshold=10,
            excluded_tags=['form', 'header', 'nav', 'footer'],
            exclude_external_links=True,

            # Content processing
            process_iframes=True,
            remove_overlay_elements=True,
            markdown_generator=md_generator,

            # Cache control
            cache_mode=CacheMode.ENABLED,

            # Wait time
            wait_time=wait,

            verbose=True
        )

        # Initialize progress tracking
        total_urls = len(url_list)
        completed = 0
        failed = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task(f"[cyan]Crawling URLs...", total=total_urls)

            async with AsyncWebCrawler(config=browser_conf) as crawler:
                # Process URLs in batches
                for i in range(0, len(url_list), batch_size):
                    batch = url_list[i:i + batch_size]

                    try:
                        # Use arun_many for parallel crawling
                        results = await crawler.arun_many(
                            urls=batch,
                            config=crawl_conf,
                            max_concurrent=max_concurrent
                        )

                        # Process results
                        for url, result in zip(batch, results):
                            if result.success:
                                try:
                                    # Generate filename from URL
                                    base_filename = sanitize_filename(url)
                                    filename = f"{base_filename}.{format}"
                                    filepath = output_path / filename

                                    # Get appropriate content based on format
                                    if format == 'markdown':
                                        content = result.markdown_v2.fit_markdown if hasattr(result, 'markdown_v2') else result.markdown
                                    elif format == 'html':
                                        content = result.html
                                    else:
                                        content = result.text

                                    # Save content
                                    if content:
                                        with open(filepath, 'w', encoding='utf-8') as f:
                                            f.write(content)
                                        completed += 1
                                    else:
                                        failed.append((url, "No content retrieved"))

                                except Exception as e:
                                    failed.append((url, f"Failed to save content: {str(e)}"))
                            else:
                                failed.append((url, result.error_message if hasattr(result, 'error_message') else 'Unknown error'))

                            # Update progress
                            progress.update(task, advance=1)

                    except Exception as batch_error:
                        # Handle batch-level errors
                        for url in batch:
                            failed.append((url, f"Batch processing error: {str(batch_error)}"))
                            progress.update(task, advance=1)

        # Final report
        table = Table(title="Crawl Results Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Total URLs", str(total_urls))
        table.add_row("Successfully Crawled", str(completed))
        table.add_row("Failed", str(len(failed)))

        console.print("\n")
        console.print(table)

        if failed:
            error_table = Table(title="Failed URLs", show_lines=True)
            error_table.add_column("URL", style="yellow")
            error_table.add_column("Error", style="red")

            for url, error in failed:
                error_table.add_row(url, str(error))

            console.print("\n")
            console.print(error_table)

    except Exception as e:
        console.print(Panel.fit(
            f"[red]Failed to complete multi-URL crawl:[/red]\n{str(e)}"
        ))
        raise click.Abort()

@cli.command()
@click.argument('base_url')
@click.option('--output-dir', '-o', type=click.Path(), required=True, help='Output directory for results')
@click.option('--max-concurrent', '-c', type=int, default=3, help='Maximum concurrent crawls')
@click.option('--batch-size', '-b', type=int, default=10, help='Batch size for processing')
@click.option('--format', type=click.Choice(['markdown', 'html', 'text']), default='markdown', help='Output format')
@click.option('--headless/--no-headless', default=True, help='Run browser in headless mode')
@click.option('--wait', '-w', type=float, default=1.0, help='Wait time between requests in seconds')
@async_command
async def crawl_docs(base_url: str, output_dir: str, max_concurrent: int,
                    batch_size: int, format: str, headless: bool, wait: float):
    """Automatically discover and crawl all documentation pages from a base URL"""
    try:
        console.print(f"[cyan]Discovering URLs from {base_url}...[/cyan]")

        # Configure browser
        browser_conf = BrowserConfig(
            headless=headless,
            viewport_width=1280,
            viewport_height=720,
            verbose=True
        )

        # Configure crawler for URL discovery
        discover_conf = CrawlerRunConfig(
            process_iframes=True,
            remove_overlay_elements=True,
            cache_mode=CacheMode.ENABLED,
            wait_time=wait,
            verbose=True
        )

        discovered_urls: Set[str] = set()
        base_domain = urllib.parse.urlparse(base_url).netloc

        async def discover_urls(url: str) -> List[str]:
            async with AsyncWebCrawler(config=browser_conf) as crawler:
                result = await crawler.arun(url=url, config=discover_conf)
                if not result.success:
                    console.print(f"[yellow]Warning: Failed to discover URLs from {url}[/yellow]")
                    return []

                # Extract URLs from the page
                urls = []
                if hasattr(result, 'links'):
                    # Get all internal links
                    internal_links = result.links.get("internal", [])
                    for link in internal_links:
                        parsed = urllib.parse.urlparse(link)
                        # Only include links from the same domain
                        if parsed.netloc == base_domain:
                            urls.append(link)
                return urls

        # Initial URL discovery
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Discovering documentation pages...", total=None)

            # Start with base URL
            urls_to_check = {base_url}
            discovered_urls.add(base_url)

            while urls_to_check:
                url = urls_to_check.pop()
                new_urls = await discover_urls(url)

                for new_url in new_urls:
                    if new_url not in discovered_urls:
                        discovered_urls.add(new_url)
                        urls_to_check.add(new_url)

                progress.update(task, description=f"[cyan]Discovered {len(discovered_urls)} pages...")

        console.print(f"[green]Found {len(discovered_urls)} documentation pages[/green]")

        # Sort URLs for consistent ordering
        url_list = sorted(discovered_urls)

        # Now crawl all discovered URLs using existing crawl_many logic
        await crawl_many.callback(
            urls=tuple(url_list),
            from_file=None,
            output_dir=output_dir,
            max_concurrent=max_concurrent,
            batch_size=batch_size,
            format=format,
            headless=headless,
            wait=wait
        )

    except Exception as e:
        console.print(Panel.fit(
            f"[red]Failed to crawl documentation:[/red]\n{str(e)}"
        ))
        raise click.Abort()

if __name__ == '__main__':
    cli()