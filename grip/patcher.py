import re
import sys



INCOMPLETE_TASK_RE = re.compile(r'<li>\[ \] (.*?)(<ul.*?>|</li>)', re.DOTALL)
INCOMPLETE_TASK_SUB = (r'<li class="task-list-item">'
                       r'<input type="checkbox" '
                       r'class="task-list-item-checkbox" disabled=""> \1\2')
COMPLETE_TASK_RE = re.compile(r'<li>\[x\] (.*?)(<ul.*?>|</li>)', re.DOTALL)
COMPLETE_TASK_SUB = (r'<li class="task-list-item">'
                     r'<input type="checkbox" class="task-list-item-checkbox" '
                     r'checked="" disabled=""> \1\2')


HEADER_PATCH_RE = re.compile(r'<span>{:"aria-hidden"=&gt;"true", :class=&gt;'
                             r'"octicon octicon-link"}</span>', re.DOTALL)
HEADER_PATCH_SUB = r'<span class="octicon octicon-link"></span>'


MERMAID_CODE_RE = re.compile(r'<div class="highlight highlight-source-mermaid"><pre>(.*?)</pre></div>', re.DOTALL)


def convert_mermaid_to_div(match):
    """
    Converts GitHub's Mermaid code block to a proper Mermaid div container.
    """
    code_content = match.group(1)
    # Remove all HTML tags but preserve the text content
    clean_content = re.sub(r'<[^>]*>', '', code_content)
    # Clean up any remaining HTML entities
    clean_content = clean_content.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    # Normalize whitespace - remove extra spaces but keep line structure
    lines = [line.strip() for line in clean_content.split('\n') if line.strip()]
    clean_content = '\n'.join(lines)
    
    return f'<div class="mermaid">\n{clean_content}\n</div>'


def patch(html, user_content=False, with_mermaid=False):
    """
    Processes the HTML rendered by the GitHub API, patching
    any inconsistencies from the main site.
    """
    # FUTURE: Remove this once GitHub API renders task lists
    # https://github.com/isaacs/github/issues/309
    if not user_content:
        html = INCOMPLETE_TASK_RE.sub(INCOMPLETE_TASK_SUB, html)
        html = COMPLETE_TASK_RE.sub(COMPLETE_TASK_SUB, html)

    # FUTURE: Remove this once GitHub API fixes the header bug
    # https://github.com/joeyespo/grip/issues/244
    html = HEADER_PATCH_RE.sub(HEADER_PATCH_SUB, html)

    # Convert Mermaid code blocks to Mermaid diagram containers (if enabled)
    if with_mermaid:
        html = MERMAID_CODE_RE.sub(convert_mermaid_to_div, html)

    return html
