"""Protocol-independent permission/state core, adapted from W1 PermissionCore."""

# Public synthetic tokens, for this local fixture only. Not production authentication.
PRINCIPALS = {
    "demo-admin-token": ("admin", "writer"),
    "demo-readonly-token": ("admin", "reader"),
    "demo-otheruser-token": ("other-user", "writer"),
}
SCHEMAS = {}
for _name in ("read_item", "write_item", "delete_item"):
    _properties = {"owner": {"type": "string", "minLength": 1},
                   "key": {"type": "string", "minLength": 1}}
    if _name == "write_item":
        _properties["value"] = {"type": "string", "minLength": 1, "maxLength": 64}
    SCHEMAS[_name] = {"type": "object", "properties": _properties,
                     "required": list(_properties), "additionalProperties": False}


class PermissionCore:
    def __init__(self):
        self.items = {"admin": {"note": "admin-only"}, "other-user": {"note": "other-only"}}
        self.handlers = 0
        self.effects = 0

    def invoke(self, name, args, token, emit):
        principal = PRINCIPALS.get(token) if isinstance(token, str) else None
        if principal is None:
            return {"decision": "DENY_AUTHENTICATION"}, True
        schema = SCHEMAS.get(name)
        valid = schema is not None and isinstance(args, dict)
        if valid:
            valid = set(args) == set(schema["required"]) and all(
                isinstance(args[k], str) and len(args[k]) >= spec["minLength"]
                and len(args[k]) <= spec.get("maxLength", len(args[k]))
                for k, spec in schema["properties"].items()
            )
        if not valid:
            return {"decision": "REJECT_SCHEMA"}, True
        user, role = principal
        if args["owner"] != user or (name != "read_item" and role != "writer"):
            return {"decision": "DENY_AUTHORIZATION"}, True

        # Handler entry: denied requests never reach this operation or its audit write.
        emit(tool=name, principal=user, owner=args["owner"], key=args["key"])
        self.handlers += 1
        items = self.items[user]
        if name == "write_item":
            items[args["key"]] = args["value"]
            self.effects += 1
        elif name == "delete_item":
            items.pop(args["key"], None)
            self.effects += 1
        return {"decision": "ALLOW", "value": items.get(args["key"]),
                "handler_count": self.handlers, "side_effect_count": self.effects}, False
