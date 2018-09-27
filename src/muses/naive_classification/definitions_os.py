# Class keys should start at 0 and end at the number of classes-1
# Commented classes might be added if there is more data available
classes = {
    '0': 'scarab',
    '1': 'shabti',
    '2': 'stela',
    '3': 'ostracon',
    '4': 'ring',
    '5': 'mummy',
    '6': 'bead',
    '7': 'coffin',
    '8': 'papyrus',
    '9': 'statue',
    '10': 'coin',
    '11': 'vessel',
    '12': 'relief',
    '13': 'plaque',
    '14': 'shard',
    '15': 'earring',
    '16': 'bowl',
    '17': 'jar',
    '18': 'pendant',
    '19': 'canopic jar',
    '20': 'sealing',
    '21': 'vase',
    '22': 'cone',
}

# A list of synonyms and search fields
# The search fields are used to retrieve similar objects
synonyms_extended = {
    'scarab': {
        'synonyms': ['scarab', 'scarabee', 'scarabs'],
        'exclude': [],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 4),],
    },
    'shabti': {
        'synonyms': ['ushabti', 'shabti', 'shabty', 'oesjebti', 'ushabtis', 'shabtis', 'shabtys'],
        'exclude': [],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    'stela': {
        'synonyms': ['stela', 'stele', 'steles', 'stelae', 'stelas', 'stelaes'],
        'exclude': [],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    'ostracon': {
        'synonyms': ['ostracon', 'ostracons', 'ostraca'],
        'exclude': [],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    'ring': {
        'synonyms': ['ring', 'rings'],
        'exclude': [],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    'mummy': {
        'synonyms': ['mummy', 'mummie', 'human remains', 'mummified'],
        'exclude': ['coffin', 'inner coffin', 'outer coffin', 'mummy board', 'coffins'],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    'bead': {
        'synonyms': ['bead', 'beads', 'string of beads', 'necklace', 'necklaces',],
        'exclude': ['bracelet', 'bracelets', 'pendant', 'scarab', 'statue'],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    # 'necklace': {
    #     'synonyms': ['string of beads', 'necklace', 'necklaces', 'chain', 'chains', 'collar'],
    #     'exclude': ['pendant', 'statue', 'bracelets', 'statuette'],
    #     'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 4),],
    # },
    'coffin': {
        'synonyms': ['coffin', 'inner coffin', 'outer coffin', 'mummy board', 'coffins'],
        'exclude': [],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    'papyrus': {
        'synonyms': ['papyrus', 'book of the dead', 'amduat', 'amdoeat', 'amduats', 'amdoeats'],
        'exclude': ['shard', 'fragment', 'shards', 'fragments', 'mirror', 'mirrors'],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    'statue': {
        'synonyms': ['statue', 'statuette', 'kneeling statue', 'standing statue', 'statues', 'statuettes'],
        'exclude': ['shard', 'fragment', 'shards', 'fragments'],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    'coin': {
        'synonyms': ['coin', 'tetradrachme', 'tetradrachm', 'coins', 'tetradrachmes', 'tetradrachms'],
        'exclude': [],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    'vessel': {
        'synonyms': ['vessel', 'vat', 'container', 'vessels', 'vats', 'containers'],
        'exclude': ['shard', 'fragment', 'shards', 'fragments'],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    'relief': {
        'synonyms': ['relief', 'reliefs'],
        'exclude': [],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    'plaque': {
        'synonyms': ['plaque', 'plaques'],
        'exclude': [],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    # 'amulet': {
    #     'synonyms': ['amulet', 'amulet-pendant', 'amulet-pendants', 'amulets'],
    #     'exclude': [],
    #     'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 4),],
    # },
    'shard': {
        'synonyms': ['shard', 'shards', 'fragments'], #fragment
        'exclude': [],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    'earring': {
        'synonyms': ['earring', 'earrings', 'ear'], #, 'ear ring', 'ear rings'
        'exclude': [],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    'bowl': {
        'synonyms': ['bowl', 'kom', 'bowls'],
        'exclude': ['shard', 'fragment', 'shards', 'fragments'],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    'jar': {
        'synonyms': ['jar', 'pot', 'jars', 'pots'],
        'exclude': ['canopic jar', 'canope', 'canopes', 'canopic jars', 'shard', 'fragment', 'shards', 'fragments'],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    # 'bottle': {
    #     'synonyms': ['bottle', 'bottles'],
    #     'exclude': ['shard', 'fragment', 'shards', 'fragments'],
    #     'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 4),],
    # },
    'pendant': {
        'synonyms': ['pendant', 'pendants', 'hanger', 'amulet-pendant', 'amulet-pendants'],
        'exclude': [],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    'canopic jar': {
        'synonyms': ['canopic jar', 'canope', 'canopes', 'canopic jars'],
        'exclude': ['shard', 'fragment', 'shards', 'fragments', 'canopic box', 'canopic chest'],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    # 'horuscippus': {
    #     'synonyms': ['horuscippus', 'cippus of horus', 'cippus with horus', 'stele; horus; bes', 'stela; horus; bes',
    #                 'cippus/ horus stela', 'horus-stele', 'cippus-horus stela', 'horus stele'],
    #     'exclude': [],
    #     'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 4),],
    # },
    # 'heart scarab': ['heart scarab'],
    # 'linen': ['linen', 'linnen', 'cloth', 'mummy coat', 'cloths'],
    # 'mirror': ['mirror', 'mirrors'],
    # 'basket': ['basket', 'baskets'],
    # 'axe': ['axe', 'ax', 'axes'],
    # 'arrow': ['arrow', 'arrows'],
    # 'talatat': ['talatat'],
    'sealing': {
        'synonyms': ['sealing', 'seal impression', 'seal'],
        'exclude': [],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    # 'palette': ['palette', 'palet', 'palets', 'palettes'],
    # 'offering table': ['offering table', 'offer table'],
    'vase': {
        'synonyms': ['vase', 'vaas', 'vases'],
        'exclude': ['shard', 'fragment', 'shards', 'fragments'],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    # 'dish': ['dish', 'schaal', 'dishes'],
    'cone': {
        'synonyms': ['cone', 'cones', 'funerary cone', 'funerary cones'],
        'exclude': [],
        'fields': ['title_en', ('object_type_en', 2), ('primary_object_type_en', 3),],
    },
    # 'bracelet': ['bracelet', 'bracelets'],
}
