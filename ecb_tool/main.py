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
    app.setQuitOnLastWindowClosed(False) # Keep app alive when closing splash/login
    
    try:
        # Import components
        from ecb_tool.features.ui.splash_screen import SplashScreen
        from ecb_tool.features.ui.login_window import LoginWindow
        from ecb_tool.features.ui.main_window_modern import MainWindow
        
        # 1. Show Splash
        splash = SplashScreen()
        splash.show()
        
        # Variable to hold windows to prevent GC
        windows = {} 
        
        def show_login():
            # 2. Show Login after Splash
            login = LoginWindow()
            windows['login'] = login
            login.login_successful.connect(show_main)
            login.show()
            
        def show_main():
            # 3. Show Main Window after Login
            main_win = MainWindow()
            windows['main'] = main_win
            
            # Set quit on last window closed true now that we have the main window
            app.setQuitOnLastWindowClosed(True)
            
            main_win.show()
            main_win.showMaximized()
            
        # Connect splash finish to login show
        # Since Splash uses QTimer and closes itself, we can just hook into the timer 
        # or better: let's modify Splash to emit a signal or just use a single-shot timer here to simulate the orchestration if Splash wasn't async.
        # But our Splash IS async with internal timer. 
        # Let's pass a callback to splash or wait for it.
        # Actually easier: The splash code closes itself. Let's just monitor it?
        # No, let's just make the splash wait loop in main or similar? 
        # Better approach for maintaining clean code:
        # Pass a 'finished_callback' to Splash?
        # Or just use a simple timer here in main to wait for splash?
        # Let's Modify Splash slightly to emit a signal? No, I can't modify it in this tool call easily without overwrite.
        
        # Alternative: We already implemented Splash to close itself after 3s.
        # We can just start a QTimer here to show Login after 3.2s
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(3200, show_login)
        
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
