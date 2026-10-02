"""Compatibility at the config boundary for existing EasyProxy deployments."""

from copy import deepcopy


def _aliases(value, mapping):
    if not isinstance(value, dict):
        return
    for old, new in mapping.items():
        if old in value:
            if new in value and value[new] != value[old]:
                raise ValueError(f"conflicting legacy and current config fields: {old}, {new}")
            value[new] = value.pop(old)


def normalize_legacy_config(data):
    result = deepcopy(data)
    if not isinstance(result, dict):
        return result
    task_aliases = {"ignorede": "ignore_default_exclude", "liveness": "check_alive", "rate": "max_rate", "secure": "require_tls"}
    _aliases(result, {"domains": "sites"})
    for site in result.get("sites", []):
        _aliases(site, {"sub": "subscribe", **task_aliases})
    for group in result.get("groups", {}).values():
        _aliases(group, {"list": "list_only"})
    storage = result.get("storage", {})
    _aliases(storage, {"access_key": "access_key_id", "secret_key": "secret_access_key", "public_base": "domain"})
    for item in storage.get("items", {}).values():
        _aliases(item, {"folderid": "folder_id", "fileid": "file_id", "gistid": "gist_id"})
    crawl = result.get("crawl")
    if isinstance(crawl, dict):
        _aliases(crawl, {"config": "task", "threshold": "max_fails", "singlelink": "include_nodes"})
        _aliases(crawl.get("persist"), {"subs": "subscribe", "proxies": "nodes"})
        _aliases(crawl.get("task"), task_aliases)
        _aliases(crawl.get("google"), {"limits": "limit", "notinurl": "exclude_sites", "within": "days"})
        _aliases(crawl.get("yandex"), {"notinurl": "exclude_sites", "within": "days"})
        _aliases(crawl.get("github"), {"spams": "exclude_repos"})
        telegram = crawl.get("telegram", {})
        _aliases(telegram, {"users": "channels"})
        channels = list(telegram.get("channels", {}).values())
        channels += list(crawl.get("twitter", {}).get("users", {}).values())
        for channel in channels:
            _aliases(channel, {"config": "task"})
            if isinstance(channel, dict):
                _aliases(channel.get("task"), task_aliases)
    return result
