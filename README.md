# Bulkrr

Bulkrr, where the 'r's stand for rapid and reliable, is an efficient tool designed to streamline the process of bulk file renaming. Whether you're managing a large collection of files or organizing data for your projects, Bulkrr empowers you with rapid and reliable renaming capabilities.

![Bulkrr Logo](Bulkrr_Logo.jpeg)

## Features

- **Bulk Renaming**: Queue up multiple files and rename them sequentially with Bulkrr's efficient bulk renaming feature.
- **Preview Changes**: Preview the changes before applying them to ensure accuracy in renaming.
- **Cross-Platform**: Bulkrr is designed to work seamlessly across different operating systems, ensuring flexibility in usage.
- **Built in Python**: Bulkrr is built using Python, making it open-source and easily modifiable to suit specific needs.
- **Open Source**: Bulkrr's source code is openly available, allowing users to modify and contribute to its development.
- **Customizable Build**: Included with Bulkrr is the `auto-py-to-exe` configuration file (`auto-py-to-exe bulkrr_onefile.json`), enabling users to rebuild Bulkrr locally after making edits to the codebase.


## Getting Started

Bulkrr is a fully portable tool, requiring no installation or setup. It provides builds for Windows, Linux, and macOS platforms, ensuring compatibility across different operating systems.

### Using Pre-built Binaries

To get started quickly, download the appropriate binary for your operating system from the [Releases](https://github.com/asorge29/bulkrr/releases) page on GitHub. Once downloaded, simply unzip the file and run Bulkrr directly without any installation process.

### Building from Source

For advanced users or those who prefer to build from source, Bulkrr's codebase is available on GitHub. Follow these steps to build Bulkrr locally:

1. **Clone the Repository**: Clone the Bulkrr repository to your local machine using Git.

```bash
git clone https://github.com/asorge29/bulkrr.git
```

2. **Install Dependencies**: Ensure you have Python installed on your system. Navigate to the cloned repository directory and install the required dependencies using pip.

```bash
pip install -r requirements.txt
```


3. **Build with PyInstaller**: Use PyInstaller to create a standalone executable for your platform. Run the following command:

```bash
pyinstaller --noconfirm --onefile --windowed --icon "C:/Users/path/to/cloned/repo/Bulkrr/bulkrr_logo_icon.ico" --splash "C:/Users/path/to/cloned/repo/Bulkrr/Bulkrr_Logo.jpeg" --add-data "C:/Users/path/to/cloned/repo/Bulkrr/Bulkrr_Logo.jpeg;."  "C:/Users/path/to/cloned/repo/Bulkrr/bulkrr.py"
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This command will generate the executable file in the `dist` directory.

4. **Alternative: Auto Py to Exe**: Alternatively, if you prefer using Auto Py to Exe, you can utilize the provided configuration file (`auto-py-to-exe bulkrr_onefile.json`) to build Bulkrr. Simply open Auto Py to Exe, load the configuration file, and generate the executable.

Ensure to replace `"path/to/cloned/repo"` with the actual path to your cloned repository in the JSON configuration file or in the command above.

By following these steps, you can build Bulkrr locally and customize it according to your preferences.


## Usage

Using Bulkrr is simple and straightforward:

1. **Load Files**: Add the files you want to rename to Bulkrr's file list. You can do this by dragging and dropping files into the Bulkrr window or by using the "Add Files" button. Additionally, you can load files from multiple source directories simultaneously, and they will remain in their original directories after renaming.

2. **Enter Name**: Enter the desired new name. A number will be added to the end of each file name automatically during renaming.

3. **Hit Rename**: Once you've entered the desired name, simply click the "Rename" button to initiate the renaming process.

Bulkrr also provides additional functionalities to manage your file queue efficiently:
- **Edit Queue**: Use the "Edit" button to modify the file list before renaming, allowing you to remove individual files as needed.
- **Clear Queue**: If you want to start fresh, use the "Clear Queue" button to remove all files from the queue.

By following these steps and utilizing Bulkrr's features, you can efficiently rename multiple files with ease.

## Contribution

Bulkrr is an open-source project developed following the Real Python tutorial. The codebase has been expanded beyond the tutorial for my specific use case, and further feature enhancements are planned. Contributions are welcome! Whether it's bug fixes, feature enhancements, or localization efforts, feel free to contribute by forking the repository and submitting a pull request.

## License

Bulkrr is licensed under the GNU General Public License v3.0 (GPL-3.0). See the [LICENSE](LICENSE) file for details.
