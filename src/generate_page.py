import os
from block_markdown import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the Markdown file
    with open(from_path, "r") as markdown_file:
        markdown_content = markdown_file.read()

    # Read the template file
    with open(template_path, "r") as template_file:
        template_content = template_file.read()

    # Convert Markdown to HTML
    node = markdown_to_html_node(markdown_content)
    html_content = node.to_html()

    # Extract title from Markdown
    title = extract_title(markdown_content)
    
    # Replace placeholders in template
    final_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write the final HTML to the destination file
    with open(dest_path, "w") as dest_file:
        dest_file.write(final_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Base Case
    if len(os.listdir(dir_path_content)) == 0:
        print("Empty Directory")
        return

    # Recursive Case
    for filename in os.listdir(dir_path_content):
        src = os.path.join(dir_path_content, filename)
        if os.path.isdir(src):
            # Recurse into subdirectory
            sub_dest = os.path.join(dest_dir_path, filename)
            generate_pages_recursive(src, template_path, sub_dest)
        elif os.path.isfile(src) and filename.endswith('.md'):
            # Set destination path with .html extension
            html_filename = filename[:-3] + ".html"
            dest = os.path.join(dest_dir_path, html_filename)
            generate_page(src, template_path, dest)