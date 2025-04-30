# Atom Feed Renderer

1.  Reads Atom feed plaintext from standard input (stdin).
2.  Parses the feed using `feedparser`.
3.  Renders the main feed information (title, link, subtitle).
4.  Renders key information for each entry (title, link, published date, author, summary).
5.  Includes basic error handling for invalid feeds.
6.  Formats dates nicely.

---

**1. Prerequisites:**
Requires `feedparser` library:

```bash
python -m venv .venv
source .venv/bin/activate
pip install feedparser
```

# How to Use

1.  **Make Executable (Optional, Linux/macOS):** `chmod +x render_atom.py`
2.  **Run and Provide Input:**

    *   **Option A: Paste Input Directly**
        Run the script. It will wait for input. Paste your entire Atom feed XML content into the terminal, then press `Ctrl+D` (on Linux/macOS) or `Ctrl+Z` followed by `Enter` (on Windows) to signal the end of the input.

        ```bash
        python render_atom.py
        # --- or ---
        # ./render_atom.py
        ```
        *(Now paste your Atom feed XML here)*
        ```xml
        <?xml version="1.0" encoding="utf-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
          <title>Example Feed</title>
          <link href="http://example.org/"/>
          <updated>2023-10-27T18:30:02Z</updated>
          <author>
            <name>John Doe</name>
          </author>
          <id>urn:uuid:60a76c80-d399-11d9-b93C-0003939e0af6</id>
          <entry>
            <title>Atom-Powered Robots Run Amok</title>
            <link href="http://example.org/2003/12/13/atom03"/>
            <id>urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a</id>
            <updated>2023-10-26T19:25:00Z</updated>
            <published>2023-10-26T19:20:00Z</published>
            <summary>Some text.</summary>
          </entry>
          <entry>
            <title>Second Entry</title>
            <link href="http://example.org/2003/12/14/second"/>
            <id>urn:uuid:1225c695-cfb8-4ebb-bbbb-80da344efa6b</id>
            <updated>2023-10-27T10:00:00Z</updated>
            <summary>Another summary text, potentially longer to demonstrate wrapping capabilities.</summary>
            <author><name>Jane Smith</name></author>
         </entry>
        </feed>
        ```
        *(Then press Ctrl+D or Ctrl+Z+Enter)*

    *   **Option B: Pipe from a File**
        If you have the Atom feed saved in a file (e.g., `myfeed.atom`), you can pipe it into the script:

        ```bash
        cat myfeed.atom | python render_atom.py
        # --- or on Windows ---
        # type myfeed.atom | python render_atom.py
        # --- or if executable ---
        # cat myfeed.atom | ./render_atom.py
        ```

    *   **Option C: Redirect Input from a File**
        Alternatively, use input redirection:

        ```bash
        python render_atom.py < myfeed.atom
        # --- or if executable ---
        # ./render_atom.py < myfeed.atom
        ```

## Formatting output

1.  **Plaintext Output (Default):** Use it exactly as before. It will print formatted text to your terminal (stdout).
    ```bash
    # Pipe from file
    cat myfeed.atom | python render_atom.py

    # Redirect from file
    python render_atom.py < myfeed.atom

    # Paste directly (Ctrl+D/Ctrl+Z+Enter when done)
    python render_atom.py
    ```
2.  **HTML Output:** Use the `--html` flag followed by the desired output filename. The script will *not* print the feed to the terminal (stdout) in this mode, but it will print status messages to stderr and create the HTML file.
    ```bash
    # Pipe from file
    cat myfeed.atom | python render_atom.py --html my_rendered_feed.html

    # Redirect from file
    python render_atom.py --html my_rendered_feed.html < myfeed.atom

    # Paste directly (Ctrl+D/Ctrl+Z+Enter when done)
    python render_atom.py --html my_rendered_feed.html
    ```
    After running, you will find a file named `my_rendered_feed.html` (or whatever name you provided) in the current directory. You can open this file in a web browser to view the rendered feed.

