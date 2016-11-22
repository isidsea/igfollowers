from raven.conf 		    import setup_logging
from raven.handlers.logging import SentryHandler
import raven
import logging

class Logger(raven.Client):
	def __init__(self, **kwargs):
		self.public_key = "d0f1a5199ead45238217dc7b93b8749c"
		self.secret_key = "204e6b80054c4c3fb089f301513aa001"
		self.project_id = 2

		self.dsn = "http://%s:%s@sentry:9000/%s" % (
			self.public_key,
			self.secret_key,
			self.project_id
		)
		raven.Client.__init__(self, self.dsn, auto_log_stacks=True, **kwargs)

		self.handler = SentryHandler(self)
		setup_logging(self.handler)