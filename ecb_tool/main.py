"""
ECB Tool - Main Application Entry Point

Professional Beat to Video Converter and YouTube Uploader
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def setup_environment():
    """Setup application environment."""
    # Add project root to sys.path for legacy imports
    project_root_parent = project_root.parent
    if str(project_root_parent) not in sys.path:
        sys.path.insert(0, str(project_root_parent))
    
    # Change to project directory
    os.chdir(project_root_parent)
    
    # Setup FFmpeg environment
    from ecb_tool.core.paths import get_paths
    paths = get_paths()
    
    if paths.ffmpeg_bin.exists():
        os.environ["FFMPEG_BINARY"] = str(paths.ffmpeg_bin)
    if paths.ffprobe_bin.exists():
        os.environ["FFPROBE_BINARY"] = str(paths.ffprobe_bin)
    
    # Create logging
    if not paths.app_log.exists():
        paths.app_log.parent.mkdir(parents=True, exist_ok=True)
        paths.app_log.write_text("=== ECB TOOL START ===\n")
    
    return paths


def main():
    """Main application entry point."""
    paths = setup_environment()
    
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt
    except ImportError as e:
        print(f"Error importing PyQt6: {e}")
        print("Please install dependencies: pip install -r requirements.txt")
        sys.exit(1)
    
    # Configure DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Create application
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    
    try:
        # Import and create main window (NUEVA ESTRUCTURA)
        from ecb_tool.features.ui import MainWindow
        from ecb_tool.core.shared.screen_utils import get_screen_adapter
        
        window = MainWindow()
        
        # Iniciar en modo fullscreen
        window.showFullScreen()
        
        # Run application
        return app.exec()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        
        # Log error
        with open(paths.app_log, 'a', encoding='utf-8') as f:
            f.write(f"\n=== ERROR ===\n{traceback.format_exc()}\n")
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
