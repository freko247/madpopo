# -*- coding:utf-8 -*-
from models import Language
import db


def get_language(lang):
    db.init_db()
    q = db.session.query(Language).all()
    language_dict = {}
    for language in q:
        language_dict[language.language] = language.id
    if language_dict.get(lang):
        return language_dict.get(lang)
    else:
        new_language = Language(language=lang)
        db.session.add(new_language)
        db.session.commit()
        return get_language(lang)
