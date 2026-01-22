"""YouTube video uploader."""

from pathlib import Path
from typing import List, Optional
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

from ecb_tool.core.paths import get_paths
from ecb_tool.features.upload.models import UploadConfig, UploadJob


class YouTubeAuth:
    """YouTube OAuth authentication manager."""
    
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    def __init__(self):
        """Initialize YouTube authentication."""
        self.paths = get_paths()
        self.credentials = None
        self.youtube_service = None
    
    def authenticate(self):
        """Authenticate with YouTube and return service."""
        token_file = self.paths.oauth / 'token.pickle'
        secrets_file = self.paths.oauth / 'client_secrets.json'
        
        # Load existing token
        if token_file.exists():
            with open(token_file, 'rb') as token:
                self.credentials = pickle.load(token)
        
        # Refresh or get new credentials
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                if not secrets_file.exists():
                    raise FileNotFoundError(
                        f"OAuth credentials not found: {secrets_file}\n"
                        "Download from Google Cloud Console"
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(secrets_file), self.SCOPES
                )
                self.credentials = flow.run_local_server(port=0)
            
            # Save credentials
            with open(token_file, 'wb') as token:
                pickle.dump(self.credentials, token)
        
        # Build service
        self.youtube_service = build('youtube', 'v3', credentials=self.credentials)
        return self.youtube_service


class VideoUploader:
    """Handles video uploads to YouTube."""
    
    def __init__(self, config: UploadConfig):
        """
        Initialize VideoUploader.
        
        Args:
            config: Upload configuration
        """
        self.config = config
        self.paths = get_paths()
        self.auth = YouTubeAuth()
    
    def list_videos(self) -> List[Path]:
        """List all available video files for upload."""
        videos = []
        
        if self.config.videos_dir.exists():
            for file in self.config.videos_dir.iterdir():
                if file.suffix.lower() == '.mp4' and not file.name.startswith('.'):
                    videos.append(file)
        
        return sorted(videos)
    
    def get_next_title(self) -> Optional[str]:
        """Get next title from titles file."""
        if not self.config.titles_file or not self.config.titles_file.exists():
            return None
        
        try:
            with open(self.config.titles_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Find first non-empty line
            for i, line in enumerate(lines):
                title = line.strip()
                if title:
                    # Remove this title from file
                    remaining = lines[:i] + lines[i+1:]
                    with open(self.config.titles_file, 'w', encoding='utf-8') as f:
                        f.writelines(remaining)
                    return title
            
            return None
        except Exception as e:
            print(f"Error reading titles: {e}")
            return None
    
    def get_description(self) -> str:
        """Get description from file."""
        if not self.config.description_file or not self.config.description_file.exists():
            return ""
        
        try:
            with open(self.config.description_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return ""
    
    def upload(self, job: UploadJob) -> bool:
        """
        Upload a video to YouTube.
        
        Args:
            job: Upload job to process
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get YouTube service
            youtube = self.auth.authenticate()
            
            # Prepare metadata
            body = {
                'snippet': {
                    'title': job.title[:100],  # Max 100 chars
                    'description': job.description[:5000],  # Max 5000 chars
                    'categoryId': self.config.category_id,
                    'tags': ['beat', 'instrumental', 'music'],
                },
                'status': {
                    'privacyStatus': self.config.privacy_status,
                    'selfDeclaredMadeForKids': self.config.made_for_kids,
                }
            }
            
            # Prepare media
            media = MediaFileUpload(
                str(job.video_file),
                chunksize=1024*1024,  # 1MB chunks
                resumable=True,
                mimetype='video/mp4'
            )
            
            # Execute upload
            request = youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    job.progress = int(status.progress() * 100)
            
            job.status = "completed"
            job.progress = 100.0
            job.video_id = response['id']
            
            return True
            
        except HttpError as e:
            job.status = "failed"
            job.error_message = f"YouTube API error: {e}"
            return False
        except Exception as e:
            job.status = "failed"
            job.error_message = str(e)
            return False
    
    def cleanup(self, job: UploadJob) -> None:
        """
        Clean up uploaded video if configured.
        
        Args:
            job: Completed upload job
        """
        if job.status == "completed":
            if self.config.auto_delete_videos and job.video_file.exists():
                job.video_file.unlink()
            elif self.config.move_to_trash and job.video_file.exists():
                trash_path = self.paths.trash / job.video_file.name
                job.video_file.rename(trash_path)


__all__ = ['VideoUploader', 'YouTubeAuth']
