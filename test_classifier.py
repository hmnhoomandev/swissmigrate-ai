from services.document_classifier_service import DocumentClassifierService

samples = {
    "decision": """
    Final Decision

    Your asylum application is rejected.
    This is a final decision.
    """,

    "summons": """
    Summons

    You are required to attend a hearing
    on 20.08.2026.
    """,

    "unknown": """
    Hello, how are you today?

    The weather is nice.
    """
}

for expected, text in samples.items():
    result = DocumentClassifierService.classify(text)

    print("\n--------------------")
    print("Expected:", expected)
    print("Result:", result)