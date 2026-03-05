from app.services.ai_utils import extract_json

test_cases = [
    '{"status": "ok"}',
    '```json\n{"status": "ok"}\n```',
    'Here is the JSON: {"status": "ok"}',
    'The result is: ```json {"status": "ok"} ``` Hope this helps!',
    '{"status": "ok"} and some extra text',
    '[{"id": 1}, {"id": 2}]',
    '```[{"id": 1}]```'
]

for i, case in enumerate(test_cases):
    result = extract_json(case)
    print(f"Test {i}: {'SUCCESS' if result else 'FAILED'}")
    print(f"  Input: {case!r}")
    print(f"  Output: {result}")
