# Desc: Mixins for models

class SerializerMixin:
    def serialize(self, include_relationships=True, exclude=[]):
        """
        Serialize an object to a dictionary.
        """
        # Get the names of all the columns in the model
        columns = [c.key for c in self.__table__.columns]
        # Add any requested relationships to the list of columns
        if include_relationships:
            columns += [c.key for c in self.__table__.relationships]
        # Remove any columns we don't want to serialize
        columns = [c for c in columns if c not in exclude]
        # Build the dictionary
        return {c: getattr(self, c) for c in columns}
       

        