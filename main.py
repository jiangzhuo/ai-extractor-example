import re
import asyncio
from pyppeteer import launch
from html_to_markdown import convert_html_to_markdown, convert_html_to_markdown_v2

# Patterns
SCRIPT_PATTERN = r"<[ ]*script.*?\/[ ]*script[ ]*>"
STYLE_PATTERN = r"<[ ]*style.*?\/[ ]*style[ ]*>"
META_PATTERN = r"<[ ]*meta.*?>"
COMMENT_PATTERN = r"<[ ]*!--.*?--[ ]*>"
LINK_PATTERN = r"<[ ]*link.*?>"
BASE64_IMG_PATTERN = r'<img[^>]+src="data:image/[^;]+;base64,[^"]+"[^>]*>'
SVG_PATTERN = r"(<svg[^>]*>)(.*?)(<\/svg>)"


def replace_svg(html: str, new_content: str = "this is a placeholder") -> str:
    return re.sub(
        SVG_PATTERN,
        lambda match: f"{match.group(1)}{new_content}{match.group(3)}",
        html,
        flags=re.DOTALL,
    )


def replace_base64_images(html: str, new_image_src: str = "#") -> str:
    return re.sub(BASE64_IMG_PATTERN, f'<img src="{new_image_src}"/>', html)


def clean_html(html: str, clean_svg: bool = False, clean_base64: bool = False):
    html = re.sub(
        SCRIPT_PATTERN, "", html, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL
    )
    html = re.sub(
        STYLE_PATTERN, "", html, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL
    )
    html = re.sub(
        META_PATTERN, "", html, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL
    )
    html = re.sub(
        COMMENT_PATTERN, "", html, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL
    )
    html = re.sub(
        LINK_PATTERN, "", html, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL
    )

    if clean_svg:
        html = replace_svg(html)
    if clean_base64:
        html = replace_base64_images(html)
    return html


async def fetch_and_clean_webpage(url: str, clean_svg: bool = False, clean_base64: bool = False):
    # Launch browser
    browser = await launch(headless=True)
    try:
        # Create new page
        page = await browser.newPage()
        
        # Navigate to URL and wait until network is idle
        await page.goto(url, {'waitUntil': 'networkidle0'})
        
        # Get page content
        content = await page.content()
        
        # Clean HTML
        cleaned_html = clean_html(content, clean_svg=clean_svg, clean_base64=clean_base64)
        
        return cleaned_html
    finally:
        # Make sure to close the browser
        await browser.close()


async def main():
    # Example usage
    url = "https://www.ingni-store.com/item/1999-600029"
    # url = "https://www.example.com"
    cleaned_html = await fetch_and_clean_webpage(url, clean_svg=True, clean_base64=True)
    print("Cleaned HTML:")
    print(cleaned_html[:500])  # Print first 500 characters as preview

    markdown_text = convert_html_to_markdown(cleaned_html)
    print("Markdown Text:")
    print(markdown_text[:500])  # Print first 500 characters as preview

    # Save markdown text to a file
    with open("output.md", "w") as f:
        f.write(markdown_text)


if __name__ == "__main__":
    asyncio.run(main())
