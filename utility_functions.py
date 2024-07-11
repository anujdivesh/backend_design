import requests
from datetime import datetime, timedelta

class Utility:
    
    @staticmethod
    def remove_substrings(original_string, substrings):
        for substring in substrings:
            original_string = original_string.replace(substring, "")
        return original_string
    
    @staticmethod
    def add_time(current_time, days=0, hours=0, minutes=0):
        return current_time + timedelta(days=days, hours=hours, minutes=minutes)