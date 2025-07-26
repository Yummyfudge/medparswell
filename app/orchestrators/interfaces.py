from app.runner_modules.fastapi_runner import launch_fastapi_app
from fastapi import FastAPI
from app.config.settings import settings
from app.constructor.route_factory import build_routes_for_interface
import uvicorn
import logging


# Helper to parse enabled interfaces from settings
def get_enabled_interfaces():
    """
    Returns a list of enabled interface names as parsed from settings.
    """
    return [s.strip() for s in settings.enabled_interfaces.split(",") if s.strip()]


# Dispatcher dictionaries for future extensibility
INTERFACE_PREPARERS = {
    "swagger_ui": lambda app: build_routes_for_interface(app=app, interface="swagger_ui"),
    # Add new interface preparers here as needed
}

INTERFACE_LAUNCHERS = {
    "swagger_ui": launch_fastapi_app,
    # Add new interface launchers here as needed
}


def prepare_interface_routes(app: FastAPI):
    """
    Mounts routes for any interfaces declared in the .env via ENABLED_INTERFACES.
    Does not launch Uvicorn — this is pure setup.
    """
    enabled_interfaces = get_enabled_interfaces()
    for interface in enabled_interfaces:
        if interface in INTERFACE_PREPARERS:
            logging.info(f"Preparing interface: {interface}")
            INTERFACE_PREPARERS[interface](app)
        else:
            logging.warning(f"Unknown interface '{interface}' specified in ENABLED_INTERFACES. Skipping.")


def launch_interface_servers(app: FastAPI):
    """
    Starts any interface servers that serve traffic.
    For example, swagger_ui implies serving via FastAPI + Uvicorn.
    """
    enabled_interfaces = get_enabled_interfaces()
    for interface in enabled_interfaces:
        if interface in INTERFACE_LAUNCHERS:
            logging.info(f"Launching server for interface: {interface}")
            INTERFACE_LAUNCHERS[interface](app)
        else:
            logging.warning(f"Unknown interface '{interface}' specified in ENABLED_INTERFACES. Skipping.")