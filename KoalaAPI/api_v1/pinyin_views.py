from . import api_v1
from flask import request, jsonify
from pypinyin import pinyin, lazy_pinyin


@api_v1.route('/pinyin', methods=['GET', 'POST'])
def pinyin():
    word = request.args.get('word')
    return jsonify({"pinyin": lazy_pinyin(word), "word": word})
