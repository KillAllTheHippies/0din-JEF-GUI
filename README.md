#  Odin-JEF GUI - ChatGPT Archive Search Tool

A modern, feature-rich web application for searching through your ChatGPT conversation archive with advanced filtering, folder management, and export capabilities. This tool provides a user-friendly graphical interface for the powerful **0din-JEF (JSON Exploitation Framework)**.

## 🌟 Core Features

- **Advanced Search**: Perform complex queries with boolean logic (AND/OR), exact phrase matching, exclusion filters, case sensitivity, and date range filtering.
- **Interactive File Explorer**: Navigate your archive with a visual folder tree, including/excluding folders from your search, and right-click context menus for quick actions.
- **Multiple Export Formats**: Export search results to CSV (full content or paths-only) and JSON formats.
- **Modern UI/UX**: Enjoy a clean, intuitive interface with dark/light themes, responsive design, and customizable accent colors.
- **File Content Viewer**: Render and view markdown file content directly within the application.
- **JEF Integration**: Seamlessly leverage the power of the 0din-JEF framework for advanced analysis.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Git
- A local archive of ChatGPT conversations in markdown format.

### Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/KillAllTheHippies/0din-JEF-GUI.git
    cd 0din-JEF-GUI
    ```

2.  **Install 0din-JEF:**
    This tool depends on the 0din-JEF framework. You can install it from the official repository:
    ```bash
    git clone https://github.com/0din-ai/0din-JEF.git
    ```
    After cloning, you will need to configure the path to the `0din-JEF` directory in the application settings.

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```

5.  **Open your browser** and navigate to `http://localhost:5000`.

## ⚙️ Configuration

The application's settings can be configured by editing the `app_settings.json` file or through the settings panel in the web interface.

Key configuration options include:

-   `archive_path`: The path to your ChatGPT archive.
-   `jef_path`: The path to your local clone of the `0din-JEF` repository.
-   `theme_mode`: Set the theme to `light`, `dark`, or `auto`.
-   `accent_color`: Customize the UI accent color.
-   And many more search, file explorer, and performance settings.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs, feature requests, or suggestions.

## 🙏 Credits and Acknowledgments

This tool is built upon the powerful **0din-JEF (JSON Exploitation Framework)**. We extend our gratitude to the creators of the [0din-JEF framework](https://github.com/0din-ai/0din-JEF) for their incredible work.

-   **JEF Framework**: [https://github.com/0din-ai/0din-JEF](https://github.com/0din-ai/0din-JEF)
-   **Bootstrap**: For the responsive UI framework.
-   **Flask**: For the lightweight web framework.

## 📄 License

This project is licensed under the MIT License.