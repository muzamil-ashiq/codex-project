# Autumn To-Do App

A visually appealing desktop To-Do application built with Tkinter, featuring an autumn-inspired theme and animated falling leaves.

## Features

- **Autumn Theme:** Warm colors for backgrounds, buttons, and text.
- **Animated Falling Leaves:** Decorative animated leaves using Pillow (PIL) and Canvas.
- **Task Management:** 
  - Add, delete, and toggle complete status for tasks.
  - Tasks are stored locally in `tasks.json`.
  - Filter tasks: All, Pending, Completed.
- **User-Friendly UI:** 
  - Sidebar menu for quick actions.
  - Scrollable task list.

## Getting Started

### Prerequisites

- Python 3.x
- Required libraries:
  - `tkinter` (standard)
  - `Pillow` (`pip install Pillow`)

### Running the App

1. Clone the repository:
    ```bash
    git clone https://github.com/muzamil-ashiq/codex-project.git
    cd codex-project
    ```
2. Make sure you have Pillow installed:
    ```bash
    pip install Pillow
    ```
3. Run the application:
    ```bash
    python todo_app.py
    ```

## File Structure

- `todo_app.py` - Main application file.
- `tasks.json` - Automatically created to store tasks.
- `resources/` - Contains leaf images for animation (created automatically if not present).

## Screenshots

*(Add screenshots here if available)*

## Customization

- Colors and images can be customized in the `autumn_colors` dictionary and `resources` folder.
- Leaf images are auto-generated if not present, but you can replace them with your own PNG images.

## License

MIT License.

---

Made with ❤️ using Python and Tkinter.
