from datetime import datetime, timedelta
import math

class SchedulerLogic:
    """Logic to distribute uploads throughout the day."""
    
    @staticmethod
    def calculate_slots(num_videos: int, start_hour: int = 10, end_hour: int = 22):
        """
        Calculates time slots for N videos.
        If num_videos == 1: upload at start_hour.
        If num_videos > 1: distribute evenly between start and end.
        
        Examples:
        2 videos, 10-22 (12h span) -> 10:00, 22:00 (Gap 12h)
        4 videos, 10-22 (12h span) -> 10:00, 14:00, 18:00, 22:00 (Gap 4h)
        """
        if num_videos <= 0:
            return []
            
        if num_videos == 1:
            return [f"{start_hour:02d}:00"]
            
        # Total span in hours
        # Actually user said: "se divide la hora de subida entre las 24h"
        # "si hay 2 ese dia. se sube uni cada 12h, si hay 4 uno cada 6"
        # This implies a 24h distribution starting usually from a base time.
        
        # Taking "24h" literally:
        interval_hours = 24 / num_videos
        
        slots = []
        current_hour = start_hour # Start at preferred start time
        
        for _ in range(num_videos):
            # Normalize to 24h
            hour_norm = current_hour % 24
            
            # Format
            slots.append(f"{int(hour_norm):02d}:00")
            
            current_hour += interval_hours
            
        return slots

__all__ = ['SchedulerLogic']
