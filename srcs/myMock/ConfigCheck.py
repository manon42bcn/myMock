schema_config = {
    "type": "object",
    "properties": {
        "host": {"type": "string"},
        "port": {"type": "integer"},
        "multiple_messages": {"type": "boolean"},
        "error_code": {"type": "integer"},
        "error_range": {
            "type": "array",
            "items": {"type": "integer"}
        },
        "error_list": {"type": "boolean"},
        "GET": {
            "type": "object",
            "properties": {
                "request_field": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["request_field"]
        },
        "POST": {
            "type": "object",
            "properties": {
                "request_field": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["request_field"]
        },
        "PUT": {
            "type": "object",
            "properties": {
                "request_field": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["request_field"]
        },
        "DELETE": {
            "type": "object",
            "properties": {
                "request_field": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["request_field"]
        },
        "PATCH": {
            "type": "object",
            "properties": {
                "request_field": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["request_field"]
        },
        "templates": {
            "type": "object"
        }
    },
     "required": ["host", "port", "multiple_messages", "error_code", "error_range", "GET", "POST", "PUT", "DELETE", "PATCH", "templates"]
}

schema_template = {
        ".*": {
        "type": "object",
        "properties": {
            "request": {
                "type": "object",
                "properties": {
                        "header": {"type": "object"},
                        "data": {"type": "object"}
                },
                "required": ["header", "data"]
            },
            "response": {
                "type": "object",
                "properties": {
                        "header": {"type": "object"},
                        "data": {"type": "object"}
                },
                "required": ["header", "data"]
            },
            "error": {
                "type": "object",
                "properties": {
                        "header": {"type": "object"},
                        "data": {"type": "object"}
                },
                "required": ["header", "data"]
            }
        },
        "required": ["request", "response", "error"]
    }
}
