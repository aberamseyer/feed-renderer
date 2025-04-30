#!/usr/bin/env python3

import sys
import feedparser
import time
import textwrap
import argparse
import html # For escaping HTML content

# (Keep format_date and get_author_string functions as they are)
def format_date(parsed_time_struct):
    """Formats a time.struct_time object into a readable string."""
    if parsed_time_struct:
        try:
            # Format: YYYY-MM-DD HH:MM:SS
            return time.strftime("%Y-%m-%d %H:%M:%S", parsed_time_struct)
        except Exception:
            return "Invalid Date"
    return "No Date Provided"

def get_author_string(entry):
    """Extracts author name(s) from an entry."""
    author = entry.get('author')
    # Handle structure where 'authors' is a list of dicts
    if not author and 'authors' in entry and entry.authors:
         author_list = [a.get('name', 'N/A') for a in entry.authors]
         # Filter out 'N/A' if other authors exist
         valid_authors = [a for a in author_list if a != 'N/A']
         if valid_authors:
             return ', '.join(valid_authors)
         elif author_list: # Only 'N/A' was found
             return 'N/A'
         else: # Empty authors list
             return 'N/A'
    return author if author else 'N/A'


# (Keep render_feed_text function as it is)
def render_feed_text(feed):
    """Renders the parsed feed content to standard output as plain text."""

    print("=" * 70)
    print("Feed Information")
    print("-" * 70)
    print(f"Title:       {feed.feed.get('title', 'N/A')}")
    print(f"Link:        {feed.feed.get('link', 'N/A')}")
    if 'subtitle' in feed.feed:
        print(f"Subtitle:    {feed.feed.subtitle}")
    feed_updated = feed.feed.get('updated_parsed') or feed.feed.get('published_parsed')
    print(f"Last Updated:{format_date(feed_updated)}")
    print("=" * 70)
    print("\nFeed Entries:")

    if not feed.entries:
        print("\n--- No entries found in the feed. ---")
        return

    for i, entry in enumerate(feed.entries):
        print("\n" + "-" * 70)
        print(f"Entry #{i + 1}")
        print("-" * 70)
        print(f"Title:     {entry.get('title', 'N/A')}")
        print(f"Link:      {entry.get('link', 'N/A')}")

        entry_date = entry.get('published_parsed') or entry.get('updated_parsed')
        print(f"Published: {format_date(entry_date)}")

        author_str = get_author_string(entry)
        print(f"Author:    {author_str}")

        # Display summary OR content in text mode
        content_text = None
        if entry.get('content'):
             # Try to get text content, fallback to summary
             primary_content = entry.content[0]
             if primary_content.type == 'text/plain':
                 content_text = primary_content.value
             elif primary_content.type in ['text/html', 'application/xhtml+xml']:
                 # In text mode, maybe just show a placeholder for HTML
                 content_text = "[HTML Content - View in HTML output]"
             else:
                 content_text = f"[Content type: {primary_content.type}]"

        if content_text:
             print("\nContent:")
             print(textwrap.fill(content_text, width=70, initial_indent='  ', subsequent_indent='  '))
        elif entry.get('summary'):
            print("\nSummary:")
            print(textwrap.fill(entry.summary, width=70, initial_indent='  ', subsequent_indent='  '))
        else:
             print("\nSummary/Content: N/A")


    print("\n" + "=" * 70)
    print(f"Total Entries Rendered: {len(feed.entries)}")
    print("=" * 70)


# --- HTML Rendering (MODIFIED) ---
def render_feed_html(feed, output_filename):
    """Renders the parsed feed content, including full entry content, to an HTML file."""

    feed_title = html.escape(feed.feed.get('title', 'Untitled Feed'))
    feed_link = html.escape(feed.feed.get('link', '#'))
    feed_subtitle = html.escape(feed.feed.get('subtitle', ''))
    feed_updated = format_date(feed.feed.get('updated_parsed') or feed.feed.get('published_parsed'))

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{feed_title}</title>
    <style>
        body {{ font-family: sans-serif; line-height: 1.6; margin: 2em; background-color: #f8f8f8; color: #333; }}
        .container {{ max-width: 800px; margin: auto; background-color: #fff; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        h1, h2 {{ color: #444; }}
        h1 a {{ text-decoration: none; color: inherit; }}
        .feed-header {{ border-bottom: 1px solid #eee; padding-bottom: 15px; margin-bottom: 20px; }}
        .feed-header p {{ margin: 5px 0; color: #666; }}
        article.entry {{ border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; background-color: #fff; border-radius: 4px; }}
        article.entry h2 {{ margin-top: 0; font-size: 1.4em; }}
        article.entry h2 a {{ text-decoration: none; color: #0066cc; }}
        article.entry h2 a:hover {{ text-decoration: underline; }}
        .entry-meta {{ font-size: 0.9em; color: #777; margin-bottom: 10px; border-bottom: 1px dashed #eee; padding-bottom: 10px;}}
        .entry-content {{ margin-top: 15px; }}
        /* Style for preformatted text content */
        .entry-content pre {{
            white-space: pre-wrap;       /* CSS3 */
            word-wrap: break-word;     /* Internet Explorer 5.5+ */
            background-color: #f6f8fa;
            padding: 10px;
            border: 1px solid #eaecef;
            border-radius: 3px;
            font-family: monospace, monospace; /* Monospace font */
            font-size: 0.9em;
        }}
        /* Basic styling for potential HTML content from the feed */
        .entry-content img {{ max-width: 100%; height: auto; }} /* Responsive images */
        a {{ color: #0066cc; }}
    </style>
</head>
<body>
    <div class="container">
        <header class="feed-header">
            <h1><a href="{feed_link}" target="_blank" rel="noopener noreferrer">{feed_title}</a></h1>
"""
    if feed_subtitle:
        html_content += f"            <p>{feed_subtitle}</p>\n"
    html_content += f"""
            <p>Last Updated: {feed_updated}</p>
        </header>

        <section class="entries">
"""

    if not feed.entries:
        html_content += "            <p><em>--- No entries found in the feed. ---</em></p>\n"
    else:
        for entry in feed.entries:
            entry_title = html.escape(entry.get('title', 'No Title'))
            entry_link = html.escape(entry.get('link', '#'))
            entry_date_struct = entry.get('published_parsed') or entry.get('updated_parsed')
            entry_date_str = format_date(entry_date_struct)
            entry_author_str = html.escape(get_author_string(entry))

            # --- Determine content to display ---
            entry_body_html = ""
            if entry.get('content'):
                primary_content = entry.content[0]
                content_value = primary_content.value
                content_type = primary_content.type

                if content_type in ('text/html', 'application/xhtml+xml'):
                    # ************************************************************
                    # WARNING: Rendering HTML content directly from the feed.
                    # This assumes the feed source is trusted. Untrusted feeds
                    # could contain malicious scripts (XSS).
                    # Consider using an HTML sanitization library (like bleach)
                    # for untrusted sources.
                    # ************************************************************
                    entry_body_html = content_value # Render as HTML
                elif content_type == 'text/plain':
                    # Escape plain text and wrap in <pre> for formatting
                    entry_body_html = f"<pre>{html.escape(content_value)}</pre>"
                else:
                    # Handle other types by escaping and showing type
                    entry_body_html = (
                        f"<p><i>Unsupported content type: {html.escape(content_type)}. Displaying escaped value:</i></p>"
                        f"<pre>{html.escape(content_value)}</pre>"
                    )
            elif entry.get('summary'):
                # Fallback to summary if no content
                escaped_summary = html.escape(entry.summary)
                entry_body_html = f"<p>{escaped_summary}</p>" # Display escaped summary as a paragraph
            else:
                # Neither content nor summary available
                entry_body_html = "<p><em>No content or summary available.</em></p>"
            # --- End content determination ---


            html_content += f"""
            <article class="entry">
                <h2><a href="{entry_link}" target="_blank" rel="noopener noreferrer">{entry_title}</a></h2>
                <div class="entry-meta">
                    <span>Published: {entry_date_str}</span> |
                    <span>Author: {entry_author_str}</span>
                </div>
                <div class="entry-content">
                    {entry_body_html}
                </div>
            </article>
"""

    html_content += """
        </section>

        <footer>
            <p style="text-align: center; font-size: 0.8em; color: #999;">
                Generated by Atom Feed Renderer
            </p>
        </footer>
    </div>
</body>
</html>
"""

    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML output successfully written to: {output_filename}", file=sys.stderr)
    except IOError as e:
        print(f"ERROR: Could not write to file {output_filename}: {e}", file=sys.stderr)
        sys.exit(1)


# --- Main Execution (No changes needed here) ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Parse and render an Atom feed provided via stdin.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
            Examples:
              cat myfeed.atom | python render_atom.py
              python render_atom.py < myfeed.atom
              cat myfeed.atom | python render_atom.py --html feed_output.html
              python render_atom.py --html report.html < myfeed.atom
            ''')
    )
    parser.add_argument(
        '--html',
        metavar='FILENAME',
        help='Render output as HTML to the specified file instead of plaintext to stdout.'
    )

    args = parser.parse_args()

    # Simplified stderr message for pasting
    if sys.stdin.isatty(): # Only show prompt if input is coming from a terminal
        print("Paste Atom feed below, then press Ctrl+D (Unix) or Ctrl+Z+Enter (Windows)...", file=sys.stderr)

    try:
        atom_feed_plaintext = sys.stdin.read()

        if not atom_feed_plaintext.strip():
            print("\nERROR: No input received.", file=sys.stderr)
            sys.exit(1)

        # Parse the feed (do this once)
        print("Parsing feed...", file=sys.stderr)
        feed = feedparser.parse(atom_feed_plaintext)

        # --- Basic Error Handling ---
        if feed.bozo:
            print(f"WARNING: Feed may be malformed. Error: {feed.bozo_exception}\n", file=sys.stderr)

        if not feed.feed and not feed.entries:
             print("ERROR: Could not parse feed. Input does not seem to be a valid Atom/RSS feed.", file=sys.stderr)
             sys.exit(1)

        # --- Decide on Rendering ---
        if args.html:
            print(f"Rendering feed to HTML file: {args.html}", file=sys.stderr)
            render_feed_html(feed, args.html)
        else:
            print("Rendering feed to standard output (plaintext)...", file=sys.stderr)
            # Add a newline before text output if not rendering HTML, for cleaner separation from stderr messages
            print("\n---\n", file=sys.stderr)
            render_feed_text(feed)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
