import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        extracted_images = extract_markdown_images(old_node.text)
        if extracted_images == []:
            new_nodes.append(old_node)
        else:
            current_text = old_node.text
            for image in extracted_images:
                # Define the search pattern based on image tuple
                search_pattern = f"![{image[0]}]({image[1]})"
                
                # Split the current text using the search pattern
                parts = current_text.split(search_pattern, 1)
                
                # If there's text before the image, add it to new sections
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], text_type_text))
                
                # Add the image node
                new_nodes.append(TextNode(image[0], text_type_image, image[1]))
                
                # Update current_text to the remaining part after the split
                current_text = parts[1]
            
            # If there's any text left after the last image, add it
            if current_text:
                new_nodes.append(TextNode(current_text, text_type_text))
    
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        extracted_links = extract_markdown_links(old_node.text)
        if extracted_links == []:
            new_nodes.append(old_node)
        else:
            current_text = old_node.text
            for link in extracted_links:
                # Define the search pattern based on link tuple
                search_pattern = f"[{link[0]}]({link[1]})"
                
                # Split the current text using the search pattern
                parts = current_text.split(search_pattern, 1)
                
                # If there's text before the link, add it to new sections
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], text_type_text))
                
                # Add the link node
                new_nodes.append(TextNode(link[0], text_type_link, link[1]))
                
                # Update current_text to the remaining part after the split
                current_text = parts[1]
            
            # If there's any text left after the last link, add it
            if current_text:
                new_nodes.append(TextNode(current_text, text_type_text))
    
    return new_nodes