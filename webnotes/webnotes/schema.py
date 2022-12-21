import graphene

class Query(graphene.ObjectType):
    # создали тип данных Query с полем hello
    hello = graphene.String(default_value='Hi!')


schema = graphene.Schema(query=Query)  # создали схему данных

