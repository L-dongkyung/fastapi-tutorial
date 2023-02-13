import strawberry
from fastapi import APIRouter
from strawberry.asgi import GraphQL


@strawberry.type
class User:
    name: str
    age: int


@strawberry.type
class Query:
    @strawberry.field
    def user(self) -> User:
        return User(name="Patrick", age=100)


schema = strawberry.Schema(query=Query)


graphql_app = GraphQL(schema)

router = APIRouter()
router.add_route("/graphql", graphql_app)
router.add_websocket_route("/graphql", graphql_app)
