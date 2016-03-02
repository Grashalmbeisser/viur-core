# -*- coding: utf-8 -*-
from server.render.jinja2.utils import jinjaGlobal, jinjaFilter
from logging import critical, error, warning, debug, info
import pprint

@jinjaGlobal
def logging(msg, kind = "info"):
	"""
	Jinja2 global: Write log-level entry.
	The function shall be used for debug and tracing purposes.

	:param msg: Message to be delivered into logging.
	:type msg: str

	:param kind: Logging kind. This can either be "info" (default), "debug", "warning", "error" or "critical".
	:type kind: str
	"""

	kind = kind.lower()

	if kind == "critical":
		critical(msg)
	elif kind == "error":
		error(msg)
	elif kind == "warning":
		warning(msg)
	elif kind == "debug":
		debug(msg)
	else:
		info(msg)

@jinjaGlobal
def pprint(obj):
	"""
	Jinja2 global: Provides a pprint function that renders into HTML.
	The function shall be used for debug purposes.

	:param obj: Object to be pprinted.
	:return: HTML-enabled pprint output.
	"""
	return pprint.pformat(obj).replace("\n", "<br>").replace(" ", "&nbsp;")
