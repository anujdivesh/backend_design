
class PathManager:
    # Hardcoded URL paths
    URLS = {
        'ocean-api': 'https://dev-oceanportal.spc.int/v1/api',
        'tmp': '/home/anuj/Desktop/ocean-portal/code/tmp',
        'docs': 'https://docs.example.com',
        'blog': 'https://blog.example.com'
    }

    @classmethod
    def get_url(cls, key, *args):
        """Constructs a URL by joining the specified base URL with the provided arguments."""
        if key not in cls.URLS:
            raise ValueError(f"Invalid key '{key}'. Available keys: {list(cls.URLS.keys())}")
        return "/".join([cls.URLS[key]] + list(args))

