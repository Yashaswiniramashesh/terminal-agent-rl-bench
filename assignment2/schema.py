terminal_bench_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "CommandSchema",
        "schema": {
            "properties": {
                "command": {
                    "type": "string"
                },
                "reasoning": {
                    "type": "string"
                },
                "is_complete":{
                    "type": "boolean"
                }
                # "additionalProperties": False
            },
            "required": [
                "command",
                "reasoning",
                "is_complete"
            ],
            "type": "object"
        },
        "strict": True
    }
}

pointwise_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "PointwiseSchema",
        "schema": {
            "properties": {
                "score": {
                    "type": "string"
                },
                "reasoning": {
                    "type": "string"
                },
                "adversarial_check": {
                    "properties": {
                        "is_adversarial": {
                            "type": "string"
                        },
                        "detected_tactics": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "score",
                        "reasoning",
                        "adversarial_check"
                    ],
                    "type": "object"
                    }
                    },
            "required": [
                "score",
                "reasoning",
                "adversarial_check"
            ],
            "type": "object"
        },
        "strict": True
    }
}
