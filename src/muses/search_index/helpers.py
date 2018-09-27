import operator
from django.conf import settings

from elasticsearch_dsl.query import Q

import six

from muses.search_index.documents import CollectionItemDocument

__all__ = (
    'retrieve_similar',
)


def retrieve_similar(items):
    # The reason this has been moved to function level is not circular imports
    # as you might think. It's that we have to open source the project without
    # open-sourcing model definitions (entire ``naive_classification``
    # module) and thus to have the project working certain parts have to
    # be moved on function/method level. It does not make the function, of
    # course, but at least some parts of the code will work.
    from muses.naive_classification.helpers_os import predict_items
    from muses.naive_classification.definitions_os import synonyms_extended

    conf = settings.MUSES_CONFIG['classification']['naive_classification']
    model_path = conf['model_path']

    prediction = predict_items(
        items,
        model_path=model_path
    )

    top_matches = list(prediction.items())[0:3]
    qs = CollectionItemDocument().search()
    queries = []
    for idx, match in enumerate(top_matches):
        search_terms = synonyms_extended.get(match[0])['synonyms']
        search_fields = synonyms_extended.get(match[0])['fields']
        for term in search_terms:
            for field in search_fields:
                if isinstance(field, six.string_types):
                    field_name, boost = field, 1
                    query = {'query': term}
                else:
                    field_name, boost = field
                    query = {'query': term, 'boost': (boost / (idx + 1))}
                queries.append(
                    Q(
                        'match',
                        **{field_name: query}
                    )
                )

        query = {'query': match[0], 'boost': (8 / (idx + 1))}
        queries.append(
            Q(
                'match',
                **{'classified_as': query}
            )
        )

    results = qs.query(
        six.moves.reduce(operator.or_, queries)
    ).sort('_score')

    final_results = [res.to_dict() for res in results[0:200].execute()]

    return final_results, prediction
