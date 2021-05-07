"""
Константы CORS-headers
"""

access_control_allow_origin = "*"
access_control_allow_methods = "PUT", "GET", "POST", "DELETE", "OPTIONS"
access_control_allow_headers = "Content-Type", "Authorization"
access_control_expose_headers = ("Authorization", "Cache-Control",
                                 "Content-Length", "Content-Type",
                                 "X-Pagination",)
