class BaseAdaptor(object):

    entity = NotImplemented

    def get_by_id(self, entity_id):
        raise NotImplemented

    def get_by_id_or_fail(self, entity_id):
        raise NotImplemented

    def save(self, entity):
        raise NotImplemented


###################################################################################
#                           QUESTION
#
#           WHAT IS THE PURPOSE OF THIS CLASS ???
#
###################################################################################

