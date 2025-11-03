"""Application detection based on domain patterns and ports"""

# Domain pattern to application mapping (ordered by priority)
# Keywords are checked against DNS queries and SNI fields
DOMAIN_PATTERNS = {
    # Social Media
    'facebook': {'app': 'Facebook', 'category': 'Social Media', 'icon': '📘'},
    'fbcdn': {'app': 'Facebook', 'category': 'Social Media', 'icon': '📘'},
    'instagram': {'app': 'Instagram', 'category': 'Social Media', 'icon': '📷'},
    'cdninstagram': {'app': 'Instagram', 'category': 'Social Media', 'icon': '📷'},
    'whatsapp': {'app': 'WhatsApp', 'category': 'Messaging', 'icon': '💬'},
    'twitter': {'app': 'Twitter/X', 'category': 'Social Media', 'icon': '🐦'},
    'twimg': {'app': 'Twitter/X', 'category': 'Social Media', 'icon': '🐦'},
    'linkedin': {'app': 'LinkedIn', 'category': 'Professional', 'icon': '💼'},
    'reddit': {'app': 'Reddit', 'category': 'Social Media', 'icon': '🔴'},
    'redd.it': {'app': 'Reddit', 'category': 'Social Media', 'icon': '🔴'},
    'snapchat': {'app': 'Snapchat', 'category': 'Social Media', 'icon': '👻'},
    'tiktok': {'app': 'TikTok', 'category': 'Social Media', 'icon': '🎵'},
    'pinterest': {'app': 'Pinterest', 'category': 'Social Media', 'icon': '📌'},
    'tumblr': {'app': 'Tumblr', 'category': 'Social Media', 'icon': '💬'},

    # Video Streaming
    'youtube': {'app': 'YouTube', 'category': 'Video', 'icon': '▶️'},
    'googlevideo': {'app': 'YouTube', 'category': 'Video', 'icon': '▶️'},
    'netflix': {'app': 'Netflix', 'category': 'Video', 'icon': '🎬'},
    'nflxvideo': {'app': 'Netflix', 'category': 'Video', 'icon': '🎬'},
    'primevideo': {'app': 'Amazon Prime', 'category': 'Video', 'icon': '📺'},
    'hotstar': {'app': 'Hotstar', 'category': 'Video', 'icon': '⭐'},
    'disneyplus': {'app': 'Disney+', 'category': 'Video', 'icon': '🏰'},
    'twitch': {'app': 'Twitch', 'category': 'Video', 'icon': '🎮'},
    'hulu': {'app': 'Hulu', 'category': 'Video', 'icon': '📺'},
    'vimeo': {'app': 'Vimeo', 'category': 'Video', 'icon': '📺'},

    # Communication
    'zoom': {'app': 'Zoom', 'category': 'Video Call', 'icon': '📹'},
    'teams.microsoft': {'app': 'Microsoft Teams', 'category': 'Video Call', 'icon': '👥'},
    'meet.google': {'app': 'Google Meet', 'category': 'Video Call', 'icon': '📞'},
    'discord': {'app': 'Discord', 'category': 'Messaging', 'icon': '💬'},
    'telegram': {'app': 'Telegram', 'category': 'Messaging', 'icon': '✈️'},
    'slack': {'app': 'Slack', 'category': 'Messaging', 'icon': '💼'},
    'skype': {'app': 'Skype', 'category': 'Video Call', 'icon': '📞'},
    'webex': {'app': 'Webex', 'category': 'Video Call', 'icon': '📹'},

    # Gaming
    'steampowered': {'app': 'Steam', 'category': 'Gaming', 'icon': '🎮'},
    'epicgames': {'app': 'Epic Games', 'category': 'Gaming', 'icon': '🎮'},
    'riotgames': {'app': 'Riot Games', 'category': 'Gaming', 'icon': '🎮'},
    'ea.com': {'app': 'EA Games', 'category': 'Gaming', 'icon': '🎮'},
    'playstation': {'app': 'PlayStation', 'category': 'Gaming', 'icon': '🎮'},
    'xbox': {'app': 'Xbox', 'category': 'Gaming', 'icon': '🎮'},
    'blizzard': {'app': 'Blizzard', 'category': 'Gaming', 'icon': '🎮'},

    # Cloud & Services
    'googleapis': {'app': 'Google Services', 'category': 'Cloud', 'icon': '☁️'},
    'google': {'app': 'Google', 'category': 'Search', 'icon': '🔍'},
    'gstatic': {'app': 'Google Static', 'category': 'CDN', 'icon': '☁️'},
    'amazonaws': {'app': 'AWS', 'category': 'Cloud', 'icon': '☁️'},
    'cloudflare': {'app': 'Cloudflare', 'category': 'CDN', 'icon': '☁️'},
    'akamai': {'app': 'Akamai CDN', 'category': 'CDN', 'icon': '☁️'},
    'microsoft': {'app': 'Microsoft', 'category': 'Cloud', 'icon': '☁️'},
    'apple': {'app': 'Apple Services', 'category': 'Cloud', 'icon': '🍎'},
    'icloud': {'app': 'iCloud', 'category': 'Cloud', 'icon': '☁️'},
    'dropbox': {'app': 'Dropbox', 'category': 'Cloud', 'icon': '📦'},
    'office.com': {'app': 'Microsoft 365', 'category': 'Cloud', 'icon': '💼'},
    'sharepoint': {'app': 'Microsoft 365', 'category': 'Cloud', 'icon': '💼'},
    'live.com': {'app': 'Microsoft', 'category': 'Cloud', 'icon': '🔷'},
    'msftauth.net': {'app': 'Microsoft Auth', 'category': 'Cloud', 'icon': '🔐'},
    'gcp': {'app': 'Google Cloud', 'category': 'Cloud', 'icon': '☁️'},
    'azure': {'app': 'Microsoft Azure', 'category': 'Cloud', 'icon': '☁️'},
    'fastly': {'app': 'Fastly CDN', 'category': 'CDN', 'icon': '☁️'},
    'github': {'app': 'GitHub', 'category': 'Development', 'icon': '💻'},
    'gitlab': {'app': 'GitLab', 'category': 'Development', 'icon': '💻'},

    # Music
    'spotify': {'app': 'Spotify', 'category': 'Music', 'icon': '🎵'},
    'scdn.co': {'app': 'Spotify', 'category': 'Music', 'icon': '🎵'},
    'pandora': {'app': 'Pandora', 'category': 'Music', 'icon': '🎵'},
    'apple-music': {'app': 'Apple Music', 'category': 'Music', 'icon': '🎵'},

    # Shopping
    'amazon': {'app': 'Amazon', 'category': 'Shopping', 'icon': '🛒'},
    'ebay': {'app': 'eBay', 'category': 'Shopping', 'icon': '🛒'},
    'walmart': {'app': 'Walmart', 'category': 'Shopping', 'icon': '🛒'},
    'shopify': {'app': 'Shopify', 'category': 'Shopping', 'icon': '🛒'},
}

# Port-based fallback for common services
PORT_MAPPINGS = {
    80: {'app': 'HTTP Web', 'category': 'Web', 'icon': '🌐'},
    443: {'app': 'HTTPS Web', 'category': 'Web', 'icon': '🔒'},
}

# Cache for IP to application mapping (from DNS resolution)
# This maps an IP address (e.g., "1.2.3.4") to its identified application info.
ip_to_app_cache = {}

def identify_app_from_domain(domain):
    """
    Identify application from domain name using pattern matching.
    Returns app info dict or None.
    """
    if not domain:
        return None
    domain_lower = domain.lower()
    # Check each pattern (prioritized order)
    for pattern, app_info in DOMAIN_PATTERNS.items():
        if pattern in domain_lower:
            return app_info
    return None

def identify_app_from_port(port):
    """
    Fallback: identify application from port number.
    Returns app info dict or None.
    """
    if not port:
        return None
    try:
        port_num = int(port)
        return PORT_MAPPINGS.get(port_num)
    except (ValueError, TypeError):
        return None

def cache_dns_mapping(ip, domain):
    """
    Cache the DNS query result for future lookups.
    Maps IP address to application based on domain.
    """
    if not ip or not domain:
        return
    app_info = identify_app_from_domain(domain)
    if app_info:
        # Store the mapping in our cache
        ip_to_app_cache[ip] = app_info

def get_app_from_ip(ip):
    """Get cached application info from IP address."""
    return ip_to_app_cache.get(ip)

# ... (all your dictionaries and other functions remain the same) ...

def detect_application(src_ip, dst_ip, src_port, dst_port, protocol, dns_query, dns_responses, sni_hostname, quic_sni):
    """
    Main detection function:
    Prioritizes TLS SNI, then QUIC SNI, then DNS, then IP cache, then ports.
    """
    
    # --- STRATEGY 1: TLS SNI (For TCP/TLS traffic) ---
    if sni_hostname:
        app_info = identify_app_from_domain(sni_hostname)
        if app_info:
            cache_dns_mapping(dst_ip, sni_hostname)
            return app_info

    # --- STRATEGY 2: QUIC SNI (For UDP/QUIC traffic) ---
    # This specifically checks QUIC packets for their own SNI tag.
    if quic_sni:
        app_info = identify_app_from_domain(quic_sni)
        if app_info:
            cache_dns_mapping(dst_ip, quic_sni)
            return app_info
            
    # --- STRATEGY 3: DNS Query Name (Accurate, but only for DNS packets) ---
    if dns_query:
        app_info = identify_app_from_domain(dns_query)
        if app_info:
            if dns_responses:
                for resp_ip in dns_responses.split(','):
                    cache_dns_mapping(resp_ip, dns_query)
            return app_info
            
    # --- STRATEGY 4: Check Cached IP Mappings (Less Accurate) ---
    for ip in [dst_ip, src_ip]:
        cached_app = get_app_from_ip(ip)
        if cached_app:
            return cached_app
            
    # --- STRATEGY 5: Port-based Fallback (Least Accurate) ---
    app_info = identify_app_from_port(dst_port)
    if app_info:
        return app_info

    # Default: Unknown
    return {'app': 'Unknown', 'category': 'Other', 'icon': '❓'}