"""Application detection based on domain patterns and ports"""

import domain_patterns
import port_mappings

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
    for pattern, app_info in domain_patterns.DOMAIN_PATTERNS.items():
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
        return port_mappings.PORT_MAPPINGS.get(port_num)
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

def detect_application(src_ip, dst_ip, dst_port,
                       dns_query, dns_responses, sni_hostname, quic_sni):
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
    return {'app': 'Unknown', 'category': 'Other'}
