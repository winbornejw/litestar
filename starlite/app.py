from typing import (
    Any,
    AsyncContextManager,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Union,
)

from pydantic import BaseModel
from starlette.applications import Starlette
from starlette.datastructures import State
from starlette.middleware import Middleware
from starlette.responses import Response
from typing_extensions import Type

from starlite.controller import Controller
from starlite.enums import HttpMethod, MediaType
from starlite.routing import Router
from starlite.types import RouteHandler


# noinspection PyMethodOverriding
class StarliteAPP(Starlette):
    def __init__(  # pylint: disable=super-init-not-called
        self,
        debug: bool = False,
        middleware: Sequence[Middleware] = None,
        exception_handlers: Dict[Union[int, Type[Exception]], Callable] = None,
        routes: Optional[Sequence[Union[Type[Controller], Controller, Router, RouteHandler]]] = None,
        on_startup: Optional[Sequence[Callable]] = None,
        on_shutdown: Optional[Sequence[Callable]] = None,
        lifespan: Optional[Callable[[Any], AsyncContextManager]] = None,
        global_dependencies: Optional[Dict[str, Callable]] = None,
    ):
        self.global_dependencies = global_dependencies
        self._debug = debug
        self.state = State()
        self.router = Router(path="/", routes=routes, on_startup=on_startup, on_shutdown=on_shutdown, lifespan=lifespan)
        self.exception_handlers = dict(exception_handlers) if exception_handlers else {}
        self.user_middleware = list(middleware) if middleware else []
        self.middleware_stack = self.build_middleware_stack()

    def register(self, route_handler: Union[Type[Controller], Controller, Router, RouteHandler]):
        """
        Register a Controller, Route instance or route_handler function on the application main router

        Accepts a subclass of Controller, an instance of Router or a function/method that has been decorated
        by any of the routing decorators (e.g. route, get, post...) exported from starlite.decorators

        """
        self.router.register(route_handler=route_handler)

    def route(  # pylint: disable=arguments-differ
        self,
        path: str,
        http_method: Union[HttpMethod, List[HttpMethod]],
        include_in_schema: Optional[bool] = None,
        media_type: Optional[MediaType] = None,
        name: Optional[str] = None,
        response_class: Optional[Type[Response]] = None,
        response_headers: Optional[Union[dict, BaseModel]] = None,
        status_code: Optional[int] = None,
    ) -> Callable:
        return self.router.route(
            path=path,
            http_method=http_method,
            include_in_schema=include_in_schema,
            media_type=media_type,
            name=name,
            response_class=response_class,
            response_headers=response_headers,
            status_code=status_code,
        )

    def add_route(  # pylint: disable=arguments-differ
        self,
        path: str,
        endpoint: Callable,
        http_method: Union[HttpMethod, List[HttpMethod]],
        include_in_schema: Optional[bool] = None,
        media_type: Optional[MediaType] = None,
        name: Optional[str] = None,
        response_class: Optional[Type[Response]] = None,
        response_headers: Optional[Union[dict, BaseModel]] = None,
        status_code: Optional[int] = None,
    ):
        return self.router.add_route(
            endpoint=endpoint,
            http_method=http_method,
            include_in_schema=include_in_schema,
            media_type=media_type,
            name=name,
            path=path,
            response_class=response_class,
            response_headers=response_headers,
            status_code=status_code,
        )
