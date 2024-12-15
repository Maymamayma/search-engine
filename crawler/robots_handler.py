import requests
from urllib.robotparser import RobotFileParser

def is_allowed(url):
    try:
        parsed_url = url.split('/')[2]  # Extract domain
        robots_url = f"http://{parsed_url}/robots.txt"
        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch("*", url)
    except Exception as e:
        return True  # Allow if robots.txt is inaccessible
