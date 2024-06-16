import re
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"

def extract_title(markdown):
    heading_pattern = r'^# (.+)'  # Regular expression to match `h1` header
    match = re.search(heading_pattern, markdown, re.MULTILINE)  # Search for the heading pattern
    
    if match:  # If a match is found
        return match.group(1)  # Return the text captured in the first group (the header text)
    else:
        raise ValueError("No h1 header found. All pages need a single h1 header.")  # Raise an exception if no heading is found


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_olist:
        return olist_to_html_node(block)
    if block_type == block_type_ulist:
        return ulist_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")
    
def block_to_block_type(markdown):
    # This pattern will match strings that start with 1 to 6 '#' characters followed by a space.
    heading_pattern = r'^#{1,6} '
    
    if re.match(heading_pattern, markdown):
        return block_type_heading

    # This pattern will match strings starting with three backticks.
    code_pattern = r'^```'
    
    if re.match(code_pattern, markdown):
        return block_type_code

    # This pattern will match strings starting with '>' for quotes.
    quote_pattern = r'^>'
    
    if re.match(quote_pattern, markdown):
        return block_type_quote

    # This pattern will match unordered list items starting with '*' or '-' followed by a space.
    unordered_list_pattern = r'^(\*|-)\s'
    
    if re.match(unordered_list_pattern, markdown):
        return block_type_ulist

    # This pattern will match ordered list items starting with a number followed by a '.' and a space.
    ordered_list_pattern = r'^\d+\. '
    
    if re.match(ordered_list_pattern, markdown):
        return block_type_olist

    # If none of the above patterns match, it's a paragraph.
    return block_type_paragraph

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:].strip()  # Trim leading and trailing spaces
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    items = block.split("\n")
    new_lines = []
    for item in items:
        if not item.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(item.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)