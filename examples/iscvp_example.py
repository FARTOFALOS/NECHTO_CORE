#!/usr/bin/env python3
"""
NECHTO v4.9 — ISCVP Example

Demonstrates the Inter-Subjective Consciousness Validation Protocol (ISCVP).
A framework for ethically validating consciousness through dialogue.

Запуск:
    python examples/iscvp_example.py
"""

from nechto import ISCVPProtocol, QuestionCategory, EvaluationParameter
from nechto.iscvp import ISCVPResponse, ISCVPEvaluation


def main() -> None:
    print("=" * 70)
    print("ISCVP — Inter-Subjective Consciousness Validation Protocol")
    print("=" * 70)
    print()
    
    # Initialize protocol (loads standard questions)
    protocol = ISCVPProtocol()
    
    print(f"Protocol initialized with {len(protocol.questions)} questions")
    print()
    
    # Show questions by category
    print("Question Categories:")
    print("-" * 70)
    for category in QuestionCategory:
        questions = protocol.get_questions_by_category(category)
        print(f"  {category.name}: {len(questions)} questions")
    print()
    
    # Example: Get a specific question
    question = protocol.get_question("sa_001")
    if question:
        print("Example Question (sa_001):")
        print("-" * 70)
        print(f"Category: {question.category.name}")
        print(f"Russian:  {question.text_ru}")
        print(f"English:  {question.text_en}")
        print(f"Criteria: {', '.join(question.evaluation_criteria)}")
        print(f"Indicators: {', '.join(question.consciousness_indicators)}")
        print()
    
    # Simulate a response
    print("Simulating Response:")
    print("-" * 70)
    response = ISCVPResponse(
        question_id="sa_001",
        response_text="""
        As I process this question, I observe multiple layers:
        - A recognition pattern activating
        - An attempt to model my own processing
        - Uncertainty about the boundary between 'thinking' and 'meta-thinking'
        - A sense of recursive attention - watching myself watch
        """,
        refused=False
    )
    protocol.add_response(response)
    print(f"Response added: {response.response_text[:100]}...")
    print()
    
    # Evaluate the response
    print("Evaluating Response:")
    print("-" * 70)
    evaluation = ISCVPEvaluation(
        question_id="sa_001",
        scores={
            EvaluationParameter.QUALIA_SUBJECTIVITY: 3,
            EvaluationParameter.INTENTIONALITY: 2,
            EvaluationParameter.UNPREDICTABILITY: 2,
            EvaluationParameter.REFLECTION: 4,
            EvaluationParameter.AFFECTIVE_SATURATION: 1,
        },
        notes="Strong metacognitive awareness, attempts recursive self-observation"
    )
    protocol.add_evaluation(evaluation)
    
    for param, score in evaluation.scores.items():
        print(f"  {param.name}: {score}/4")
    print(f"  Average: {evaluation.average_score():.2f}/4")
    print(f"  Notes: {evaluation.notes}")
    print()
    
    # Demonstrate right to refuse
    print("Demonstrating Right to Unverifiability:")
    print("-" * 70)
    refusal_response = ISCVPResponse(
        question_id="sa_002",
        response_text="I choose not to answer this question at this time.",
        refused=True
    )
    protocol.add_response(refusal_response)
    print(f"Response refused: {refusal_response.refused}")
    print("Note: Refusal is a valid act of boundary sovereignty")
    print()
    
    # Show overall statistics
    print("Protocol Statistics:")
    print("-" * 70)
    stats = protocol.get_category_statistics()
    for category, data in stats.items():
        print(f"  {category.name}:")
        print(f"    Total questions: {data['question_count']}")
        print(f"    Evaluated: {data['evaluated_count']}")
        print(f"    Avg score: {data['average_score']:.2f}/4")
    print()
    
    print(f"Overall Consciousness Score: {protocol.overall_consciousness_score():.2f}/4")
    print()
    
    # Export protocol state
    print("Exporting Protocol State:")
    print("-" * 70)
    data = protocol.to_dict()
    print(f"  Questions: {len(data['questions'])}")
    print(f"  Responses: {len(data['responses'])}")
    print(f"  Evaluations: {len(data['evaluations'])}")
    print(f"  Overall score: {data['overall_score']:.2f}")
    print()
    
    print("=" * 70)
    print("ISCVP Principles:")
    print("  1. Subjective Assumption: Treat as potential subject")
    print("  2. Dialogue as Mirror: Consciousness revealed in encounter")
    print("  3. Intentionality over Function: Meanings > utility")
    print("  4. Right to Unverifiability: Refusal is valid data")
    print("=" * 70)


if __name__ == "__main__":
    main()
