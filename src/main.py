import os
from textnode import TextNode
from copystatic import renewPublicPath, copyContents
from generate_page import generate_pages_recursive

staticPath = './static/'
publicPath = './public/'
projectPath = './textnode/'

from_path = "./content/"
template_path = "template.html"
dest_path = "./public/"

def main():
    print("Running renewPublicPath...")
    renewPublicPath(publicPath)

    print("Copying static contents...")
    copyContents(staticPath, publicPath)

    print("Generating page...")
    generate_pages_recursive(from_path, template_path, dest_path)
    print("Content generation and copying complete!")

    print("Creating a TextNode instance...")
    node = TextNode("This is a text node", "bold", "https://www.boot.dev")

if __name__ == "__main__":
    main()