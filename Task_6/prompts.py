prompts = [
    "Extract person names, dates, and places from the text below.",
    "Return a JSON with keys: person_names, dates, locations. Extract entities from this text.",
    "Extract all person names (just names), dates (YYYY-MM-DD), and all locations mentioned in the text. Return JSON with those 3 fields: person_names, dates, locations.",
    "From the text below, extract:\n"
    '{"person_names": [], "dates": [], "locations": []}\n'
    "Example: Text: Bohdan Tsviliy spoke at the conference in Kyiv on June 15, 2025 and again on 2025-06-17 in Berlin.\n"
    'Output: {"person_names": ["Bohdan Tsviliy"], "dates": ["2025-06-15", "2025-06-17"], "locations": ["Kyiv", "Berlin"]}',
    "You are an information extraction tool that returns data only in JSON format with this structure:\n"
    '{"person_names": [], "dates": [], "locations": []}.\n'
    "Make sure all dates are in YYYY-MM-DD. Include all names and places mentioned. Output only valid JSON.\n"
    "Extract entities from the following text:",
]

test_cases = {
    "text": "In a recent conference in Tokyo on March 12, 2025, Prime Minister Fumio Kishida outlined Japan's plan for sustainable growth. He later visited Kyoto on 2025-03-15. Meanwhile, António Guterres attended a UN event in New York on 2nd April 2025.",
    "expected": {"person_names": 2, "dates": 3, "locations": 3},
}
