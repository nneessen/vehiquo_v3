from sqlalchemy.orm import class_mapper

class SerializerMixin:
    def serialize(self, depth=1, include_vehicle=False, include_store=False):
        serialized_data = {c.name: getattr(self, c.name) for c in self.__table__.columns}

        if depth > 0:
            for relationship in class_mapper(self.__class__).relationships:
                if ((relationship.key == 'vehicle' and not include_vehicle) or
                    (relationship.key == 'store' and not include_store)):
                    continue

                related_obj = getattr(self, relationship.key)
                if related_obj is not None:
                    if isinstance(related_obj, list):
                        serialized_data[relationship.key] = [item.serialize(depth-1) for item in related_obj]
                    else:
                        serialized_data[relationship.key] = related_obj.serialize(depth-1)
                else:
                    serialized_data[relationship.key] = None

        return serialized_data


