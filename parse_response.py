import os
import json
import re


def get_response_files():
    """
    返回 raw_api_responses 目录下所有文件的文件名列表（完整路径）
    """
    files = []
    try:
        # 获取 raw_api_responses 目录的绝对路径
        base_dir = os.path.join(os.getcwd(), "raw_api_responses")
        if not os.path.exists(base_dir):
            print(f"directory does not exist: {base_dir}")
            return files

        # 遍历目录下所有文件
        for entry in os.listdir(base_dir):
            if not entry.startswith("fullItem"):
                continue

            full_path = os.path.join(base_dir, entry)
            if os.path.isfile(full_path):
                files.append(full_path)
    except Exception as e:
        print(f"error occurred: {e}")

    return files


def parse_json_file(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    vocab_list = []
    # 只处理 "data" 字段下的所有词汇
    for section in data.get('data', []):
        for item in section.get('list', []):
            vocab = {
                'title': data.get('title', ''),
                'unit_id': section.get('unit_id', 0),
                'lesson_id': item.get('lesson_id', 0),
                'word_id': item.get('word_id', 0),
                'text': item.get('text', ''),
                'note': item.get('note', ''),
                'voice': item.get('voice', ''),
                'audio_url': item.get('url', ''),
                'image_url': item.get('image', ''),
                'example_cn': item.get('template', {}).get('cn', ''),
                'example_en': item.get('template', {}).get('en', ''),
                'example_audio': item.get('template', {}).get('url', ''),
                'phrases': item.get('phrase', []),
                'story': item.get('story', {}).get('text') if item.get('story') else None,
            }
            vocab_list.append(vocab)
    return vocab_list


def sort_vocabulary(vocab_list):
    """
    按照 unit_id, lesson_id, word_id 排序词汇列表
    """
    return sorted(vocab_list, key=lambda x: (x['unit_id'], x['lesson_id'], x['word_id']))


def format_vocabulary(vocab):
    """
    格式化词汇信息为字符串，支持中英文对齐
    """
    unit_id = str(vocab['unit_id'])
    lesson_id = str(vocab['lesson_id'])
    word_id = str(vocab['word_id'])

    text = vocab['text'].strip()
    voice = re.sub(r'^/', '[', vocab['voice'].strip())
    voice = re.sub(r'/$', ']', voice)
    note = vocab['note'].strip().replace('\n', ' ')
    example_en = re.sub(r'\s+', ' ', vocab['example_en']).strip()

    # return f"- {text} | {voice} | {note} | {example_en}"
    return f"{text} | {voice} | {note} | {example_en}"


if __name__ == '__main__':
    # 替换为你的实际文件路径
    files = get_response_files()
    vocabularies = []
    for file in files:
        vocabulary_in_group = parse_json_file(file)
        vocabularies.extend(vocabulary_in_group)

    title = "IELTS Vocabulary"
    category = ""
    for vocab in sort_vocabulary(vocabularies):
        if vocab['title'] != category and vocab['title']:
            print(f"\n### {vocab['title'].replace("22类 ", "")}\n")
            category = vocab['title']

        print(f"- {format_vocabulary(vocab)}")
