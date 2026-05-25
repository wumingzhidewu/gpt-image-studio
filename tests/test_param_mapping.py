import importlib.util
from pathlib import Path

path = Path(__file__).resolve().parents[1] / 'main.py'
spec = importlib.util.spec_from_file_location('app_main', path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

cases = [
    ('gpt-image-2', '方形 1:1', '4K', '3840x3840'),
    ('gpt-image-2', '宽屏 16:9', '4K', '3840x2160'),
    ('gpt-image-2', '故事版 9:16', '4K', '2160x3840'),
    ('gpt-image-2', '横版 3:2', '2K', '2048x1365'),
    ('gpt-image-1', '方形 1:1', '1.5K', '1536x1536'),
    ('gpt-image-1.5', '竖版 2:3', '1.5K', '1024x1536'),
]

for model, aspect, res, expected in cases:
    actual = mod.compute_size(aspect, res, model)
    print(f'{model:12} {aspect:10} {res:4} -> {actual}')
    assert actual == expected, (model, aspect, res, actual, expected)

print('param mapping OK')
