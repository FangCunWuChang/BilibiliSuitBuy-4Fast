from application.config import net_session_config

import httpx


class Session(httpx.Client):
    def __init__(self):
        super(Session, self).__init__(
            trust_env=net_session_config.get("trust_env", False),
            proxies=net_session_config.get("proxies", None),
            timeout=float(net_session_config.get("timeout", 5))
        )
        self.headers.update(net_session_config.get("headers", dict()))
