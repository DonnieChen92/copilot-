# worldtree_dictionary.py
"""
Full WORLD_TREE dictionary representation of the worldtree.root.window/jiadongchendonnie.ai
directory structure. Used by materialize_worldtree.py to write the tree to disk.
"""
from datetime import datetime

TS_PLACEHOLDER = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

WORLD_TREE = {
    "worldtree.root.window": {
        "jiadongchendonnie.ai": {
            "projects": {
                "JCD01-evidence-vault": {
                    "evidence": {"originals": {}, "derivatives": {}},
                    "meta": {
                        "README.md": "# JCD01: Evidence Vault\nContains signed manifests and evidence."
                    },
                    "provenance": {},
                    "integrity": {"manifests-signatures": {}, "merkle-roots": {}},
                    "exports": {},
                },
                "JCD02-os-remap-library": {
                    "mappings": {},
                    "rules": {},
                    "samples": {},
                    "tests": {},
                },
                "JCD03-privacy-boundary-policy-engine": {
                    "policies": {},
                    "modes": {},
                    "alignments": {},
                    "enforcement": {},
                    "audit": {},
                },
                "JCD04-au-legal-atlas-online-data": {
                    "commonwealth": {
                        "legislation-primary": {},
                        "regulators-guidance": {},
                    },
                    "states-territories": {},
                    "references": {},
                },
                "JCD05-canberra-contact-router": {
                    "parliament": {},
                    "prime-minister": {},
                    "regulators": {},
                    "directory": {},
                },
                "JCD06-device-event-timeline": {
                    "nodes": {},
                    "timelines": {},
                    "device-state": {},
                    "app-data": {},
                    "bundles": {},
                },
            },
            "schemas": {
                "conversation-record": {
                    "schema.json": """{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "conversation-record",
  "type": "object",
  "properties": {
    "id": {"type":"string"},
    "platform": {"type":"string"},
    "thread_id": {"type":["string","null"]},
    "participants": {"type":"array","items":{"type":"string"}},
    "messages": {
      "type":"array",
      "items": {
        "type":"object",
        "properties": {
          "message_id":{"type":"string"},
          "timestamp":{"type":"string","format":"date-time"},
          "author":{"type":"string"},
          "text":{"type":"string"},
          "attachments":{"type":"array","items":{"type":"string"}}
        },
        "required":["message_id","timestamp","author","text"]
      }
    },
    "provenance":{"type":"object"}
  },
  "required":["id","platform","participants","messages"]
}"""
                },
                "node-timestamp": {},
                "os-sample": {},
                "evidence": {},
            },
            "samples": {
                "conversation": {
                    "example-conversation.json": """{
  "id": "example:1",
  "platform": "chatgpt",
  "participants": ["user:me","assistant:ai"],
  "messages": [
    {
      "message_id": "m1",
      "timestamp": "2026-01-01T12:00:00Z",
      "author": "user:me",
      "text": "Hello",
      "attachments": []
    }
  ],
  "provenance": {}
}"""
                },
                "templates": {
                    "normalize_template.md": "# Normalizer template\n\nUse this template as a starting point for new platform normalizers.\n"
                },
                "os": {},
            },
            "conservations": {
                "local": {
                    "raw": {},
                    "normalized": {},
                    "indexes": {},
                    "attachments": {},
                    "redactions": {},
                    "provenance": {},
                    "exports": {},
                },
                "shared-links": {
                    "raw": {},
                    "snapshots": {},
                    "normalized": {},
                    "provenance": {},
                },
                "memory-layer": {"raw": {}, "versions": {}, "audit": {}},
                "logs": {"ingest": {}, "remap": {}, "export": {}},
            },
            "external-conservations": {
                "imports": {
                    "raw": {},
                    "manifests": {},
                    "provenance": {},
                },
                "sources": {
                    "slack": {},
                    "box": {},
                    "dropbox": {},
                    "chatgpt": {},
                    "email": {},
                    "imessage": {},
                    "whatsapp": {},
                    "wechat": {},
                    "telegram": {},
                    "discord": {},
                    "other": {},
                },
                "normalized": {"nodes": {}, "threads": {}, "attachments": {}},
                "os-samples": {"raw": {}, "mapped": {}, "tests": {}},
                "redactions": {},
                "indexes": {},
                "exports": {},
            },
            "connectors": {
                "slack": {"cache": {}, "scripts": {}},
                "box": {"cache": {}, "scripts": {}},
                "dropbox": {"cache": {}, "scripts": {}},
            },
            "scripts": {},
        }
    }
}
