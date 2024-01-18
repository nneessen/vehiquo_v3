from sqlalchemy.orm import class_mapper

class SerializerMixin:
    def serialize(self, depth=1):
        if depth < 0:
            return {}  # Or some other base case representation

        serialized_data = {c.name: getattr(self, c.name) for c in self.__table__.columns}

        if depth > 0:
            for relationship in class_mapper(self.__class__).relationships:
                related_obj = getattr(self, relationship.key)
                if related_obj is not None:
                    if isinstance(related_obj, list):
                        serialized_data[relationship.key] = [item.serialize(depth-1) for item in related_obj]
                    else:
                        serialized_data[relationship.key] = related_obj.serialize(depth-1)
                else:
                    serialized_data[relationship.key] = None

        return serialized_data

