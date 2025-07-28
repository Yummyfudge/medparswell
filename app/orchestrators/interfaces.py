from app.runner_modules.fastapi_runner import launch_fastapi_app
from fastapi import FastAPI
from app.config.settings import settings
from app.constructor.route_factory import build_route_for_interface
import uvicorn
import logging
from app.config.enums import InterfaceType


# Dispatcher dictionaries for future extensibility
INTERFACE_PREPARERS = {
    InterfaceType.SWAGGER_UI: lambda app: build_route_for_interface(app=app, interface=InterfaceType.SWAGGER_UI),
    # Add new interface preparers here as needed
}

INTERFACE_LAUNCHERS = {
    InterfaceType.SWAGGER_UI: launch_fastapi_app,
    # Add new interface launchers here as needed
}


def prepare_interface_routes(app: FastAPI):
    """
    Mounts routes for any interfaces declared in the .env via ENABLED_INTERFACES.
    Does not launch Uvicorn — this is pure setup.
    """
    for interface in get_active_interfaces():
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
    for interface in get_active_interfaces():
        if interface in INTERFACE_LAUNCHERS:
            logging.info(f"Launching server for interface: {interface}")
            INTERFACE_LAUNCHERS[interface](app)
        else:
            logging.warning(f"Unknown interface '{interface}' specified in ENABLED_INTERFACES. Skipping.")


def get_active_interfaces() -> list[InterfaceType]:
    """
    Returns the list of interfaces that are both active via .env
    and have a known handler in the INTERFACE_LAUNCHERS registry.
    """
    active_interfaces = []
    for raw_interface in settings.active_interfaces:
        try:
            interface = InterfaceType(raw_interface)
            active_interfaces.append(interface)
        except ValueError:
            logging.warning(f"Unknown interface '{raw_interface}' specified in ENABLED_INTERFACES. Skipping.")
    return active_interfaces