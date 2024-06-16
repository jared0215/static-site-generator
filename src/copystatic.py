import os, shutil

# Deletes the public directory with its contents and creates a new one without any content
def renewPublicPath(publicPath):
    if os.path.exists(publicPath):
        shutil.rmtree(publicPath)
    os.makedirs(publicPath, exist_ok=True)
    print("Public Path Renewed")

def copyContents(staticPath, publicPath):

    # Base Case
    if len(os.listdir(staticPath)) == 0:
        print("Empty Directory")
        return

    # Recursive Case
    for filename in os.listdir(staticPath):
        src = os.path.join(staticPath, filename)
        dest = os.path.join(publicPath, filename)

        # checking if it is a file
        if os.path.isfile(src):
            shutil.copy(src, dest)
            print(f"Copied file: {src} -> {dest}")

        elif os.path.isdir(src):
            os.makedirs(dest, exist_ok=True)  # Create the directory in the target path
            copyContents(src, dest)  # Recursively copy contents of the directory
            print(f"Created and recursed into directory: {src} -> {dest}")